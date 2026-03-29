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

# Build the main cleaned pipeline
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
    trim(col("engagement_value")).try_cast("int")
)

users_cast_df = users_renamed_df.withColumn(
    "followers_count",
    trim(col("followers_count")).try_cast("int")
)

posts_cast_df = posts_selected_df.withColumn(
    "content_length",
    trim(col("content_length")).try_cast("int")
)

posts_clean_df = posts_cast_df.dropna(subset=["post_id", "user_id", "category"])
engagement_clean_df = engagement_cast_df.dropna(subset=["engagement_id", "post_id", "engagement_type"])
users_clean_df = users_cast_df.dropna(subset=["creator_user_id", "username"])

posts_dedup_df = posts_clean_df.dropDuplicates(["post_id"])
engagement_dedup_df = engagement_clean_df.dropDuplicates(["engagement_id"])
users_dedup_df = users_clean_df.dropDuplicates(["creator_user_id"])

## Clean the extra '00' in posts.post_id column to match engagement.post_id
from pyspark.sql import functions as F
posts_standardized_df = (
    posts_dedup_df
    .withColumn("category", upper(trim(col("category"))))
    .withColumn("post_type", upper(trim(col("post_type"))))
    .withColumn("region", upper(trim(col("region"))))
    .withColumn("post_id", F.regexp_replace("post_id", r"P100", "P1"))
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
    engagement_scored_df.drop("user_id"),
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


# Create the reused DataFrame
filtered_social_media_df = filtered_social_media_df.cache()
# Trigger an action to execute the cache
filtered_social_media_df.count()

# Build multiple outputs from Cached DataFrame
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


# Inspect the number of partitions .rdd.getNumberPartitions()
print("Filtered DataFrame partitions:", filtered_social_media_df.rdd.getNumPartitions())
print("Category summary partitions:", category_engagement_df.rdd.getNumPartitions())
print("Creator summary partitions:", creator_engagement_df.rdd.getNumPartitions())
print("Region summary partitions:", region_engagement_df.rdd.getNumPartitions())

# Control the number of partitions .repartition(n)
category_engagement_repartitioned_df = category_engagement_df.repartition(2)
creator_engagement_repartitioned_df = creator_engagement_df.repartition(2)
region_engagement_repartitioned_df = region_engagement_df.repartition(2)

# Use .coalasce() to reduce number of partitons with less shuggling for small outputs
category_engagement_single_file_df = category_engagement_df.coalesce(1)
region_engagement_single_file_df = region_engagement_df.coalesce(1)


# Write outputs as CSV
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


# Write outputs as Parquet
category_engagement_repartitioned_df.write.mode("overwrite").parquet(
    "data/output/parquet/category_engagement_summary"
)

creator_engagement_repartitioned_df.write.mode("overwrite").parquet(
    "data/output/parquet/creator_engagement_summary"
)

region_engagement_repartitioned_df.write.mode("overwrite").parquet(
    "data/output/parquet/region_engagement_summary"
)

# Read back a parquet file to verify it
parquet_check_df = spark.read.parquet("data/output/parquet/category_engagement_summary")
parquet_check_df.show(truncate=False)
parquet_check_df.printSchema()


# Prepare Final Summary for PostgreSQL (optional)
final_reporting_df = creator_engagement_df.select(
    "creator_user_id",
    "username",
    "creator_total_engagement"
)
print("===== Final Reporting Creator Engangement DataFrame =====")
final_reporting_df.show(truncate=False)


spark.stop()