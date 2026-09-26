# Project proposal

*Name:*
*Date:*

Replace every italicized prompt below with your own writing. Keep the headings. Aim for 2 to 3 pages total if this were printed; there is no need to pad it.

## 1. Project summary

*In one paragraph: what domain is your project about, and what will your finished pipeline make possible? Who might use its Gold tables, and for what?*

## 2. Questions your pipeline will answer

*List 3 to 5 concrete questions your Gold layer should be able to answer. These drive your modeling decisions in Sprint 03, so be specific. "What are trends in housing?" is too vague; "How has the median sale price per square foot changed by neighborhood each quarter since 2020?" is specific.*

1.
2.
3.

## 3. Data sources

Your project needs **at least one source of each type below**, and every source must be **novel**, which means Prof. Benbow did not use it in any of our lessons, labs, or homeworks in this course. You may add more sources beyond the three required ones.

For each source, fill in every field.

### 3.1 API source

- **Name and link:**
- **What it contains:** *What does one record represent (the grain)? Roughly how many records will you ingest?*
- **Access:** *Is an API key required? Are there rate limits? Is it paginated?*
- **Update frequency:** *Does the data change over time? How often?*
- **Real or mock:** *If you are using a Mockaroo mock API because no real API fits your idea, say so and explain what real-world API it stands in for.*

### 3.2 File source (CSV, JSON, or Parquet)

- **Name and link:**
- **Format:**
- **What it contains:** *Grain, approximate size (rows and MB).*
- **How you will obtain it:** *Direct download, scraping, periodic export, etc.*

### 3.3 Database source (SQL or MongoDB)

- **Name:**
- **Database:** *Supabase (Postgres) or MongoDB Atlas.*
- **What it contains:** *Grain, approximate size, and which tables or collections.*
- **Where the data comes from:** *You are loading this database yourself, so explain where its contents originate and how they relate to your other sources.*

## 4. How the sources connect

*Your sources need to relate to each other: a Gold layer built from three unrelated datasets is three projects, not one. What keys or attributes will you join on (a location, a date, an ID, a name)? What problems do you anticipate in matching them (inconsistent formats, different granularity, missing values)?*

## 5. Ingestion plan

*For each source, briefly describe how you will land it in Bronze: which technique from our course you will use, whether it is a one-time full load or incremental, and where raw files will land (your `final_project.bronze.landing` Volume).*

## 6. Risks and open questions

*What could go wrong? Examples: an API that might change or disappear, a rate limit that makes a full load slow, a file too large for Free Edition, uncertain terms of service for a site you want to scrape. What will you do if a source falls through?*
