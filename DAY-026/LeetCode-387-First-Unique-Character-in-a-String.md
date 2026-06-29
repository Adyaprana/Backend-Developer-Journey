# Day 24 - LeetCode #387: First Unique Character in a String

# Overview

Today I solved **LeetCode #387 - First Unique Character in a String**.

This problem teaches one of the most important interview patterns:

```text
HashMap / Frequency Counter
```

The goal is to find the index of the first character that appears exactly once in a string.

---

# Problem Statement

Given a string:

```python
s = "leetcode"
```

Return the index of the first non-repeating character.

If every character repeats:

```python
return -1
```

---

# Example 1

Input:

```python
s = "leetcode"
```

Output:

```python
0
```

Explanation:

```text
l -> 1 time
e -> 3 times
t -> 1 time
c -> 1 time
o -> 1 time
d -> 1 time
```

The first unique character is:

```text
l
```

Index:

```python
0
```

---

# Example 2

Input:

```python
s = "loveleetcode"
```

Output:

```python
2
```

Explanation:

```text
l -> 2
o -> 2
v -> 1
e -> 4
t -> 1
c -> 1
d -> 1
```

First unique character:

```text
v
```

Index:

```python
2
```

---

# Example 3

Input:

```python
s = "aabb"
```

Output:

```python
-1
```

Explanation:

```text
a -> 2
b -> 2
```

No unique character exists.

---

# Constraints

```text
1 <= s.length <= 10⁵
s consists of lowercase English letters.
```

---

# Understanding the Problem

We need to find:

```text
The first character
whose frequency is exactly 1.
```

Important:

```text
Return INDEX
not the character itself.
```

Example:

```python
s = "leetcode"
```

Output:

```python
0
```

NOT:

```python
"l"
```

---

# Approach 1: Brute Force (Nested Loops)

# Intuition

For every character:

```text
Count how many times it appears.
```

If frequency becomes:

```text
1
```

then return its index.

---

# Algorithm

For every character:

1. Scan the entire string.
2. Count occurrences.
3. If count equals 1:
   return its index.
4. If no unique character exists:
   return -1.

---

# Code

```python
class Solution(object):

    def firstUniqChar(self, s):

        for i in range(len(s)):

            count = 0

            for j in range(len(s)):

                if s[i] == s[j]:
                    count += 1

            if count == 1:
                return i

        return -1
```

---

# Dry Run

Input:

```python
s = "leetcode"
```

---

## i = 0

Character:

```python
'l'
```

Inner loop:

```text
l == l -> count = 1
l == e -> no
l == e -> no
l == t -> no
l == c -> no
l == o -> no
l == d -> no
l == e -> no
```

Final:

```python
count = 1
```

Return:

```python
0
```

---

# Complexity Analysis

Time Complexity:

```text
O(n²)
```

Space Complexity:

```text
O(1)
```

---

# Why Brute Force Is Slow

For every character:

```text
n
```

we scan:

```text
n
```

characters again.

Result:

```text
n × n = O(n²)
```

For large strings:

```text
Very Slow
```

---

# Approach 2: HashMap / Frequency Counter (Optimal)

# Intuition

Instead of counting repeatedly:

```text
Count every character once.
```

Store frequencies inside a dictionary.

Then scan the string again and find the first character whose frequency is:

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
Find first character with frequency 1.
```

Return its index.

---

# Accepted Solution (Your Solution)

```python
class Solution(object):

    def firstUniqChar(self, s):

        count = {}

        for char in s:
            count[char] = count.get(char, 0) + 1

        for i in range(len(s)):

            if count[s[i]] == 1:
                return i

        return -1
```

---

# Dry Run

Input:

```python
s = "leetcode"
```

---

# Pass 1: Build Frequency Dictionary

Start:

```python
{}
```

Read:

```python
'l'
```

Dictionary:

```python
{'l':1}
```

Read:

```python
'e'
```

Dictionary:

```python
{'l':1,'e':1}
```

Read second:

```python
'e'
```

Dictionary:

```python
{'l':1,'e':2}
```

Continue...

Final:

```python
{
'l':1,
'e':3,
't':1,
'c':1,
'o':1,
'd':1
}
```

---

# Pass 2: Find First Unique Character

Check:

```python
i = 0
```

Character:

```python
'l'
```

Frequency:

```python
count['l']
```

Result:

```python
1
```

Unique.

Return:

```python
0
```

---

# Visualization

String:

```text
l e e t c o d e
0 1 2 3 4 5 6 7
```

Frequency Map:

```text
l -> 1
e -> 3
t -> 1
c -> 1
o -> 1
d -> 1
```

First frequency equal to:

```text
1
```

occurs at:

```text
index 0
```

---

# Why This Works

The first loop calculates:

```text
Frequency of every character.
```

The second loop preserves:

```text
Original order.
```

Therefore:

```text
First unique character is found correctly.
```

---

# Complexity Analysis

## Time Complexity

Pass 1:

```text
O(n)
```

Pass 2:

```text
O(n)
```

Total:

```text
O(n)
```

---

## Space Complexity

Dictionary stores character counts.

```text
O(k)
```

Where:

```text
k = number of distinct characters
```

For lowercase English letters:

```text
At most 26
```

Often treated as:

```text
O(1)
```

---

# Comparison of Approaches

| Approach    | Time  | Space |
| ----------- | ----- | ----- |
| Brute Force | O(n²) | O(1)  |
| HashMap     | O(n)  | O(k)  |

---

# Why HashMap Is Better

Brute Force:

```text
Count repeatedly.
```

HashMap:

```text
Count once.
Reuse many times.
```

This reduces:

```text
O(n²)
```

to:

```text
O(n)
```

---

# Interview Pattern

This problem teaches:

```text
HashMap / Frequency Counter
```

The same pattern appears in:

* LeetCode #242 Valid Anagram
* LeetCode #383 Ransom Note
* LeetCode #169 Majority Element
* LeetCode #389 Find the Difference
* LeetCode #1 Two Sum

---

# Concepts Learned

* Strings
* Dictionaries
* HashMap
* Frequency Counting
* Nested Loops
* Time Complexity Analysis
* Space Complexity Analysis

---

# Results

Problem Solved:

**LeetCode #387 - First Unique Character in a String**

Approaches Learned:

* Brute Force (Nested Loops) ✅
* HashMap Frequency Counter ✅

Status:

* Accepted on LeetCode ✅
* Passed All Test Cases ✅

---

# Reflection

The biggest lesson from this problem was:

> If you need to repeatedly count occurrences, a HashMap can save huge amounts of time.

Instead of counting every character again and again:

```text
Count once.
Store it.
Reuse it.
```

This transforms an O(n²) solution into an O(n) solution and introduces one of the most important interview patterns: Frequency Counting using HashMaps.
