"""Data quality rules as configuration: load them from quality_rules.yml and apply them.

This is the rules-as-data pattern from Data Quality & Validation, with the rules
moved out of Python and into a YAML file next to this module. Your Silver scripts
import it:

    from quality import load_rules, apply_quality_rules, check_quarantine_rate, split_quarantine

    rules, max_pct = load_rules("customers")              # one table's section of the YAML
    df_flagged = apply_quality_rules(df_bronze, rules)
    check_quarantine_rate(df_flagged, max_pct)            # raises if too much is bad
    df_valid, df_quarantine = split_quarantine(df_flagged)

To add or change a rule, edit quality_rules.yml, not this file.
"""

from pathlib import Path

import yaml
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, expr, lit, when
from pyspark.sql.types import BooleanType

RULES_FILE = Path(__file__).with_name("quality_rules.yml")
RULE_KEYS = {"label", "condition"}
TABLE_KEYS = {"max_quarantine_pct", "rules"}


def load_rules(table, path=RULES_FILE):
    """Return (rules, max_quarantine_pct) for one table in the rules file.

    rules is a list of (label, SQL condition) tuples, the same shape as
    QUALITY_RULES in the lesson. A malformed file fails here, loudly, before any
    data is touched.
    """
    with open(path) as f:
        config = yaml.safe_load(f) or {}

    tables = config.get("tables") or {}
    if table not in tables:
        raise KeyError(f"{Path(path).name}: no rules for table {table!r} "
                       f"(tables defined: {', '.join(tables) or 'none'})")
    section = tables[table]

    unknown = set(section) - TABLE_KEYS
    if unknown:
        raise ValueError(f"{table}: unknown key(s) {sorted(unknown)}; expected {sorted(TABLE_KEYS)}")

    rules, seen = [], set()
    for i, rule in enumerate(section.get("rules") or [], start=1):
        if not isinstance(rule, dict) or set(rule) != RULE_KEYS:
            raise ValueError(f"{table}, rule {i}: every rule needs exactly 'label' and 'condition', got {rule!r}")
        label, condition = str(rule["label"]), str(rule["condition"])
        if label in seen:
            raise ValueError(f"{table}: duplicate label {label!r}; each label must say which rule failed")
        seen.add(label)
        rules.append((label, condition))
    if not rules:
        raise ValueError(f"{table}: no rules defined")

    max_pct = float(section.get("max_quarantine_pct", 100.0))
    return rules, max_pct


def check_rules(df: DataFrame, rules) -> None:
    """Fail with the rule's label if any condition can't be evaluated against df.

    Spark only checks a SQL string when it plans a query, so a typo in the YAML
    would otherwise surface as a confusing error somewhere downstream. Asking
    for each condition's schema makes Spark parse it and resolve its column
    names now, one rule at a time.
    """
    for label, condition in rules:
        try:
            result_type = df.select(expr(condition)).schema.fields[0].dataType
        except Exception as e:
            raise ValueError(f"rule {label!r}: Spark can't evaluate {condition!r} on this table") from e
        if not isinstance(result_type, BooleanType):
            raise ValueError(f"rule {label!r}: {condition!r} has type {result_type.simpleString()}, "
                             "not a true/false condition")


def apply_quality_rules(df: DataFrame, rules) -> DataFrame:
    """Add a quality_flag column: the label of the first rule a row fails, or null if valid."""
    check_rules(df, rules)
    flag = lit(None).cast("string")
    for label, condition in reversed(rules):
        flag = when(expr(condition), label).otherwise(flag)
    return df.withColumn("quality_flag", flag)


def check_quarantine_rate(df_flagged: DataFrame, max_pct: float) -> float:
    """Raise an error if the share of flagged rows exceeds max_pct percent; return the rate."""
    total = df_flagged.count()
    flagged = df_flagged.filter(col("quality_flag").isNotNull()).count()
    pct = 100 * flagged / total if total else 0.0
    if pct > max_pct:
        raise ValueError(
            f"Quarantine rate {pct:.4f}% exceeds threshold of {max_pct}%: "
            "check the source before publishing to Silver"
        )
    print(f"Quarantine rate {pct:.4f}% is within threshold of {max_pct}%")
    return pct


def split_quarantine(df_flagged: DataFrame):
    """Split flagged rows into (valid, quarantine). Valid rows lose the flag column."""
    df_valid = df_flagged.filter(col("quality_flag").isNull()).drop("quality_flag")
    df_quarantine = df_flagged.filter(col("quality_flag").isNotNull())
    return df_valid, df_quarantine
