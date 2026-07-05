
# LeetCode 511 — Game Play Analysis I

![Difficulty](https://img.shields.io/badge/Difficulty-Easy-success)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Topic](https://img.shields.io/badge/Topic-GROUP_BY_+_MIN-orange)

---

# Problem Link

https://leetcode.com/problems/game-play-analysis-i/

---

# Problem Statement

Write a SQL query to report the **first login date** for each player.

Return:

- player_id
- first_login

The result can be returned in any order.

---

# Table Schema

## Activity

| Column | Type |
|---------|------|
| player_id | int |
| device_id | int |
| event_date | date |
| games_played | int |

The table may contain multiple records for the same player.

---

# Create Table

```sql
CREATE TABLE Activity (
    player_id INT,
    device_id INT,
    event_date DATE,
    games_played INT,
    PRIMARY KEY (player_id, event_date)
);
```

---

# Insert Sample Data

```sql
INSERT INTO Activity VALUES
(1,2,'2016-03-01',5),
(1,2,'2016-05-02',6),
(2,3,'2017-06-25',1),
(3,1,'2016-03-02',0),
(3,4,'2018-07-03',5);
```

---

# View Table

```sql
SELECT * FROM Activity;
```

---

# Expected Output

| player_id | first_login |
|-----------|-------------|
|1|2016-03-01|
|2|2017-06-25|
|3|2016-03-02|

---

# My Solution

```sql
SELECT
    player_id,
    MIN(event_date) AS first_login
FROM Activity
GROUP BY player_id;
```

---

# Explanation

Each player may have multiple login records.

To find the first login, we group the records by `player_id` and use `MIN(event_date)` to get the earliest login date.

---

# Query Breakdown

### SELECT

```sql
SELECT
    player_id,
    MIN(event_date) AS first_login
```

Returns the player's ID and their earliest login date.

---

### FROM

```sql
FROM Activity
```

Reads data from the Activity table.

---

### GROUP BY

```sql
GROUP BY player_id
```

Creates one group for each player.

---

### MIN()

```sql
MIN(event_date)
```

Returns the earliest login date within each player's group.

---

# Approach

1. Read all activity records.
2. Group records by player.
3. Find the earliest event date using `MIN()`.
4. Return the player ID and first login date.

---

# Why This Approach?

Each player can have multiple login dates.

Grouping by player creates one group per player.

`MIN(event_date)` finds the earliest login in each group.

---

# Visualization

Activity

| Player | Login Date |
|--------|------------|
|1|2016-03-01|
|1|2016-05-02|
|2|2017-06-25|
|3|2016-03-02|
|3|2018-07-03|

After GROUP BY

Player 1

```
2016-03-01
2016-05-02
```

MIN()

```
2016-03-01
```

Player 3

```
2016-03-02
2018-07-03
```

MIN()

```
2016-03-02
```

---

# Time Complexity

Let **n** be the number of activity records.

**Time Complexity**

```
O(n)
```

---

# Space Complexity

```
O(k)
```

Where **k** is the number of distinct players.

---

# Interview Questions

### Q1. Why use GROUP BY?

To create one group for each player.

---

### Q2. Why MIN(event_date)?

To find the earliest login date.

---

### Q3. Why not ORDER BY?

We only need the earliest date, not sorted output.

---

### Q4. Why is GROUP BY required?

Without it, MIN() would return only one date for the entire table.

---

### Q5. Which aggregate function is used?

`MIN()`

---

# Common Mistakes

❌ Forgetting GROUP BY

```sql
SELECT
player_id,
MIN(event_date)
```

Returns an invalid query or incorrect result.

---

❌ Using MAX()

```sql
MAX(event_date)
```

Returns the latest login instead of the first login.

---

# Key Concepts Learned

- GROUP BY
- MIN()
- Aggregate Functions
- Aliasing

---

# What I Learned

- How to find the earliest value in each group.
- How GROUP BY works with aggregate functions.
- When MIN() is sufficient without a JOIN.

---

# LeetCode Submission

**Status**

✅ Accepted

**Runtime**

2457 ms

**Memory**

0.00 MB

**Language**

PostgreSQL

**Test Cases Passed**

12 / 12

---

# Revision Notes

Remember:

- GROUP BY creates one group per player.
- MIN() returns the earliest value.
- Aggregate functions operate on grouped data.
- Use aliases for readable output.

---

# SQL Keywords Used

- SELECT
- FROM
- GROUP BY
- MIN()
- AS

---

# Tags

SQL • PostgreSQL • GROUP BY • MIN() • Aggregate Functions • Database • LeetCode Easy