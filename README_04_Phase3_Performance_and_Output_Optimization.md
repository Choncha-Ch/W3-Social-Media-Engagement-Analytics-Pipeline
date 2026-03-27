# Phase 3 — Spark Performance Awareness and Output Optimization

Welcome to **Phase 3** of the Social Media Engagement Analytics Pipeline project.

In **Phase 1**, you learned how to start Spark, load raw files, inspect schema, and understand the structure of the social media datasets.

In **Phase 2**, you did the main data engineering work: selecting columns, cleaning records, standardizing fields, joining datasets, creating derived columns, grouping, aggregating, and producing engagement-focused outputs.

Now we move to the next engineering mindset:

**A data pipeline should not only work correctly. It should also work efficiently and produce outputs in a smarter way.**

That is the purpose of this phase.

This phase is based on the learning from:

* **Week 3 — Day 4: Performance Optimization**
* Main focus:

  * caching
  * partitioning
  * output optimization

---

# Phase Objective

By the end of this phase, you should be able to:

* understand why performance matters in Spark pipelines
* explain what caching is and when it helps
* apply caching to a reused intermediate DataFrame
* understand what partitions are in practical terms
* use `repartition()` and `coalesce()` appropriately
* understand why output file organization matters
* write outputs in a more analytics-friendly format
* understand what **Parquet** is and why it is useful
* optionally prepare final results for PostgreSQL loading

---

# Why This Phase Matters in Real Work

In real companies, data engineering is not only about correctness.

A pipeline might produce correct results but still be poor engineering if it:

* runs slowly
* recomputes the same logic many times
* produces too many tiny files
* writes outputs in inefficient formats
* becomes hard to scale later

As data grows, performance decisions matter more and more.

Even in a learning project, you should start building the habit of asking:

* Can this step be reused efficiently?
* Should I cache this DataFrame?
* Am I writing output in a good format?
* Am I creating too many partitions or too few?
* Am I organizing the final output in a way that supports analytics?

That is exactly what this phase is about.

---

# Business Scenario for This Phase

The social media company is satisfied with the analytics logic from Phase 2, but now the data engineering team has received a follow-up request:

> “The pipeline works, but we want it to be more production-aware. We want the pipeline to avoid unnecessary repeated computation, organize outputs better, and prepare data in a format that is more appropriate for future analytics use.”

Your job is now to improve the engineering quality of the pipeline.

You are not redesigning the business logic.
You are improving **how the pipeline behaves**.

---

# What You Will Build in This Phase

In this phase, you will:

1. identify a DataFrame that is reused multiple times
2. cache it to avoid repeated work
3. understand what partitioning means in practice
4. use repartition or coalesce for output control
5. write final results in both a simple and improved form
6. learn what Parquet is and why it is useful
7. optionally prepare outputs for PostgreSQL loading
8. compare engineering choices and explain their business value

This phase is fully guided.
Code is provided step by step, and each step includes explanation of:

* the theory
* the business reason
* the technical implementation

---

# Important Beginner Concept — What is Caching?

## Simple explanation

When Spark processes data, it often uses **lazy evaluation**.

That means Spark builds the plan first and executes it when an **action** happens.

If the same DataFrame is used again and again in multiple later steps, Spark may recompute the same work multiple times.

That can waste time.

## What caching does

**Caching** tells Spark:

> “Keep this DataFrame in memory if possible, because I plan to reuse it.”

This can make repeated use faster.

## When caching is useful

Caching is useful when:

* a DataFrame is reused multiple times
* the earlier transformations were expensive
* you do not want Spark to recompute the whole chain repeatedly

## When caching is not useful

Caching is **not** automatically good for everything.

Do not cache every DataFrame blindly.

Caching can also use memory, so it should be applied thoughtfully.

---

# Important Beginner Concept — What is a Partition?

## Simple explanation

A **partition** is a chunk of the data.

Spark splits data into partitions so that work can be distributed across tasks.

You can think of partitions as:

* smaller pieces of a bigger dataset
* units of work Spark can process separately

## Why partitions matter

Partitions affect:

* how many tasks Spark creates
* how work is distributed
* how output files are written

## Practical meaning

If you write a DataFrame with many partitions, Spark may create many output files.

