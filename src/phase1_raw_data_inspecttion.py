from pyspark.sql import SparkSession

# Start spark session
#%%
spark = (
    SparkSession.builder
    .appName("SocialMediaPhase1RawDataInspection")
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

# Display Sample rows
#%%
print("====== Posts Data ======")
posts_df.show(10, truncate = False)
print("\n====== Posts Schema =====")
posts_df.printSchema()

print("\n\n====== Engagement Data ======")
engagement_df.show(10, truncate = False)
print("\n====== Engagement Schema =====")
engagement_df.printSchema()

print("\n\n====== Users Data ======")
users_df.show(10, truncate = False)
print("\n====== Users Schema =====")
users_df.printSchema()

## List column names
print("Posts Columns: ", posts_df.columns)
print("Engagement Columns: ", engagement_df.columns)
print("Users Columns: ", users_df.columns)

## Count
print("Posts Columns: ", posts_df.count())
print("Engagement Columns: ", engagement_df.count())
print("Users Columns: ", users_df.count())

# Perform a few Simple Transformation
posts_selected_df = posts_df.select(
    "post_id",
    "user_id",
    "category",
    "post_type",
    "created_at",
    "region"
)

print("===== Selected Posts DataFrame =====")
posts_selected_df.show(5, truncate=False)

technology_posts_df = posts_df.filter(posts_df.category == "Technology")
print("===== Posts: Technology category =====")
technology_posts_df.show(5, truncate=False)

## Add cateory name length
from pyspark.sql.functions import length

posts_with_category_length_df = posts_df.withColumn("category_name_length", length(posts_df.category))
print("===== Post with category name length =====")
posts_with_category_length_df.show(5, truncate=False)

spark.stop()




