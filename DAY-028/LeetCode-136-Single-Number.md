# Day 26 - LeetCode #136: Single Number

# Overview

Today I solved **LeetCode #136 - Single Number**.

This problem introduces:

* HashMap / Frequency Counter
* Counting Occurrences
* Unique Element Detection
* Bit Manipulation (Advanced Follow-Up)

The goal is to find the element that appears exactly once while every other element appears twice.

---

# Problem Statement

Given a non-empty array of integers:

```python
nums = [4,1,2,1,2]
```

Every element appears twice except for one.

Return that single element.

---

# Example 1

Input:

```python
nums = [2,2,1]
```

Output:

```python
1
```

---

# Example 2

Input:

```python
nums = [4,1,2,1,2]
```

Output:

```python
4
```

---

# Example 3

Input:

```python
nums = [1]
```

Output:

```python
1
```

---

# Constraints

```text
1 <= nums.length <= 3 * 10^4
-3 * 10^4 <= nums[i] <= 3 * 10^4
Each element appears twice except one.
```

---

# Understanding the Problem

Input:

```python
[4,1,2,1,2]
```

Frequency:

```text
4 -> 1
1 -> 2
2 -> 2
```

Only:

```text
4
```

appears once.

Therefore:

```python
return 4
```

---

# Approach 1: HashMap / Frequency Counter (Submitted Solution)

# Intuition

Count the frequency of every number.

Then find the number whose frequency is:

```python
1
```

---

# Algorithm

Pass 1:

```text
Build frequency dictionary.
```

Pass 2:

```text
Find value whose frequency equals 1.
```

Return that number.

---

# Submitted & Accepted Solution

```python
class Solution(object):

    def singleNumber(self, nums):

        count = {}

        for n in nums:
            count[n] = count.get(n, 0) + 1

        for key, value in count.items():

            if value == 1:
                return key
```

---

# Dry Run

Input:

```python
nums = [4,1,2,1,2]
```

---

## Pass 1

Start:

```python
{}
```

Read:

```python
4
```

Dictionary:

```python
{4:1}
```

Read:

```python
1
```

Dictionary:

```python
{4:1,1:1}
```

Read:

```python
2
```

Dictionary:

```python
{4:1,1:1,2:1}
```

Read:

```python
1
```

Dictionary:

```python
{4:1,1:2,2:1}
```

Read:

```python
2
```

Dictionary:

```python
{4:1,1:2,2:2}
```

---

## Pass 2

Check:

```python
4 -> 1
```

Condition:

```python
value == 1
```

True.

Return:

```python
4
```

---

# Visualization

```text
Array:

4 1 2 1 2

Frequency Map:

4 -> 1
1 -> 2
2 -> 2

Unique Element:

4
```

---

# Why This Works

The dictionary stores:

```text
Number -> Frequency
```

After counting:

```text
Every duplicate has frequency 2.
Only one number has frequency 1.
```

Return that number.

---

# Complexity Analysis

## Time Complexity

Building HashMap:

```text
O(n)
```

Searching HashMap:

```text
O(n)
```

Total:

```text
O(n)
```

---

## Space Complexity

Dictionary stores frequencies.

```text
O(n)
```

---

# Approach 2: XOR Optimization (Follow-Up)

# Intuition

XOR has two important properties:

```text
a ^ a = 0
a ^ 0 = a
```

Since duplicates appear exactly twice:

```text
They cancel each other.
```

Only the unique element remains.

---

# Code

```python
class Solution(object):

    def singleNumber(self, nums):

        result = 0

        for n in nums:
            result ^= n

        return result
```

---

# Dry Run

Input:

```python
[4,1,2,1,2]
```

Calculation:

```text
4 ^ 1 ^ 2 ^ 1 ^ 2

= 4 ^ (1 ^ 1) ^ (2 ^ 2)

= 4 ^ 0 ^ 0

= 4
```

Return:

```python
4
```

---

# Complexity

Time:

```text
O(n)
```

Space:

```text
O(1)
```

---

# Comparison of Approaches

| Approach | Time | Space |
| -------- | ---- | ----- |
| HashMap  | O(n) | O(n)  |
| XOR      | O(n) | O(1)  |

---

# Interview Pattern

This problem teaches:

```text
Frequency Counting
```

and introduces:

```text
Bit Manipulation
```

The same ideas appear in:

* Contains Duplicate (#217)
* First Unique Character (#387)
* Missing Number (#268)
* Single Number II (#137)

---

# Concepts Learned

* HashMap
* Frequency Counter
* Dictionary Traversal
* Unique Element Search
* XOR Basics
* Time Complexity Analysis

---

# Results

Problem Solved:

**LeetCode #136 - Single Number**

Approaches Learned:

* HashMap Frequency Counter ✅ (Submitted)
* XOR Optimization ✅ (Learned)

Status:

* Accepted on LeetCode ✅

---

# Reflection

The biggest lesson from this problem was:

> Frequency counting is often the easiest way to identify unique elements.

After solving it with a HashMap, I learned an advanced XOR trick that removes the need for extra space and achieves the same result in O(1) space.

This problem served as my introduction to Bit Manipulation concepts.