If you reduce partitions, Spark may create fewer output files.

This matters because:

* too many tiny files can be messy and inefficient
* too few partitions may reduce parallelism

So partitioning is part of practical performance thinking.

---

# Important Beginner Concept — What is Parquet?

You are going to meet **Parquet** in this phase, so it must be explained clearly.

## What is Parquet?

**Parquet** is a file format designed for analytics and big data processing.

It is different from CSV.

### CSV

* plain text
* row-based
* easy for humans to open
* simple for beginners

### Parquet

* columnar format
* better for analytics
* usually smaller in storage
* often faster when reading selected columns
* works very well with Spark

## Why Parquet is important in data engineering

In analytics pipelines, engineers often prefer Parquet because:

* Spark can read it efficiently
* storage is often smaller
* downstream analytics can perform better
* schemas are preserved better than plain CSV

## Why we used CSV earlier

In Phase 2, CSV was used because:

* it is easy to inspect
* it is simple for beginners
* it helps you see the outputs clearly

Now, in Phase 3, we begin thinking more like data engineers and less like first-time learners.
That is why Parquet appears now.

---

# Step 1 — Create the Phase 3 Script

## Task

Create a new Python file:

```python
src/phase3_optimization_and_output.py
```

## Why this matters

Separating performance/output logic into its own phase makes the project clearer and more professional.

This also reflects real engineering practice, where transformation logic and performance tuning are often reviewed carefully.

---

# Step 2 — Start Spark and Reload the Data

## Theory

Just like Phase 2, this script should be able to run independently.

That means it should:

* create its own Spark session
* load the raw files
* rebuild the Phase 2 pipeline up to the point needed for optimization work

This is a professional habit.
A script should not depend on another script having already run in memory.

---

## Technical implementation

Add this code first:

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, trim, when

spark = (
    SparkSession.builder
    .appName("SocialMediaPhase3OptimizationAndOutput")
    .master("local[*]")
    .getOrCreate()
)

posts_path = "data/raw/posts.csv"
engagement_path = "data/raw/engagement.csv"
users_path = "data/raw/users.csv"

posts_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(posts_path)
)

engagement_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(engagement_path)
)

users_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(users_path)
)
```

---

# Step 3 — Rebuild the Main Cleaned Pipeline

## Theory

To optimize something, we need a useful intermediate DataFrame to optimize.

We will rebuild the important logic from Phase 2 until we reach a cleaned, joined, reusable DataFrame.

This is the DataFrame we will later cache and use for multiple outputs.

---

## Technical implementation

Add:

```python
posts_selected_df = posts_df.select(
    "post_id",
    "user_id",
    "category",
    "post_type",
    "content_length",
    "created_at",
    "region"
)

engagement_selected_df = engagement_df.select(
    "engagement_id",
    "post_id",
    "engagement_type",
    "engagement_value",
    "user_id",
    "timestamp"
)

users_selected_df = users_df.select(
    "user_id",
    "username",
    "country",
    "account_type",
    "followers_count",
    "join_date"
)

users_renamed_df = users_selected_df.withColumnRenamed("user_id", "creator_user_id")

engagement_cast_df = engagement_selected_df.withColumn(
    "engagement_value",
    col("engagement_value").cast("int")
)

users_cast_df = users_renamed_df.withColumn(
    "followers_count",
    col("followers_count").cast("int")
)

posts_cast_df = posts_selected_df.withColumn(
    "content_length",
    col("content_length").cast("int")
)

posts_clean_df = posts_cast_df.dropna(subset=["post_id", "user_id", "category"])
engagement_clean_df = engagement_cast_df.dropna(subset=["engagement_id", "post_id", "engagement_type"])
users_clean_df = users_cast_df.dropna(subset=["creator_user_id", "username"])

posts_dedup_df = posts_clean_df.dropDuplicates(["post_id"])
engagement_dedup_df = engagement_clean_df.dropDuplicates(["engagement_id"])
users_dedup_df = users_clean_df.dropDuplicates(["creator_user_id"])

posts_standardized_df = (
    posts_dedup_df
    .withColumn("category", upper(trim(col("category"))))
    .withColumn("post_type", upper(trim(col("post_type"))))
    .withColumn("region", upper(trim(col("region"))))
)

