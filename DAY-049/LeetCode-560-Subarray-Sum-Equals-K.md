# LeetCode #560 — Subarray Sum Equals K
---

# Problem Statement

Given an integer array `nums` and an integer `k`, return **the total number of continuous subarrays whose sum equals `k`.**

A **subarray** is a contiguous (continuous) part of an array.

---

# Example 1

```text
Input

nums = [1,1,1]

k = 2

Output

2
```

### Explanation

The valid subarrays are

```text
[1,1]   (Index 0 → 1)

[1,1]   (Index 1 → 2)
```

Therefore,

```text
Answer = 2
```

---

# Example 2

```text
Input

nums = [1,2,3]

k = 3

Output

2
```

### Explanation

```text
[1,2]

↓

3

----------------

[3]

↓

3
```

Answer

```text
2
```

---

# Constraints

```text
1 <= nums.length <= 20,000

-1000 <= nums[i] <= 1000

-10⁷ <= k <= 10⁷
```

---

# Understanding the Problem

The question is **NOT** asking

```text
Find one subarray
```

It is asking

```text
Count ALL subarrays

whose sum is exactly k.
```

---

Suppose

```text
nums

[1,2,3]
```

All possible subarrays are

```text
[1]

Sum = 1

----------------

[1,2]

Sum = 3 ✅

----------------

[1,2,3]

Sum = 6

----------------

[2]

Sum = 2

----------------

[2,3]

Sum = 5

----------------

[3]

Sum = 3 ✅
```

Answer

```text
2
```

---

# What is a Subarray?

Many beginners confuse

```text
Subarray

and

Subset
```

They are NOT the same.

---

## Subarray

A subarray is **continuous**.

Example

```text
nums

[1,2,3]
```

Valid

```text
[1]

[2]

[3]

[1,2]

[2,3]

[1,2,3]
```

Invalid

```text
[1,3]
```

because

```text
2

is skipped.
```

---

## Subset

A subset allows skipping elements.

Example

```text
[1,3]
```

is a subset,

but NOT a subarray.

---

# Important Observations

When solving this problem,

think about

```text
Where does the subarray start?

Where does it end?
```

Example

```text
nums

[1,2,3]
```

Start from

```text
Index 0
```

Possible subarrays

```text
[1]

↓

[1,2]

↓

[1,2,3]
```

---

Start from

```text
Index 1
```

Possible subarrays

```text
[2]

↓

[2,3]
```

---

Start from

```text
Index 2
```

Possible subarrays

```text
[3]
```

Notice the pattern.

```text
Choose Starting Index

↓

Keep Expanding Towards Right
```

This immediately suggests

```text
Two Loops
```

---

# Brute Force Approach

The simplest solution is

Choose every possible starting index.

For every starting index,

keep extending the ending index,

while maintaining a running sum.

Every time

```text
Running Sum == k
```

increase the answer.

---

# Algorithm

## Step 1

Choose every possible

```text
Start Index
```

---

## Step 2

Initialize

```text
current_sum = 0
```

---

## Step 3

Expand the subarray towards the right.

```text
current_sum += nums[end]
```

---

## Step 4

If

```text
current_sum == k
```

increase

```text
count
```

---

## Step 5

Repeat for every starting index.

---

# Brute Force Code

```python
class Solution(object):

    def subarraySum(self, nums, k):

        count = 0

        for start in range(len(nums)):

            current_sum = 0

            for end in range(start, len(nums)):

                current_sum += nums[end]

                if current_sum == k:

                    count += 1

        return count
```

---

# Dry Run

Input

```text
nums

[1,2,3]

k = 3
```

Initially

```text
count = 0
```

---

## Start = 0

```text
current_sum = 0
```

Add

```text
1

↓

1
```

Not equal.

---

Extend

```text
1+2

↓

3
```

Equal

```text
count = 1
```

---

Extend

```text
1+2+3

↓

6
```

Not equal.

---

## Start = 1

Reset

```text
current_sum = 0
```

Add

```text
2
```

Not equal.

---

Extend

```text
2+3

↓

5
```

Not equal.

---

## Start = 2

Reset

```text
current_sum = 0
```

Add

```text
3

↓

3
```

Equal

```text
count = 2
```

Finished.

Answer

```text
2
```

---

# Time Complexity

Outer Loop

```text
O(n)
```

Inner Loop

```text
O(n)
```

Overall

```text
O(n²)
```

---

# Space Complexity

```text
O(1)
```

No extra data structure is used.

---

# Why Does This Get TLE?

Constraints

```text
n ≤ 20,000
```

Worst Case

```text
20,000 × 20,000

=

400,000,000
```

Nearly

```text
400 Million

Operations
```

Python cannot execute this within the time limit.

So although the algorithm is

```text
Correct
```

it is

```text
Too Slow.
```

---

# What Needs to be Improved?

Notice something.

For every starting index,

we recalculate many sums.

Example

```text
[1]

↓

[1,2]

↓

[1,2,3]
```

Then again

```text
[2]

↓

[2,3]
```

Lots of repeated work.

Can we somehow

