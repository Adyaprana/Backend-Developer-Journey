# Day 27 - LeetCode #169: Majority Element

# Overview

Today I solved **LeetCode #169 - Majority Element**.

This problem is one of the most famous interview questions because it introduces the **Boyer-Moore Voting Algorithm**, an elegant algorithm that finds the majority element in **O(n) time** and **O(1) space**.

Before learning the optimal algorithm, I first solved the problem using a **HashMap (Frequency Counter)** approach, then learned why Boyer-Moore works.

---

# Problem Statement

Given an integer array `nums`, return the **majority element**.

The majority element is the element that appears **more than ⌊ n / 2 ⌋ times**.

The problem guarantees that the majority element always exists.

---

# Example 1

Input

```python
nums = [3,2,3]
```

Output

```python
3
```

Explanation

```
3 → 2 times
2 → 1 time

3 appears more than n/2 times.
```

---

# Example 2

Input

```python
nums = [2,2,1,1,1,2,2]
```

Output

```python
2
```

Explanation

```
2 → 4 times
1 → 3 times

Length = 7

More than 7//2 = 3

2 appears 4 times.

Therefore,

Answer = 2
```

---

# Constraints

```
1 <= nums.length <= 5 × 10⁴

-10⁹ <= nums[i] <= 10⁹
```

The problem guarantees that a majority element always exists.

---

# Follow-up
```
Can you solve the problem in:
- O(n) time?
- O(1) extra space?
```
The Boyer-Moore Voting Algorithm satisfies both requirements.

---
# Understanding the Problem

Example

```python
nums = [2,2,1,1,1,2,2]
```

Frequency

```
2 → 4

1 → 3
```

The answer is **NOT** the largest number.

The answer is the number having the **highest frequency**.

Therefore,

```
Return 2
```

---

# Approach 1 — Brute Force (Nested Loops)

# Intuition

For every element,

Count how many times it appears in the array.

If its count becomes greater than

```
n // 2
```

return that number.

---

# Algorithm

For every element

```
Count its frequency

If frequency > n//2

Return it
```

---

# Code

```python
class Solution:

    def majorityElement(self, nums):

        n = len(nums)

        for i in range(n):

            count = 0

            for j in range(n):

                if nums[i] == nums[j]:
                    count += 1

            if count > n // 2:
                return nums[i]
```

---

# Dry Run

Input

```python
nums = [2,2,1,1,1,2,2]
```

First element

```
2
```

Count

```
2
2
2
2

count = 4
```

Since

```
4 > 3
```

Return

```
2
```

---

# Complexity

Time Complexity

```
O(n²)
```

Space Complexity

```
O(1)
```

---

# Why Brute Force is Slow

For every element

```
n
```

we again scan

```
n
```

elements.

Total

```
O(n²)
```

This becomes very slow for large arrays.

---

# Approach 2 — HashMap / Frequency Counter

# Intuition

Instead of counting every number repeatedly,

Count every number **once** using a dictionary.

Then simply return the number having the highest frequency.

This was my **first accepted solution**.

---

# Algorithm

Pass 1

```
Build frequency dictionary.
```

Pass 2

```
Find the key having maximum frequency.
```

Return that key.

---

# Accepted Solution (HashMap)

```python
class Solution:

    def majorityElement(self, nums):

        count = {}

        max_count = 0

        majority = 0

        for num in nums:

            count[num] = count.get(num,0)+1

        for key,value in count.items():

            if value > max_count:

                max_count = value

                majority = key

        return majority
```

---

# Dry Run

Input

```python
nums = [2,2,1,1,1,2,2]
```

Pass 1

Dictionary

```
{

2 : 4,

1 : 3

}
```

---

Pass 2

Check

```
2 → 4
```

Current maximum

```
4
```

Majority

```
2
```

Next

```
1 → 3
```

```
3 < 4
```

Ignore.

Return

```
2
```

---

# Visualization

Array

```
2 2 1 1 1 2 2
```

Dictionary

```
2 → 4

1 → 3
```

Maximum frequency

```
4
```

Answer

```
2
```

---

# Why This Works

The HashMap stores

```
Number → Frequency
```

Once frequencies are known,

Finding the largest frequency directly gives the majority element.

---

# Complexity Analysis

Time Complexity

Building Dictionary

```
O(n)
```

Finding Maximum

```
O(n)
```

Overall

```
O(n)
```

Space Complexity

```
O(n)
```

because of the dictionary.

---

# Approach 3 — Boyer-Moore Voting Algorithm (Optimal)

# Intuition

This algorithm does **not** count frequencies.

Instead, it uses the idea of **cancellation**.

Imagine an election where every different number votes against the current candidate.

If two different numbers are seen, they cancel one vote.

Since the majority element appears **more than half of the total elements**, it can never be completely cancelled.

Eventually, only the majority element survives.

This is why the algorithm works.

---

# Understanding the Algorithm

We maintain only two variables.

```python
candidate
votes
```

Initially,

```python
candidate = None
votes = 0
```

For every number:

### Rule 1

If

```python
votes == 0
```

Choose the current number as the new candidate.

Increase votes.

---

### Rule 2

If the current number equals the candidate,

Increase votes.

---

### Rule 3

Otherwise,

Decrease votes.

---

After processing the entire array,

The candidate will always be the majority element.