engagement_standardized_df = engagement_dedup_df.withColumn(
    "engagement_type",
    upper(trim(col("engagement_type")))
)

engagement_scored_df = engagement_standardized_df.withColumn(
    "engagement_score",
    when(col("engagement_type") == "LIKE", 1)
    .when(col("engagement_type") == "COMMENT", 2)
    .when(col("engagement_type") == "SHARE", 3)
    .otherwise(0)
)

posts_engagement_df = posts_standardized_df.join(
    engagement_scored_df,
    on="post_id",
    how="inner"
)

full_social_media_df = posts_engagement_df.join(
    users_dedup_df,
    posts_engagement_df.user_id == users_dedup_df.creator_user_id,
    how="left"
)

filtered_social_media_df = full_social_media_df.filter(
    col("engagement_score") > 0
)
```

---

## Explanation

This DataFrame, `filtered_social_media_df`, is now a strong candidate for caching because:

* it already contains many transformations
* it is clean and joined
* it will be reused for several output summaries

That makes it a meaningful intermediate result.

---

# Step 4 — Cache the Reused DataFrame

## Theory

We will now cache the main filtered DataFrame because it will be reused several times.

Without caching, Spark may recompute much of the previous work every time we create a new aggregation or output from that DataFrame.

Caching can reduce repeated computation.

---

## Technical implementation

Add:

```python
filtered_social_media_df = filtered_social_media_df.cache()
```

Then trigger an action to materialize the cache:

```python
filtered_social_media_df.count()
```

---

## Explanation

### Why call `.count()` after `.cache()`?

Caching is lazy too.

Calling `.cache()` alone does not immediately force Spark to store the DataFrame.

The `count()` action triggers execution so Spark can actually build and cache the result.

### Business meaning

If the company will generate multiple reports from the same cleaned intermediate dataset, caching can help avoid repeating the same work over and over.

---

# Step 5 — Build Multiple Outputs from the Cached DataFrame

## Theory

Now we simulate a realistic case where the same cleaned dataset is reused for multiple business outputs.

This is exactly the kind of scenario where caching may help.

---

## Technical implementation

Add:

```python
category_engagement_df = filtered_social_media_df.groupBy("category").agg(
    {"engagement_score": "sum"}
).withColumnRenamed("sum(engagement_score)", "total_engagement_score")

creator_engagement_df = filtered_social_media_df.groupBy(
    "creator_user_id",
    "username"
).agg(
    {"engagement_score": "sum"}
).withColumnRenamed("sum(engagement_score)", "creator_total_engagement")