```text
Reuse

Previously Calculated Sums?
```

That question leads us directly to

```text
Prefix Sum.
```

---

# Pattern Explanation

This problem belongs to one of the most important interview patterns.

```text
Running Sum

↓

Prefix Sum

↓

Need = Prefix - k

↓

HashMap

↓

O(n)
```

If you've already solved

- Running Sum of 1D Array (#1480)
- Range Sum Query - Immutable (#303)

then this problem is the next natural step.

---

# Connection With Previous Problems

### Problem 1480

Learned

```text
Running Sum
```

---

### Problem 303

Learned

```text
Prefix Sum

Range Query

prefix[right]

-

prefix[left-1]
```

---

### Problem 560

New Question

Instead of asking

```text
Find the Sum
```

It asks

```text
How many previous Prefix Sums

can create

the current subarray?
```

This is the biggest idea behind the optimal solution.

---

# Key Insight Before the Optimal Solution

Suppose

Current Prefix Sum is

```text
10
```

and

```text
k = 3
```

We need

```text
Current Prefix

-

Previous Prefix

=

k
```

So

```text
10

-

Previous Prefix

=

3
```

Therefore

```text
Previous Prefix

=

7
```

Now ask yourself

```text
Have I already seen

Prefix Sum = 7 ?
```

If YES,

then a valid subarray exists.

This single observation converts

```text
O(n²)

↓

O(n)
```

---

# Interview Questions

### Q1

What is the difference between

```text
Subarray

and

Subset?
```

---

### Q2

Why is the brute force solution

```text
O(n²)?
```

---

### Q3

Why does the brute force solution get

```text
Time Limit Exceeded?
```

---

### Q4

Which previously learned concept can help optimize this problem?

Answer

```text
Prefix Sum
```

---

### Q5

Which data structure can store previously seen Prefix Sums efficiently?

Answer

```text
HashMap
```

---

# What I Learned

- A subarray must always be continuous.
- Choosing a starting index and expanding to the right naturally gives the brute-force solution.
- Maintaining a running sum is better than repeatedly calling `sum()`.
- The brute-force algorithm is correct but too slow for large inputs.
- Prefix Sum is the key observation needed to optimize the solution.
- This problem is a direct continuation of Running Sum (#1480) and Range Sum Query (#303).

---

# Optimal Approach — Prefix Sum + HashMap

This is the **optimal interview solution**.

Instead of checking every possible subarray,

we reuse the Prefix Sum idea and store previously seen Prefix Sums inside a HashMap.

This reduces the time complexity from

```text
O(n²)

↓

O(n)
```

---

# Intuition

Suppose

```text
nums

[1,2,3]
```

Prefix Sums become

```text
Index

0    1    2

↓

1    3    6
```

Suppose the current Prefix Sum is

```text
6
```

and

```text
k = 5
```

Need

```text
Current Prefix

-

Previous Prefix

=

k
```

Substitute

```text
6

-

Previous Prefix

=

5
```

Therefore

```text
Previous Prefix

=

1
```

Question

```text
Have we already seen

Prefix Sum = 1 ?
```

If YES,

then the subarray between those two Prefix Sums has a sum of exactly

```text
5
```

Instead of checking every subarray,

we simply check

```text
Need = Prefix - k
```

inside a HashMap.

---

# The Biggest Observation

Every time we calculate

```text
Current Prefix Sum
```

we only need to know

```text
Have I seen

Current Prefix - k

before?
```

If YES,

then one or more valid subarrays exist.

---

# Why Do We Use a HashMap?

A HashMap stores

```text
Prefix Sum

↓

Frequency
```

Example

```text
{

0 : 1,

1 : 2,

3 : 1,

6 : 1

}
```

Meaning

```text
Prefix Sum

0

appeared once.

---------------

Prefix Sum

1

appeared twice.

---------------

Prefix Sum

3

appeared once.
```

HashMap lookup is

```text
O(1)
```

which makes the overall algorithm

```text
O(n)
```

---

# Why Do We Initialize

```python
HashMap = {0:1}
```

This is the most common interview question.

Imagine

```text
nums

[2]

k = 2
```

Initially

```text
Prefix Sum

0
```

Now

```text
Prefix

↓

2
```

Need

```text
2-2

↓

0
```

If

```text
0

is already inside

HashMap
```

then

```text
[2]
```

is counted correctly.

Without

```text
{0:1}
```

we would completely miss every valid subarray starting from

```text
Index 0
```

---

# Why Do We Store Prefix Sum?

Another common interview question.

Suppose

```text
nums

[1,1,1]
```

Current Number

```text
1
```

Current Prefix Sum

```text
3
```

Need

```text
3-2

↓

1
```

Notice

We never ask

```text
Have we seen

Number = 1 ?
```

We ask

```text
Have we seen

Prefix Sum = 1 ?
```

Therefore

we store

```text
Prefix Sum
```

NOT

```text
nums[i]
```

---

# Why Do We Store Frequency?

Suppose

```text
nums

[0,0,0]

k = 0
```

Prefix Sums become

```text
0

0

0

0
```

Notice

Prefix Sum

```text
0
```

appears

multiple times.

If we store

```text
0 : 1
```

every time,

we overwrite the previous value.

Instead,

we store

```text
0 : 4
```

because it appeared four times.

Whenever

```text
Need = 0
```

we immediately know

how many valid subarrays exist.

---

# Algorithm

## Step 1

Initialize

```text
prefix_sum = 0

count = 0

HashMap = {0:1}
```

---

## Step 2

Traverse the array.

---

## Step 3

Update

```text
prefix_sum
```

---

## Step 4

Compute

```text
Need

=

prefix_sum - k
```

---

## Step 5

If

```text
Need

exists

inside HashMap
```

increase

```text
count
```

by

```text
Frequency of Need
```

---

## Step 6

Store the current Prefix Sum

inside the HashMap.

---

## Step 7

Return

```text
count
```

---

# Code

```python
class Solution(object):

    def subarraySum(self, nums, k):

        prefix_sum = 0

        count = 0

        HashMap = {0:1}

        for i in range(len(nums)):

            prefix_sum += nums[i]

            need = prefix_sum - k

            if need in HashMap:

                count += HashMap[need]

            HashMap[prefix_sum] = HashMap.get(prefix_sum, 0) + 1

        return count
```

---

# Complete Dry Run

Input

```text
nums

[1,1,1]

k = 2
```

Initially

```text
prefix_sum = 0

count = 0

HashMap

{

0:1

}
```

---

## Index 0

Number

```text
1
```

Prefix Sum

```text
1
```

Need

```text
1-2

↓

-1
```

Exists?

```text
NO
```

Store

```text
1
```

HashMap

```text
{

0:1,

1:1

}
```

---

## Index 1

Prefix Sum

```text
2
```

Need

```text
2-2

↓

0
```

Exists?

YES

Frequency

```text
1
```

Increase

```text
count

↓

1
```

Store

```text
2
```

HashMap

```text
{

0:1,

1:1,

2:1

}
```

---

## Index 2

Prefix Sum

```text
3
```

Need

```text
3-2

↓

1
```

Exists?

YES

Frequency

```text
1
```

Increase

```text
count

↓

2
```

Store

```text
3
```

HashMap

```text
{

0:1,

1:1,

2:1,

3:1

}
```

Finished.

Answer

```text
2
```

---

# Another Dry Run

Input

```text
nums

[0,0,0]

k = 0
```

Initially

```text
HashMap

{

0:1

}
```

---

Index 0

Need

```text
0
```

Frequency

```text
1
```

Count

```text
1
```

HashMap

```text
0:2
```

---

Index 1

Need

```text
0
```

Frequency

```text
2
```

Count

```text
3
```

HashMap

```text
0:3
```

---

Index 2

Need

```text
0
```

Frequency

```text
3
```

Count

```text
6
```

HashMap

```text
0:4
```

Final Answer

```text
6
```

This example shows why storing **frequency** is essential.

---

# Complexity Analysis

## Time Complexity

One traversal

```text
O(n)
```

HashMap lookup

```text
O(1)
```

Overall

```text
O(n)
```

---

## Space Complexity

HashMap stores Prefix Sums.

Worst case

```text
O(n)
```

---

# Common Mistakes I Made

## Mistake 1

Stored

```python
HashMap[nums[i]]
```

instead of

```python
HashMap[prefix_sum]
```

---

## Mistake 2

Always wrote

```python
count += 1
```

instead of

```python
count += HashMap[need]
```

Need can appear multiple times.

---

## Mistake 3

Forgot

```python
HashMap = {0:1}
```

Without this,

subarrays starting at

```text
Index 0
```

are never counted.

---

## Mistake 4

Stored

```python
HashMap[prefix_sum] = 1
```

This overwrites previous occurrences.

Instead,

increase the frequency.

---

# Pattern Learned

```text
Running Sum

↓

Prefix Sum

↓

Need = Prefix - k

↓

HashMap

↓

Count Frequency

↓

O(n)
```

---

# Interview Questions

### Q1

Why do we initialize

```python
HashMap = {0:1}
```

---

### Q2

Why do we store

```text
Prefix Sum
```

instead of

```text
Current Number?
```

---

### Q3

Why do we store

```text
Frequency
```

instead of only

```text
True / False?
```

---

### Q4

Why is the brute-force solution

```text
O(n²)
```

while the optimal solution is

```text
O(n)?
```

---

### Q5

What is the relationship between

Problem

```text
303

Range Sum Query
```

and

```text
560

Subarray Sum Equals K?
```

Answer

```text
Both are based on Prefix Sum.
```

The only difference is

Problem 560 combines Prefix Sum with a HashMap.

---

# Key Takeaways

- Running Sum evolves into Prefix Sum.
- Prefix Sum combined with a HashMap eliminates nested loops.
- `{0:1}` is required to count subarrays starting from index `0`.
- The HashMap stores **Prefix Sum frequencies**, not array elements.
- The frequency tells us how many valid subarrays end at the current index.
- This is one of the most important Prefix Sum + HashMap patterns for coding interviews.

---