(LeetCode guarantees that a majority element always exists.)

---

# Why Does Cancellation Work?

Example

```
2 2 2 2 1 3 4
```

Pair one majority element with one different element.

```
2 × 1

2 × 3

2 × 4
```

After cancellation,

```
2
```

still remains.

Since the majority appears more than every other element combined,

It can never disappear completely.

---

# Visual Explanation

Array

```
2 2 1 1 1 2 2
```

Think of cancelling pairs.

```
2 × 1

2 × 1

2 × 1
```

After cancelling,

```
2
```

still remains.

Therefore,

```
2
```

must be the majority element.

---

# Boyer-Moore Voting Algorithm (Submitted Solution)

```python
class Solution:

    def majorityElement(self, nums):

        candidate = None

        votes = 0

        for num in nums:

            if votes == 0:

                candidate = num

                votes = 1

            elif num == candidate:

                votes += 1

            else:

                votes -= 1

        return candidate
```

---

# Dry Run

Input

```python
nums = [3,3,4,2,4,4,2,4,4]
```

Initial

```
Candidate = None

Votes = 0
```

---

Current

```
3
```

Votes are zero.

Choose

```
Candidate = 3

Votes = 1
```

---

Current

```
3
```

Same candidate.

```
Votes = 2
```

---

Current

```
4
```

Different.

```
Votes = 1
```

---

Current

```
2
```

Different.

```
Votes = 0
```

Everything seen so far has cancelled.

---

Current

```
4
```

Votes are zero.

Choose new candidate.

```
Candidate = 4

Votes = 1
```

---

Current

```
4
```

Same.

```
Votes = 2
```

---

Current

```
2
```

Different.

```
Votes = 1
```

---

Current

```
4
```

Same.

```
Votes = 2
```

---

Current

```
4
```

Same.

```
Votes = 3
```

Loop finishes.

Return

```
4
```

Correct.

---

# Another Dry Run

Input

```python
nums = [2,2,1,1,1,2,2]
```

| Current | Candidate | Votes |
|---------|-----------|------:|
|2|2|1|
|2|2|2|
|1|2|1|
|1|2|0|
|1|1|1|
|2|1|0|
|2|2|1|

Return

```
2
```

---

# Why We Don't Change Candidate Immediately

Suppose

```
Candidate = 3

Votes = 1

Current = 2
```

Different number.

Votes become

```
0
```

We **do not** immediately make

```
Candidate = 2
```

Instead,

The next element decides the next candidate.

This is one of the most important ideas behind Boyer-Moore.

---

# Why This Algorithm Is Amazing

Unlike HashMap,

it never stores frequencies.

Instead,

it continuously removes equal numbers of majority and non-majority elements.

Only the true majority survives.

---

# Complexity Analysis

## Brute Force

Time

```
O(n²)
```

Space

```
O(1)
```

---

## HashMap

Time

```
O(n)
```

Space

```
O(n)
```

---

## Boyer-Moore

Time

```
O(n)
```

Space

```
O(1)
```

This is the optimal solution.

---

# Comparison of Approaches

| Approach | Time | Space | Interview |
|-----------|------|-------|-----------|
| Brute Force | O(n²) | O(1) | ❌ |
| HashMap | O(n) | O(n) | ✅ |
| Boyer-Moore | O(n) | O(1) | ⭐ Best |

---

# Interview Notes

Most candidates solve this problem using a HashMap.

A common interview follow-up is:

> "Can you solve it in O(1) extra space?"

The expected answer is:

```
Boyer-Moore Voting Algorithm
```

If the interviewer asks why it works,

explain the **pair cancellation** idea instead of memorizing the code.

---

# Concepts Learned

- Arrays
- HashMap
- Frequency Counter
- Majority Element
- Pair Cancellation
- Boyer-Moore Voting Algorithm
- Time Complexity Analysis
- Space Complexity Analysis

---

# Related Problems

- #136 Single Number
- #217 Contains Duplicate
- #387 First Unique Character in a String
- #229 Majority Element II
- #137 Single Number II

---

# Results

Problem Solved

**LeetCode #169 - Majority Element**

Approaches Learned

- Brute Force ✅
- HashMap Frequency Counter ✅
- Boyer-Moore Voting Algorithm ✅

Final Submitted Solution

✅ Boyer-Moore Voting Algorithm

Status

- Accepted on LeetCode ✅
- Passed All Test Cases ✅

---

# Reflection

This problem taught me that counting frequencies is not always necessary.

Instead of storing every frequency, Boyer-Moore continuously cancels different elements.

Since the majority element appears more than half of the total array, it can never be completely cancelled and is guaranteed to survive.

Learning this algorithm helped me understand one of the most elegant O(n) time and O(1) space interview algorithms.

---

# LeetCode Submission Notes

```markdown
# Intuition

The majority element appears more than n/2 times. We can use the Boyer-Moore Voting Algorithm, which repeatedly cancels out different elements. Since the majority element occurs more than all other elements combined, it will remain as the final candidate.

# Approach

1. Initialize a candidate and a vote counter.
2. If votes become zero, choose the current element as the new candidate.
3. If the current element matches the candidate, increment votes.
4. Otherwise, decrement votes.
5. After one pass, return the candidate.

# Complexity

- Time complexity:
O(n)

- Space complexity:
O(1)
```

---