region_engagement_df = filtered_social_media_df.groupBy("region").agg(
    {"engagement_score": "sum"}
).withColumnRenamed("sum(engagement_score)", "region_total_engagement")
```

---

## Explanation

We are reusing the same cached DataFrame for:

* category summary
* creator summary
* region summary

This is one of the strongest reasons to cache a DataFrame.

---

# Step 6 — Inspect the Number of Partitions

## Theory

Before changing partitions, it is useful to see how many partitions a DataFrame currently has.

This helps build awareness.

---

## Technical implementation

Add:

```python
print("Filtered DataFrame partitions:", filtered_social_media_df.rdd.getNumPartitions())
print("Category summary partitions:", category_engagement_df.rdd.getNumPartitions())
print("Creator summary partitions:", creator_engagement_df.rdd.getNumPartitions())
print("Region summary partitions:", region_engagement_df.rdd.getNumPartitions())
```

---

## Explanation

### `rdd.getNumPartitions()`

This gives the number of partitions behind the DataFrame.

### Why this matters

Spark partitioning affects execution and also affects how many output files may be produced when writing results.

---

# Step 7 — Repartition a DataFrame Before Writing

## Theory

Sometimes you want to control the number of partitions before writing output.

### `repartition(n)`

This creates exactly `n` partitions and may involve reshuffling data.

Use it when you want to redistribute the data more deliberately.

### Why this matters

If output is too fragmented, you may get too many files.
If output is too compressed into too few partitions too early, you may lose parallelism.

For a small learning project, controlling file count is a good practical reason to use repartitioning.

---

## Technical implementation

Add:

```python
category_engagement_repartitioned_df = category_engagement_df.repartition(2)
creator_engagement_repartitioned_df = creator_engagement_df.repartition(2)
region_engagement_repartitioned_df = region_engagement_df.repartition(2)
```

---

## Explanation

We choose `2` here just as a simple controlled example.

In a real project, the right number depends on:

* data size
* cluster resources
* workload patterns

### Business meaning

The business may not care about the word “partition,” but it does care if the pipeline creates messy outputs or becomes harder to manage.

---

# Step 8 — Understand `coalesce()` and Use It for Small Outputs

## Theory

### What is `coalesce()`?

`coalesce(n)` reduces the number of partitions, usually with less reshuffling than `repartition()`.

It is often used when:

* you already have many partitions
* you want fewer output files
* you are reducing partitions, not expanding them

### Difference in simple words

* `repartition()` = full repartitioning, more flexible, more shuffle
* `coalesce()` = usually used to reduce partitions more gently

For small summary outputs, `coalesce()` is often practical.

---

## Technical implementation

Add:

```python
category_engagement_single_file_df = category_engagement_df.coalesce(1)
region_engagement_single_file_df = region_engagement_df.coalesce(1)
```

---

## Explanation

This is useful when you want to produce very small summary outputs with fewer files.

### Important note

Using `coalesce(1)` everywhere is not always a good idea for larger datasets, because it may reduce parallelism too much.

But for small final summaries in a learning project, it is a useful demonstration.

---

# Step 9 — Write Output as CSV

## Theory

CSV is still useful when:

* you want something easy to inspect manually
* beginners need visibility
* business users may want a simple text export

We will first write CSV as a familiar format.

---

## Technical implementation

Add:

```python
category_engagement_single_file_df.write.mode("overwrite").csv(
    "data/output/csv/category_engagement_summary",
    header=True
)

creator_engagement_repartitioned_df.write.mode("overwrite").csv(
    "data/output/csv/creator_engagement_summary",
    header=True
)

region_engagement_single_file_df.write.mode("overwrite").csv(
    "data/output/csv/region_engagement_summary",
    header=True
)
```

---

## Explanation

These are readable outputs for inspection.

### Business meaning

CSV outputs are easy to share and validate quickly, especially in early-stage workflows.

---

# Step 10 — Write Output as Parquet

## Theory

Now we move to a more professional analytics-oriented format.

As explained earlier, **Parquet** is better suited for many analytics workloads than CSV.

### Why Parquet is useful

* more storage-efficient
* better for column-based analytics
* often faster with Spark
* preserves schema better

This makes it a stronger engineering choice for downstream analytics use.

---

## Technical implementation

Add:

```python
category_engagement_repartitioned_df.write.mode("overwrite").parquet(
    "data/output/parquet/category_engagement_summary"
)

creator_engagement_repartitioned_df.write.mode("overwrite").parquet(
    "data/output/parquet/creator_engagement_summary"
)

