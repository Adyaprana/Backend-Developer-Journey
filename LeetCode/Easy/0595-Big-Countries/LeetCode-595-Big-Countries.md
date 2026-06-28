# LeetCode 595 — Big Countries

![Difficulty](https://img.shields.io/badge/Difficulty-Easy-success)
![Database](https://img.shields.io/badge/Database-MySQL-blue)
![Topic](https://img.shields.io/badge/Topic-Filtering-orange)

---

# Problem Link

https://leetcode.com/problems/big-countries/

---

# Problem Statement

A country is considered **big** if:

- It has an area of at least **3,000,000 km²**
OR
- It has a population of at least **25,000,000**

Write a SQL query to return:

- name
- population
- area

for all big countries.

The result can be returned in any order.

---

# Table Schema

## World

| Column | Type |
|---------|------|
| name | varchar |
| continent | varchar |
| area | int |
| population | int |
| gdp | bigint |

The **name** column is the primary key.

---

# Create Table

```sql
CREATE TABLE World (
    name VARCHAR(255) PRIMARY KEY,
    continent VARCHAR(255),
    area INT,
    population INT,
    gdp BIGINT
);
```

---

# Insert Sample Data

```sql
INSERT INTO World (name, continent, area, population, gdp)
VALUES
('Afghanistan','Asia',652230,25500100,20343000000),
('Albania','Europe',28748,2831741,12960000000),
('Algeria','Africa',2381741,37100000,188681000000),
('Andorra','Europe',468,78115,3712000000),
('Angola','Africa',1246700,20609294,100990000000);
```

---

# View Table

```sql
SELECT * FROM World;
```

---

# Expected Output

| name | population | area |
|------|------------|---------|
| Afghanistan | 25500100 | 652230 |
| Algeria | 37100000 | 2381741 |

Afghanistan qualifies because its population is greater than or equal to 25 million.

Algeria qualifies because its population is greater than or equal to 25 million.

---

# My Solution

```sql
SELECT
    name,
    population,
    area
FROM World
WHERE area >= 3000000
   OR population >= 25000000;
```

---

# Explanation

The problem only requires filtering rows based on two conditions.

A country is considered big if **either**:

- area ≥ 3,000,000
- population ≥ 25,000,000

Since satisfying **either** condition is enough, we use the **OR** operator.

---

# Query Breakdown

### SELECT

```sql
SELECT
    name,
    population,
    area
```

Returns only the required columns.

---

### FROM

```sql
FROM World
```

Reads data from the World table.

---

### WHERE

```sql
WHERE area >= 3000000
   OR population >= 25000000;
```

Filters countries that satisfy at least one of the required conditions.

---

# Approach

1. Read data from the World table.
2. Filter rows using the WHERE clause.
3. Use the OR operator because either condition qualifies a country as big.
4. Return only the required columns.

---

# Why This Approach?

The problem does not require:

- Sorting
- Grouping
- Joining tables
- Aggregate functions

Only filtering rows based on given conditions.

The WHERE clause is the simplest and most efficient solution.

---

# Time Complexity

Let **n** be the number of rows in the World table.

**Time Complexity**

```
O(n)
```

Every row is checked once.

---

# Space Complexity

```
O(1)
```

No extra memory is used apart from the output.

---

# Interview Questions

### Q1. Why use WHERE?

Because we need to filter rows based on conditions.

---

### Q2. Why use OR instead of AND?

The problem states that a country is big if **either** condition is true.

---

### Q3. What would happen if AND were used?

Only countries satisfying both conditions would be returned, which would produce incorrect results.

---

### Q4. Can multiple conditions be written in WHERE?

Yes.

Example:

```sql
WHERE area >= 3000000
OR population >= 25000000;
```

---

### Q5. Which SQL clause filters records?

The WHERE clause.

---

# Common Mistakes

❌ Using AND instead of OR

```sql
WHERE area >= 3000000
AND population >= 25000000;
```

This excludes countries that satisfy only one condition.

---

❌ Selecting unnecessary columns

```sql
SELECT *
```

Only return the columns requested.

---

❌ Using incorrect comparison values

```sql
300000
```

Instead of

```sql
3000000
```

Always read the constraints carefully.

---

# Key Concepts Learned

- SELECT
- FROM
- WHERE
- OR operator
- Comparison operators (>=)
- Filtering rows

---

# What I Learned

- How to filter records using the WHERE clause.
- The difference between OR and AND.
- How SQL evaluates multiple conditions.
- How to return only the required columns instead of using SELECT *.

---

# LeetCode Submission

**Status**

✅ Accepted

**Runtime**

305 ms

**Memory**

Optimized

**Language**

MySQL

**Test Cases Passed**

7 / 7

---

# Revision Notes

Remember:

- Use WHERE to filter rows.
- Use OR when either condition should match.
- Use AND only when all conditions must match.
- Return only the required columns.

---

# SQL Keywords Used

- SELECT
- FROM
- WHERE
- OR

---

# Tags

SQL • MySQL • WHERE Clause • Filtering • Database • LeetCode Easy