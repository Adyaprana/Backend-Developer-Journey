# Day 19 - LeetCode #14: Longest Common Prefix

## Overview

Today I solved **LeetCode #14 - Longest Common Prefix**.

This problem helped me understand:

* String manipulation
* Prefix matching
* Horizontal Scanning
* Vertical Scanning
* Character-by-character comparison
* Time and Space Complexity analysis

The goal is to find the longest common starting substring shared among all strings in the array.

---

# Problem Statement

Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string.

---

## Example 1

Input:

```python
strs = ["flower","flow","flight"]
```

Output:

```python
"fl"
```

Explanation:

```text
flower
flow
flight
```

Common characters:

```text
f
l
```

At index 2:

```text
flower -> o
flow   -> o
flight -> i
```

Mismatch occurs.

Answer:

```text
fl
```

---

## Example 2

Input:

```python
strs = ["dog","racecar","car"]
```

Output:

```python
""
```

Explanation:

There is no common prefix among all strings.

---

# Constraints

```text
1 <= strs.length <= 200
0 <= strs[i].length <= 200
```

Strings consist of lowercase English letters.

---

# Understanding the Problem

We need to find the common beginning part of every string.

Example:

```python
strs = ["interview","internet","internal"]
```

Common prefix:

```text
inter
```

Because:

```text
interview
internet
internal
```

All begin with:

```text
inter
```

---

# Approach 1: Horizontal Scanning

## Thought Process

Start with the first (or shortest) string as the prefix.

Compare the prefix with every other word.

If the current word does not start with the prefix:

```text
Remove the last character
Check again
```

Keep shrinking until the prefix matches.

---

## My Solution

```python
class Solution(object):
    def longestCommonPrefix(self, strs):

        if not strs:
            return ""

        strs.sort(key=len)

        prefix = strs[0]

        for word in strs:

            while not word.startswith(prefix):

                prefix = prefix[:-1]

                if not prefix:
                    return ""

        return prefix
```

---

# Dry Run (Horizontal Scanning)

Input:

```python
strs = ["flower","flow","flight"]
```

After sorting:

```python
["flow","flower","flight"]
```

Shortest word:

```python
prefix = "flow"
```

---

Compare:

```python
word = "flower"
```

Check:

```python
"flower".startswith("flow")
```

Result:

```python
True
```

No changes.

---

Compare:

```python
word = "flight"
```

Check:

```python
"flight".startswith("flow")
```

Result:

```python
False
```

Shrink:

```text
flow
flo
```

Check again:

```python
"flight".startswith("flo")
```

False.

Shrink:

```text
fl
```

Check again:

```python
"flight".startswith("fl")
```

True.

Final prefix:

```python
"fl"
```

Return:

```python
"fl"
```

---

# Example With No Common Prefix

Input:

```python
strs = ["dog","racecar","car"]
```

After sorting:

```python
["dog","car","racecar"]
```

Prefix:

```python
"dog"
```

Compare with:

```python
"car"
```

Shrink:

```text
dog
do
d
""
```

Prefix becomes empty.

Return:

```python
""
```

---

# Time Complexity (Horizontal Scanning)

Sorting:

```text
O(n log n)
```

Prefix shrinking and comparisons:

```text
O(S)
```

Where:

```text
S = total number of characters
```

Overall:

```text
O(n log n + S)
```

---

# Space Complexity

```text
O(1)
```

No extra data structures are used.

---

# Approach 2: Vertical Scanning

## Thought Process

Instead of shrinking a prefix:

Check every character position across all words.

Example:

```python
strs = ["flower","flow","flight"]
```

Check:

```text
Index 0
Index 1
Index 2
...
```

The first mismatch stops the process.

---

# Vertical Scanning Code

```python
class Solution(object):
    def longestCommonPrefix(self, strs):

        if not strs:
            return ""

        shortest = min(strs, key=len)

        for i in range(len(shortest)):

            char = shortest[i]

            for word in strs:

                if word[i] != char:
                    return shortest[:i]

        return shortest
```

---

# Dry Run (Vertical Scanning)

Input:

```python
strs = ["flower","flow","flight"]
```

Shortest:

```python
"flow"
```

---

## Index 0

```text
flower -> f
flow   -> f
flight -> f
```

Match.

---

## Index 1

```text
flower -> l
flow   -> l
flight -> l
```

Match.

---

## Index 2

```text
flower -> o
flow   -> o
flight -> i
```

Mismatch.

Return:

```python
shortest[:2]
```

Result:

```python
"fl"
```

---

# Complexity (Vertical Scanning)

Time Complexity:

```text
O(S)
```

Where:

```text
S = total characters in all strings
```

Space Complexity:

```text
O(1)
```

---

# Comparison of Approaches

| Approach            | Time           | Space |
| ------------------- | -------------- | ----- |
| Horizontal Scanning | O(n log n + S) | O(1)  |
| Vertical Scanning   | O(S)           | O(1)  |

---

# Why My Horizontal Scanning Solution Works

The key insight is:

```text
Every common prefix must be a prefix of the shortest string.
```

By starting with the shortest word:

```python
prefix = strs[0]
```

and repeatedly removing:

```python
prefix = prefix[:-1]
```

we eventually find the longest prefix shared by all strings.

---

# Concepts Learned

During this problem I learned:

* String Manipulation
* Prefix Matching
* Horizontal Scanning
* Vertical Scanning
* Character-by-Character Comparison
* String Slicing
* startswith()
* Time Complexity Analysis
* Space Complexity Analysis

---

# Results

Problem Solved:

**LeetCode #14 - Longest Common Prefix**

Approaches Learned:

* Horizontal Scanning ✅
* Vertical Scanning ✅

Status:

* Accepted on LeetCode ✅
* Passed All Test Cases ✅

---

# Reflection

The biggest lesson from this problem was:

> A common prefix does not need to be equal to the entire word.

For example:

```python
prefix = "fl"
word = "flight"
```

Even though:

```python
"fl" != "flight"
```

The word still begins with:

```python
"fl"
```

which makes it a valid prefix.

I also learned two common interview patterns:

1. Horizontal Scanning
2. Vertical Scanning

and understood how each approach solves the same problem in a different way.
