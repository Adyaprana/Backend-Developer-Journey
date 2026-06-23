# Day 27 - LeetCode #268: Missing Number

# Overview

Today I solved **LeetCode #268 - Missing Number**.

This problem teaches multiple ways of solving the same problem and is an excellent example of how one problem can be optimized step by step.

The goal is to find the only missing number from an array containing distinct numbers from **0 to n**.

---

# Problem Statement

Given an array containing **n distinct numbers** taken from the range:

0 to n

Return the only number missing from the array.

---

# Example 1

Input

```python
nums = [3,0,1]
```

Output

```python
2
```

Explanation

Expected numbers

```
0 1 2 3
```

Array contains

```
3 0 1
```

Missing number

```
2
```

---

# Example 2

Input

```python
nums = [0,1]
```

Output

```python
2
```

---

# Example 3

Input

```python
nums = [9,6,4,2,3,5,7,0,1]
```

Output

```python
8
```

---

# Constraints

```
1 <= nums.length <= 10⁴

0 <= nums[i] <= n

All numbers are unique.
```

---

# Understanding the Problem

If the array length is

```python
9
```

then the numbers should be

```
0 1 2 3 4 5 6 7 8 9
```

One number is missing.

Our task is to find it.

---

# Approach 1 : Brute Force (Linear Search)

# Intuition

Check every number from **0 to n**.

If any number is not found in the array, that must be the missing number.

---

# Algorithm

1. Traverse from 0 to n.
2. Check whether the number exists in the array.
3. Return the first missing number.

---

# Code

```python
class Solution(object):

    def missingNumber(self, nums):

        n = len(nums)

        for i in range(n + 1):

            if i not in nums:
                return i
```

---

# Dry Run

Input

```python
nums = [3,0,1]
```

Check

```
0 ✓

1 ✓

2 ✗
```

Return

```python
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

# Why It Is Slow

Every

```python
i not in nums
```

performs a linear search.

Therefore

```
n × n

=

O(n²)
```

---

# Approach 2 : HashSet

# Intuition

Searching inside a Set takes approximately O(1).

Convert the array into a set first, then perform membership checking.

---

# Code

```python
class Solution(object):

    def missingNumber(self, nums):

        seen = set(nums)

        for i in range(len(nums)+1):

            if i not in seen:
                return i
```

---

# Dry Run

Input

```python
nums = [3,0,1]
```

Convert

```python
{0,1,3}
```

Check

```
0 ✓

1 ✓

2 ✗
```

Return

```python
2
```

---

# Complexity

Time

```
O(n)
```

Space

```
O(n)
```

---

# Approach 3 : Math Formula (Submitted Solution)

# Intuition

The sum of numbers from **0 to n** is known.

Expected Sum

```
n × (n + 1) / 2
```

If we subtract the actual array sum, the remaining value is the missing number.

---

# Algorithm

1. Compute the expected sum.
2. Compute the actual sum.
3. Return

```
Expected − Actual
```

---

# Submitted Solution

```python
class Solution(object):

    def missingNumber(self, nums):

        expected = len(nums) * (len(nums)+1) // 2

        actual = sum(nums)

        return expected - actual
```

---

# Dry Run

Input

```python
nums = [3,0,1]
```

Expected Sum

```
3 × 4 / 2

=

6
```

Actual Sum

```
3+0+1

=

4
```

Difference

```
6−4

=

2
```

Return

```python
2
```

---

# Complexity

Time

```
O(n)
```

Space

```
O(1)
```

---

# Why This Works

The complete range is

```
0 1 2 3
```

Only one number is absent.

Subtracting the actual sum from the expected sum leaves exactly that missing value.

---

# Approach 4 : XOR (Optimal Alternative)

# Intuition

XOR has two important properties

```
a ^ a = 0

a ^ 0 = a
```

If we XOR every expected number with every array element, all matching values cancel out.

Only the missing number remains.

---

# Code

```python
class Solution(object):

    def missingNumber(self, nums):

        result = len(nums)

        for i in range(len(nums)):

            result ^= i

            result ^= nums[i]

        return result
```

---

# Dry Run

Input

```python
nums = [3,0,1]
```

Start

```
result = 3
```

Loop

```
3 ^ 0 ^ 3

^

1 ^ 0

^

2 ^ 1
```

Everything cancels except

```
2
```

Return

```python
2
```

---

# Complexity

Time

```
O(n)
```

Space

```
O(1)
```

---

# Comparison of Approaches

| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n²) | O(1) |
| HashSet | O(n) | O(n) |
| Math Formula | O(n) | O(1) |
| XOR | O(n) | O(1) |

---

# Interview Pattern

This problem teaches four important interview techniques:

- Brute Force Search
- HashSet
- Mathematical Formula
- XOR / Bit Manipulation

---

# Concepts Learned

- Arrays
- Linear Search
- HashSet
- Mathematical Formula
- XOR
- Time Complexity
- Space Complexity

---

# Results

Problem Solved

**LeetCode #268 - Missing Number**

Approaches Learned

- Brute Force ✅
- HashSet ✅
- Math Formula ✅ (Submitted)
- XOR ✅

Status

- Accepted on LeetCode ✅

---

# Reflection

This problem demonstrated how one problem can have multiple valid solutions with different trade-offs.

I first solved it using a Brute Force approach, then improved it using a HashSet. Next, I derived the Mathematical Formula solution using the expected sum concept, and finally understood the XOR approach by learning how duplicate values cancel each other.

The key takeaway was that understanding **why** each optimization works is more valuable than memorizing the final solution.