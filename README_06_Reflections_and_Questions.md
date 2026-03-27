# Reflections and Questions to Answer

Welcome to the final part of the **Social Media Engagement Analytics Pipeline** mini-project.

This README is not about writing more code.
It is about showing that you understand:

* the business problem
* the Spark pipeline you built
* the technical decisions you made
* the reason behind those decisions
* how the theory from the week was applied in practice

In real data engineering work, it is not enough to build a pipeline and stop there. Engineers are often expected to explain:

* what the pipeline does
* why the design makes sense
* what business value it provides
* what could be improved later

This reflection file is designed to help you practice that professional habit.

---

# Purpose of This README

This file helps you show that you can connect:

* **business understanding**
* **technical implementation**
* **engineering reasoning**

Your answers should show that you understand not only **what** you did, but also **why** you did it.

---

# Submission Instruction

Create a file for your answers if your instructor asks for a separate response file, for example:

```text
docs/checkpoint_answers.md
```

You may either:

* answer directly in this README if instructed to do so, or
* copy the questions into your answer file and write your answers there

Follow your instructor’s submission instructions.

---

# How to Answer

Your answers should be:

* clear
* complete
* professional
* written in your own words

Try to avoid one-word answers.

A strong answer should explain:

* the idea
* the reason
* the business or technical importance

---

# Section 1 — Business Reflection

## Question 1

What is the main business problem this project is trying to solve for the social media platform?

## Question 2

Why is raw social media activity data not enough for business reporting?

## Question 3

Why would a social media company care about:

* engagement by category
* engagement by creator
* engagement by region

## Question 4

How does this project simulate real work done by a junior data engineer?

---

# Section 2 — Reflection on Phase 1 / Day 1 Concepts

## Question 5

What is a Spark DataFrame, in your own words?

## Question 6

What is a schema, and why does it matter in a Spark project?

## Question 7

Why was it important to inspect the raw files before starting transformations?

## Question 8

Explain the difference between:

* a transformation
* an action

Give at least one example of each from your project.

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

# What a Strong Answer Looks Like

A strong answer:

* explains the idea clearly
* uses examples from your own project
* shows understanding of both business and technical reasoning
* avoids very short vague answers
* sounds professional and thoughtful

### Weak example

“Because it is useful.”

### Stronger example

“It was important to standardize category values because grouping depends on consistent text values. Without standardization, the same business category could appear under multiple spellings, which would make the final engagement summaries inaccurate.”

---

# Final Reminder

These questions are part of the project.

They are not extra optional writing.

They help show that you understand:

* the purpose of the pipeline
* the Spark concepts from the week
* the connection between theory and implementation
* the business reason behind the engineering work

Treat this part seriously.

A strong project is not only code.
A strong project also shows understanding.

---

# Final Note

By the time you reach this README, you have completed:

* **Phase 1** — Spark foundations and raw data understanding
* **Phase 2** — data processing and engagement analytics
* **Phase 3** — performance awareness and output optimization

That means you have now built a small but realistic Spark data engineering project.

Use these reflection questions to show the full value of what you built.

---

# End of Project

You have reached the final README of the Week 3 Spark mini-project.

Make sure your repository now includes:

* all README files
* all Spark scripts
* your outputs
* your SQL file
* your reflection answers

Once that is done, your project submission is complete.