region_engagement_repartitioned_df.write.mode("overwrite").parquet(
    "data/output/parquet/region_engagement_summary"
)
```

---

## Explanation

### `.parquet(...)`

This writes the DataFrame in Parquet format instead of CSV.

### Why use it now?

Because this phase is about engineering quality and output optimization.

### Business meaning

If the company wants these outputs to support future analytics or repeated processing, Parquet is often a better long-term choice.

---

# Step 11 — Read Back a Parquet File to Verify It

## Theory

A strong engineering habit is to verify important outputs.

Writing a file is not enough.
You should also confirm that it can be read back correctly.

---

## Technical implementation

Add:

```python
parquet_check_df = spark.read.parquet("data/output/parquet/category_engagement_summary")
parquet_check_df.show(truncate=False)
parquet_check_df.printSchema()
```

---

## Explanation

This confirms that:

* the Parquet file was written successfully
* Spark can read it back
* the schema still looks correct

---

# Step 12 — Optional: Prepare Final Summary for PostgreSQL

## Theory

In many real workflows, Spark is used for large-scale processing, and a database like PostgreSQL is used for final reporting tables.

In this project, PostgreSQL can serve as the destination for final summary outputs.

At this stage, we will prepare a final DataFrame that would be appropriate to load into PostgreSQL later.

We will not force JDBC writing here unless your environment is ready, but we will prepare for that workflow.

---

## Technical implementation

Create a business-ready final report:

```python
final_reporting_df = creator_engagement_df.select(
    "creator_user_id",
    "username",
    "creator_total_engagement"
)
```

Display it:

```python
final_reporting_df.show(truncate=False)
```

---

## Explanation

This is a clean summary that could later be loaded into PostgreSQL as a reporting table such as:

* `creator_engagement_summary`

### Business meaning

This reflects a realistic workflow:

* Spark processes raw large data
* PostgreSQL stores final structured reporting outputs

---

# Step 13 — Compare Engineering Choices

This step is about reflection inside the phase itself.

## Ask yourself:

* Why did we cache `filtered_social_media_df` and not every DataFrame?
* Why did we use `repartition()` for some outputs?
* Why did we use `coalesce(1)` for small summary files?
* Why is Parquet stronger than CSV for analytics workloads?
* Why might a final PostgreSQL table still be useful even after using Spark?

These are important engineering questions.

---

# Step 14 — Stop the Spark Session

Add:

```python
spark.stop()
```

---

# Full Example Script for Phase 3

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, trim, when

spark = (
    SparkSession.builder
    .appName("SocialMediaPhase3OptimizationAndOutput")
    .master("local[*]")
    .getOrCreate()
)

posts_path = "data/raw/posts.csv"
engagement_path = "data/raw/engagement.csv"
users_path = "data/raw/users.csv"

posts_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(posts_path)
)

engagement_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(engagement_path)
)

users_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(users_path)
)

posts_selected_df = posts_df.select(
    "post_id",
    "user_id",
    "category",
    "post_type",
    "content_length",
    "created_at",
    "region"
)

engagement_selected_df = engagement_df.select(
    "engagement_id",
    "post_id",
    "engagement_type",
    "engagement_value",
    "user_id",
    "timestamp"
)

users_selected_df = users_df.select(
    "user_id",
    "username",
    "country",
    "account_type",
    "followers_count",
    "join_date"
)

users_renamed_df = users_selected_df.withColumnRenamed("user_id", "creator_user_id")

engagement_cast_df = engagement_selected_df.withColumn(
    "engagement_value",
    col("engagement_value").cast("int")
)

users_cast_df = users_renamed_df.withColumn(
    "followers_count",
    col("followers_count").cast("int")
)

posts_cast_df = posts_selected_df.withColumn(
    "content_length",
    col("content_length").cast("int")
)

posts_clean_df = posts_cast_df.dropna(subset=["post_id", "user_id", "category"])
engagement_clean_df = engagement_cast_df.dropna(subset=["engagement_id", "post_id", "engagement_type"])
users_clean_df = users_cast_df.dropna(subset=["creator_user_id", "username"])

posts_dedup_df = posts_clean_df.dropDuplicates(["post_id"])
engagement_dedup_df = engagement_clean_df.dropDuplicates(["engagement_id"])
users_dedup_df = users_clean_df.dropDuplicates(["creator_user_id"])

posts_standardized_df = (
    posts_dedup_df
    .withColumn("category", upper(trim(col("category"))))
    .withColumn("post_type", upper(trim(col("post_type"))))
    .withColumn("region", upper(trim(col("region"))))
)

engagement_standardized_df = engagement_dedup_df.withColumn(
    "engagement_type",
    upper(trim(col("engagement_type")))
)

engagement_scored_df = engagement_standardized_df.withColumn(
    "engagement_score",
    when(col("engagement_type") == "LIKE", 1)
    .when(col("engagement_type") == "COMMENT", 2)
    .when(col("engagement_type") == "SHARE", 3)
    .otherwise(0)
)

posts_engagement_df = posts_standardized_df.join(
    engagement_scored_df,
    on="post_id",
    how="inner"
)

full_social_media_df = posts_engagement_df.join(
    users_dedup_df,
    posts_engagement_df.user_id == users_dedup_df.creator_user_id,
    how="left"
)

filtered_social_media_df = full_social_media_df.filter(
    col("engagement_score") > 0
)

filtered_social_media_df = filtered_social_media_df.cache()
filtered_social_media_df.count()

category_engagement_df = filtered_social_media_df.groupBy("category").agg(
    {"engagement_score": "sum"}
).withColumnRenamed("sum(engagement_score)", "total_engagement_score")

creator_engagement_df = filtered_social_media_df.groupBy(
    "creator_user_id",
    "username"
).agg(
    {"engagement_score": "sum"}
).withColumnRenamed("sum(engagement_score)", "creator_total_engagement")

region_engagement_df = filtered_social_media_df.groupBy("region").agg(
    {"engagement_score": "sum"}
).withColumnRenamed("sum(engagement_score)", "region_total_engagement")

print("Filtered DataFrame partitions:", filtered_social_media_df.rdd.getNumPartitions())
print("Category summary partitions:", category_engagement_df.rdd.getNumPartitions())
print("Creator summary partitions:", creator_engagement_df.rdd.getNumPartitions())
print("Region summary partitions:", region_engagement_df.rdd.getNumPartitions())

category_engagement_repartitioned_df = category_engagement_df.repartition(2)
creator_engagement_repartitioned_df = creator_engagement_df.repartition(2)
region_engagement_repartitioned_df = region_engagement_df.repartition(2)

category_engagement_single_file_df = category_engagement_df.coalesce(1)
region_engagement_single_file_df = region_engagement_df.coalesce(1)

category_engagement_single_file_df.write.mode("overwrite").csv(
    "data/output/csv/category_engagement_summary",
    header=True
)

creator_engagement_repartitioned_df.write.mode("overwrite").csv(
    "data/output/csv/creator_engagement_summary",
    header=True
)

region_engagement_single_file_df.write.mode("overwrite").csv(
    "data/output/csv/region_engagement_summary",
    header=True
)

category_engagement_repartitioned_df.write.mode("overwrite").parquet(
    "data/output/parquet/category_engagement_summary"
)

creator_engagement_repartitioned_df.write.mode("overwrite").parquet(
    "data/output/parquet/creator_engagement_summary"
)

region_engagement_repartitioned_df.write.mode("overwrite").parquet(
    "data/output/parquet/region_engagement_summary"
)

parquet_check_df = spark.read.parquet("data/output/parquet/category_engagement_summary")
parquet_check_df.show(truncate=False)
parquet_check_df.printSchema()

final_reporting_df = creator_engagement_df.select(
    "creator_user_id",
    "username",
    "creator_total_engagement"
)

final_reporting_df.show(truncate=False)

spark.stop()
```

