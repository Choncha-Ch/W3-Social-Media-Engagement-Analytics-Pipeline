# Section 1 — Business Reflection

## Question 1

What is the main business problem this project is trying to solve for the social media platform?

The business team wants to answer important questions such as:
- Which creators are driving the highest engagement? 
U1071: tech_pulse_915 with 26 total engagemnt score (the user with 29 is NULL)
- Which content categories perform best?
TECHNOLOGY with 181 total engagement score
- Which regions are the most active?
Middle East with 167 total engagement score
- Which posts are underperforming?
- How can the company prepare cleaner datasets for reporting and future analytics?

## Question 2

Why is raw social media activity data not enough for business reporting?
Because the raw dat still contain many duplicates, inconsistence value, inaccurate types, missing values, etc. In addition, it would still require meaningful additional columns for calculation too.

## Question 3

Why would a social media company care about:

* engagement by category to see which category drives most engangement
* engagement by creator to see which creator performs best
* engagement by region to see which region is most active on socail media

## Question 4

How does this project simulate real work done by a junior data engineer?
It demonstrate the real world datasets and all necessary transformation and data pipeline required for Data Engineer task in the real project. 

---

# Section 2 — Reflection on Phase 1 / Day 1 Concepts

## Question 5

What is a Spark DataFrame, in your own words?
A table like data structure consisting of row and columns.

## Question 6

What is a schema, and why does it matter in a Spark project?
It indicate the data type of each columns and it matter in Spark project becuase it effect the capability of data transformation. Different data types can be differently manipulated with different limitaion.

## Question 7

Why was it important to inspect the raw files before starting transformations?
To understand the data set and what needed to be done in transformation instead of writing the code blindly.

## Question 8

Explain the difference between:

* a transformation
is like a recipe of what is to be done but no real working is done yet, just a plan
* an action
is like an order the execute the actions of what is in the recipe or planning

Give at least one example of each from your project.
transformation : cache() action: count()

## Question 9

What does lazy evaluation mean in Spark, and why is it useful?

---

# Section 3 — Reflection on Phase 2 / Day 3 Concepts

## Question 10

Which columns did you select from the raw datasets, and why were those columns important?

## Question 11

Why did you rename or cast certain columns?

## Question 12

Why was it important to remove null records or incomplete rows?

## Question 13

Why was it important to remove duplicate records?

## Question 14

Why did you standardize text fields such as category, post type, or region?

## Question 15

What is a derived column?
Give one example of a derived column from your project and explain why it was useful.

## Question 16

What is the business purpose of the `engagement_score` column?

## Question 17

Why did you join the datasets together instead of analyzing each file separately?

## Question 18

Describe one grouped summary you created and explain what business insight it provides.

## Question 19

How did Spark SQL help in this project?

## Question 20

What is a UDF?
If you used the UDF step, explain why it was useful.
If you did not use it, explain when a UDF might be needed.

---

# Section 4 — Reflection on Phase 3 / Day 4 Concepts

## Question 21

Why is performance awareness important in a Spark pipeline?

## Question 22

Why was `filtered_social_media_df` a good candidate for caching?

## Question 23

What does caching do in Spark, in simple words?

## Question 24

What is a partition, in simple words?

## Question 25

What is the difference between:

* `repartition()`
* `coalesce()`

## Question 26

Why can too many small output files be a problem in a data pipeline?

## Question 27

What is Parquet, and why is it important in analytics workflows?

## Question 28

Compare CSV and Parquet in simple terms:

* Which one is easier for beginners to open and inspect?
* Which one is usually better for analytics?
* Why?

## Question 29

Why might PostgreSQL still be useful even when Spark does the main processing?

---

# Section 5 — End-to-End Project Reflection

## Question 30

Which part of the project felt most realistic to you, and why?

## Question 31

Which part of the project was most difficult, and why?

## Question 32

Which technical concept from this week became clearer to you during the mini-project?

## Question 33

If this project were used in a real company with much more data, what part of the pipeline would need the most improvement first?

## Question 34

If you had one more week to improve this project, what would you add or improve?

## Question 35

How does this mini-project reflect the learning from:

* Day 1
* Day 3
* Day 4

---

# Section 6 — Final Reflection

## Question 36

What did this project teach you about the role of a data engineer?

## Question 37

What is the difference between:

* writing code that works
* building a pipeline that is professionally structured

## Question 38

Why is it important to connect technical implementation to business value?

## Question 39

What part of your final repository are you most proud of?

## Question 40

Write a short final reflection paragraph explaining what you learned from this project.

---

# Suggested Answer Format

You may answer using a simple format like this:

```text
Q1.
Your answer here.

Q2.
Your answer here.

Q3.
Your answer here.
```

Or, if you prefer, you may use markdown headings:

```text
## Q1
Your answer here.

## Q2
Your answer here.
```

Use whichever format is clearer and more organized.

---