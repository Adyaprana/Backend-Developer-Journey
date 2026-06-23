# Day 22 - LeetCode #28: Find the Index of the First Occurrence in a String

# Overview

Today I solved **LeetCode #28 - Find the Index of the First Occurrence in a String**.

This problem helped me understand:

* String Traversal
* String Slicing
* Sliding Window Technique
* Pattern Matching
* Brute Force String Search

The goal is to find the first index where a target string (`needle`) appears inside another string (`haystack`).

---

# Problem Statement

Given two strings:

```python
haystack
needle
```

Return the index of the first occurrence of `needle` in `haystack`.

If `needle` is not part of `haystack`, return:

```python
-1
```

---

# Example 1

Input:

```python
haystack = "sadbutsad"
needle = "sad"
```

Output:

```python
0
```

Explanation:

```text
s a d b u t s a d
^
```

The first occurrence of `"sad"` starts at index:

```python
0
```

---

# Example 2

Input:

```python
haystack = "leetcode"
needle = "leeto"
```

Output:

```python
-1
```

Explanation:

```text
"leeto"
```

does not exist inside:

```text
"leetcode"
```

---

# Example 3

Input:

```python
haystack = "uytfleetcode"
needle = "leet"
```

Output:

```python
4
```

Explanation:

```text
u y t f l e e t c o d e
        ^
```

The substring `"leet"` starts at index:

```python
4
```

---

# Constraints

```text
1 <= haystack.length, needle.length <= 10⁴
haystack and needle consist of lowercase English characters.
```

---

# Understanding the Problem

Think of:

```python
haystack = "uytfleetcode"
needle = "leet"
```

We need to slide through the string and check:

```text
uytf
ytfl
tfle
flee
leet
```

The first time we find:

```text
leet
```

we return its starting position.

---

# My First Attempt

Initially I tried:

```python
if needle in haystack:
    return i
```

inside a loop.

The problem was:

```python
haystack = "hello"
needle = "ll"
```

The code would return:

```python
0
```

because:

```python
"ll" in "hello"
```

is True.

But the correct answer is:

```python
2
```

because `"ll"` starts at index 2.

---

# Approach 1: Built-in Methods

Python provides:

```python
find()
```

Example:

```python
haystack = "hello"
needle = "ll"

print(haystack.find(needle))
```

Output:

```python
2
```

If not found:

```python
-1
```

---

# Code

```python
class Solution(object):

    def strStr(self, haystack, needle):

        return haystack.find(needle)
```

---

# Complexity

Time Complexity:

```text
O(n)
```

Space Complexity:

```text
O(1)
```

---

# Why We Usually Don't Use This In Interviews

Because the interviewer wants to test:

```text
String Traversal
Logic Building
Pattern Matching
```

not library functions.

---

# Approach 2: Sliding Window (Manual Search)

## Thought Process

Take a window of length:

```python
len(needle)
```

and slide it through the string.

Compare each window with:

```python
needle
```

---

# My Accepted Solution

```python
class Solution(object):

    def strStr(self, haystack, needle):

        if needle not in haystack:
            return -1

        for i in range(len(haystack)):

            if haystack[i:i+len(needle)] == needle:
                return i
```

---

# Improved Version

The first check is actually unnecessary.

We can simply do:

```python
class Solution(object):

    def strStr(self, haystack, needle):

        for i in range(len(haystack) - len(needle) + 1):

            if haystack[i:i+len(needle)] == needle:
                return i

        return -1
```

This is the version commonly used in interviews.

---

# Dry Run

Input:

```python
haystack = "uytfleetcode"
needle = "leet"
```

Needle length:

```python
4
```

---

## i = 0

Window:

```python
haystack[0:4]
```

Result:

```python
"uytf"
```

Compare:

```python
"uytf" == "leet"
```

False.

---

## i = 1

Window:

```python
"ytfl"
```

False.

---

## i = 2

Window:

```python
"tfle"
```

False.

---

## i = 3

Window:

```python
"flee"
```

False.

---

## i = 4

Window:

```python
"leet"
```

Compare:

```python
"leet" == "leet"
```

True.

Return:

```python
4
```

---

# Sliding Window Visualization

```text
haystack = "uytfleetcode"
needle   = "leet"
```

Window movement:

```text
uytf
 ytfl
  tfle
   flee
    leet  <- Found
```

Return:

```python
4
```

---

# Why This Works

The window size is always:

```python
len(needle)
```

For every position:

```python
i
```

we compare:

```python
haystack[i:i+len(needle)]
```

with:

```python
needle
```

If they match:

```python
return i
```

Otherwise continue.

---

# Complexity Analysis

## Sliding Window Solution

### Time Complexity

```text
O((n-m+1) * m)
```

Where:

```text
n = len(haystack)
m = len(needle)
```

For each starting position we may compare up to:

```text
m
```

characters.

Simplified:

```text
O(n*m)
```

---

### Space Complexity

```text
O(1)
```

Ignoring Python slice internals.

---

# Comparison of Approaches

| Approach       | Time   | Space |
| -------------- | ------ | ----- |
| find()         | O(n)   | O(1)  |
| Sliding Window | O(n*m) | O(1)  |

---

# Concepts Learned

During this problem I learned:

* String Traversal
* String Slicing
* Sliding Window
* Pattern Matching
* Substring Search
* Time Complexity Analysis
* Space Complexity Analysis

---

# Interview Pattern

This problem introduces:

```text
Fixed Size Sliding Window
```

The window size is:

```python
len(needle)
```

and moves:

```text
0
1
2
3
...
```

through the string.

This pattern appears in many advanced string problems.

---

# Results

Problem Solved:

**LeetCode #28 - Find the Index of the First Occurrence in a String**

Approaches Learned:

* Built-in find() ✅
* Sliding Window Search ✅

Status:

* Accepted on LeetCode ✅
* Passed All Test Cases ✅

---

# Reflection

The biggest lesson from this problem was:

> Finding whether a string exists is different from finding where it exists.

Using:

```python
needle in haystack
```

only tells us:

```text
True / False
```

but does not provide the index.

The Sliding Window approach taught me how to manually search for a pattern inside a larger string and return its starting position.

This problem also introduced the Fixed Size Sliding Window technique, which is a very common interview pattern.