---

# Phase 3 Checkpoint Tasks

Complete the following after running the script.

## Task 1

Explain why `filtered_social_media_df` was a good candidate for caching.

## Task 2

Explain in your own words what caching does in Spark.

## Task 3

Check the number of partitions in at least two DataFrames and record your observations.

## Task 4

Explain the difference between:

* `repartition()`
* `coalesce()`

## Task 5

Explain why too many small output files can be a problem.

## Task 6

Explain what Parquet is in simple words.

## Task 7

Compare CSV and Parquet:

* Which one is easier for humans to inspect?
* Which one is generally better for analytics workloads?
* Why?

## Task 8

Explain why PostgreSQL may still be useful even when Spark does the heavy processing.

---

# What You Should Understand Before Finishing the Project

Before leaving this phase, make sure you are comfortable with:

* why performance matters in Spark
* when caching is useful
* what a partition is
* how partition count affects output organization
* the difference between `repartition()` and `coalesce()`
* why Parquet is an important analytics format
* why final reporting data may still be stored in PostgreSQL

---

# End of Phase 3

At this point, you have completed the final technical phase of the project.

You now understand how to:

* improve a Spark pipeline beyond simple correctness
* reuse intermediate results more intelligently
* think about partition-aware output design
* choose better output formats for analytics
* connect Spark processing to final business-ready reporting outputs

This is an important step toward thinking like a real data engineer.

---

# Next Step

Continue to:

**`README_05_Project_Deliverables_and_Submission.md`**

In the next README, you will review exactly what needs to be submitted, how your repository should be organized, and what files and outputs are expected for this mini-project.
