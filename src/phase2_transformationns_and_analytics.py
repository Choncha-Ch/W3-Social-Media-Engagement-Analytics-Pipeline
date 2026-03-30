from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("SocialMediaPhase2TransformationsAndAnalytics")
    .master("local[*]")
    .getOrCreate()
    )

# Define file paths
#%%
posts_path = "data/raw/posts.csv"
engagement_path = "data/raw/engagement.csv"
users_path = "data/raw/users.csv"

# Read Raw Data including row, column & data types
#%%
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


# Select only the meaningful columns
#%%
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


# Rename Columns for clarity .withColumnRenamed()
users_renamed_df = users_selected_df.withColumnRenamed("user_id", "creator_user_id")

# Cast Data Type
from pyspark.sql.functions import col, trim

post_cast_df = posts_selected_df.withColumn(
    "content_length", trim(col("content_length")).try_cast("int")
)

engagement_cast_df = engagement_selected_df.withColumn(
    "engagement_value", trim(col("engagement_value")).try_cast("int")
    )

users_cast_df = users_renamed_df.withColumn(
    "followers_count", trim(col("followers_count")).try_cast("int")
)

# Remove invalid or incomplete records
posts_clean_df = post_cast_df.dropna(subset=["post_id", "user_id", "category"])
engagement_clean_df = engagement_cast_df.dropna(subset=["engagement_id", "post_id", "engagement_type"])
users_clean_df = users_cast_df.dropna(subset=["creator_user_id", "username"])

# Remove duplicat records
posts_dedup_df = posts_clean_df.dropDuplicates(["post_id"])
engagment_dedup_df = engagement_clean_df.dropDuplicates(["engagement_id"])
users_dedup_df = users_clean_df.dropDuplicates(["creator_user_id"])


# Standardize text fields
from pyspark.sql.functions import upper
## Clean the extra '00' in posts.post_id column to match engagement.post_id
from pyspark.sql import functions as F

posts_standardized_df = (
    posts_dedup_df
    .withColumn("category", upper(trim(col("category"))))
    .withColumn("post_type", upper(trim(col("post_type"))))
    .withColumn("region", upper(trim(col("region"))))
    .withColumn("post_id", F.regexp_replace("post_id", r"P100", "P1"))
)

engagement_standardized_df = (
    engagment_dedup_df
    .withColumn("engagement_type", upper(trim(col("engagement_type"))))
)

# Create a derive engagement score for technical implementation
from pyspark.sql.functions import when

engagement_scored_df = (
    engagement_standardized_df
    .withColumn("engagement_score",
                when(col("engagement_type") == "LIKE", 1)
                .when(col("engagement_type") == "COMMENT", 2)
                .when(col("engagement_type") == "SHARE", 3)
                .otherwise(0)
    )
)

# Join the Datasets
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

# Filter record for business relevance
filterd_social_media_df = full_social_media_df.filter(
    col("engagement_score") > 0)
print("===== Filtered Social Media DataFrame Schema ======")
filterd_social_media_df.printSchema()




# Group & Aggregate the data
category_engagement_df = filterd_social_media_df.groupBy("category").agg(
    {"engagement_score": "sum"}
).withColumnRenamed("sum(engagement_score)", "total_engagement_score")
print("===== Category Engagement DataFrame =====")
category_engagement_df.show(truncate=False)

creator_engagement_df = filterd_social_media_df.groupBy(
    "user_id",
    "username"
).agg(
    {"engagement_score": "sum"}
).withColumnRenamed("sum(engagement_score)", "creator_total_engagement")
print("===== Creator Engagement DataFrame =====")
creator_engagement_df.show(truncate=False)

region_engagement_df = filterd_social_media_df.groupBy("region").agg(
    {"engagement_score": "sum"}
).withColumnRenamed("sum(engagement_score)", "region_total_engagement")
print("===== Region Engagement DataFrame =====")
region_engagement_df.show(truncate=False)


# Use SparkSQL for reporting queries
## Create temporary view
filterd_social_media_df.createOrReplaceTempView("social_media_activity")

## Run SQL query
top_categories_sql_df = spark.sql("""
    SELECT
        category,
        SUM(engagement_score) AS total_engagement_score,
        COUNT(DISTINCT post_id) AS total_posts
    FROM social_media_activity
    GROUP BY category
    ORDER BY total_engagement_score DESC
""")

print("===== SQL: Top Category =====")
top_categories_sql_df.show(truncate=False)

# Use a simple UDF (optional)
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

def classify_creator_size(followers_count):
    if followers_count is None:
        return "UNKNONW"
    elif followers_count < 1000:
        return "SMALL"
    elif followers_count < 10000:
        return "MEDIUM"
    else:
        return "LARGE"
    
classify_creator_size_udf = udf(classify_creator_size, StringType())

creator_classified_df = filterd_social_media_df.withColumn(
    "creator_size",
    classify_creator_size_udf(col("followers_count"))
)

print("===== UDF: Creator Classified DataFrame =====")
creator_classified_df.select(
    "creator_user_id",
    "username",
    "followers_count",
    "creator_size"
).show(10, truncate=False)


# Write processed Outputs
category_engagement_df.write.mode("overwrite").csv(
    "data/processed/category_engagement_summary",
    header=True
)

creator_engagement_df.write.mode("overwrite").csv(
    "data/processed/creator_engagement_summary",
    header=True
)

region_engagement_df.write.mode("overwrite").csv(
    "data/processed/region_engagment_summary",
    header=True
)


spark.stop()



