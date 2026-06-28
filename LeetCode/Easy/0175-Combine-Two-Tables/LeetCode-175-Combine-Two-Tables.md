# LeetCode 175 — Combine Two Tables

![Difficulty](https://img.shields.io/badge/Difficulty-Easy-success)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Topic](https://img.shields.io/badge/Topic-JOIN-orange)

---

# Problem Link

https://leetcode.com/problems/combine-two-tables/

---

# Problem Statement

Write a SQL query to report:

- firstName
- lastName
- city
- state

for every person in the Person table.

If a person's address is not present, return NULL for city and state.

---

# Table Schema

## Person

| Column | Type |
|---------|------|
| personId | int |
| firstName | varchar |
| lastName | varchar |

personId is the primary key.

---

## Address

| Column | Type |
|---------|------|
| addressId | int |
| personId | int |
| city | varchar |
| state | varchar |

addressId is the primary key.

personId is a foreign key referencing Person.

---

# Create Tables

```sql
CREATE TABLE Person (
    personId INT PRIMARY KEY,
    firstName VARCHAR(50),
    lastName VARCHAR(50)
);

CREATE TABLE Address (
    addressId INT PRIMARY KEY,
    personId INT,
    city VARCHAR(50),
    state VARCHAR(50),
    FOREIGN KEY (personId) REFERENCES Person(personId)
);
```

---

# Insert Sample Data

```sql
INSERT INTO Person (personId, firstName, lastName)
VALUES
(1,'Wang','Allen'),
(2,'Alice','Bob');

INSERT INTO Address (addressId, personId, city, state)
VALUES
(1,2,'New York City','New York'),
(2,3,'Leetcode','California');
```

---

# View Data

```sql
SELECT * FROM Person;

SELECT * FROM Address;
```

Output

Person

| personId | firstName | lastName |
|----------|-----------|----------|
|1|Wang|Allen|
|2|Alice|Bob|

Address

|addressId|personId|city|state|
|---------|--------|----|------|
|1|2|New York City|New York|
|2|3|Leetcode|California|

---

# Expected Output

| firstName | lastName | city | state |
|------------|----------|----------------|-----------|
| Wang | Allen | NULL | NULL |
| Alice | Bob | New York City | New York |

---

# My Solution

```sql
SELECT
    Person.firstName,
    Person.lastName,
    Address.city,
    Address.state
FROM Person
LEFT JOIN Address
ON Person.personId = Address.personId;
```

---

# Explanation

The query starts with the Person table because the problem asks to display **every person**.

A **LEFT JOIN** keeps all rows from the left table (Person).

If a matching address exists, city and state are returned.

If no address exists, SQL returns **NULL**.

---

# Why LEFT JOIN?

There are four common joins:

- INNER JOIN
- LEFT JOIN
- RIGHT JOIN
- FULL OUTER JOIN

The requirement says:

> Show every person even if they don't have an address.

Only **LEFT JOIN** guarantees that every record from Person is included.

Example:

Person

|personId|Name|
|--------|----|
|1|Wang|
|2|Alice|

Address

|personId|City|
|--------|----|
|2|New York|

LEFT JOIN Result

|Name|City|
|----|----|
|Wang|NULL|
|Alice|New York|

---

# Query Breakdown

### SELECT

```sql
SELECT
    Person.firstName,
    Person.lastName,
    Address.city,
    Address.state
```

Selects the required columns.

---

### FROM

```sql
FROM Person
```

Person becomes the main table.

---

### LEFT JOIN

```sql
LEFT JOIN Address
```

Joins the Address table.

---

### ON

```sql
ON Person.personId = Address.personId;
```

Matches both tables using personId.

---

# Approach

1. Start from Person.
2. Join Address using personId.
3. Keep all persons.
4. Return NULL if address doesn't exist.

---

# Why This Approach?

The problem specifically requires all people.

If we used INNER JOIN:

```sql
SELECT *
FROM Person
INNER JOIN Address
ON Person.personId = Address.personId;
```

Output

Only Alice would appear.

Wang would be removed because no matching address exists.

Therefore INNER JOIN is incorrect.

LEFT JOIN satisfies the requirement.

---

# Time Complexity

Let

- n = rows in Person
- m = rows in Address

Time Complexity

```
O(n + m)
```

(with indexes)

Space Complexity

```
O(1)
```

(excluding result set)

---

# Interview Questions

### Q1. Why not INNER JOIN?

Because INNER JOIN only returns matching records.

---

### Q2. Why LEFT JOIN?

Because the problem asks to keep every person.

---

### Q3. What happens if there is no address?

city and state become NULL.

---

### Q4. Which table should be on the left?

Person.

Because we need every person.

---

### Q5. Which column is used to join?

personId

---

# Common Mistakes

❌ Using INNER JOIN

```sql
INNER JOIN Address
```

This removes people without addresses.

---

❌ Joining on the wrong column

```sql
Person.personId = Address.addressId
```

Incorrect.

---

❌ Forgetting the ON clause

Every JOIN requires a matching condition.

---

# Key Concepts Learned

- SELECT
- FROM
- LEFT JOIN
- ON
- Primary Key
- Foreign Key
- NULL values
- One-to-One Relationship

---

# What I Learned

- Difference between INNER JOIN and LEFT JOIN.
- How SQL combines data from multiple tables.
- Why choosing the correct JOIN matters.
- How NULL values appear when no matching record exists.
- How foreign keys connect related tables.

---

# LeetCode Submission

Status

✅ Accepted

Runtime

268 ms

Memory

0.00 MB

Language

PostgreSQL

Test Cases Passed

8 / 8

---

# Revision Notes

Remember:

- Need all rows from left table → LEFT JOIN
- Need only matching rows → INNER JOIN
- Match tables using ON
- Foreign keys connect related tables

---

# SQL Keywords Used

- SELECT
- FROM
- LEFT JOIN
- ON

---

# Tags

SQL • PostgreSQL • Joins • Database • LeetCode Easy