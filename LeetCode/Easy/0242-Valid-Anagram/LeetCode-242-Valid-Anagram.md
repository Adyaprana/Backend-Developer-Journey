# Day 16 - LeetCode #242: Valid Anagram

## Overview

Today I solved **LeetCode #242 - Valid Anagram** and learned how to determine whether two strings are anagrams of each other.

During this problem, I explored:

1. Brute Force (Theoretical Only)
2. Sorting Approach
3. Frequency Counting using HashMap (Optimal)

This problem introduced a very important interview pattern:

```text
Character → Count
```

which is commonly known as **Frequency Counting**.

---

# Problem Statement

Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.

An Anagram is a word or phrase formed by rearranging the letters of another word, using all the original letters exactly once.

---

## Example 1

### Input

```python
s = "listen"
t = "silent"
```

### Output

```python
True
```

### Explanation

Both strings contain:

```text
l i s t e n
```

with the same frequency.

Only the order is different.

---

## Example 2

### Input

```python
s = "rat"
t = "car"
```

### Output

```python
False
```

### Explanation

The characters are different.

---

# Constraints

```text
1 <= s.length, t.length <= 5 × 10⁴
```

This means:

```text
Minimum Length = 1
Maximum Length = 50,000
```

---

# Understanding the Problem

Two strings are Anagrams if:

* They contain the same characters.
* Each character appears the same number of times.
* Order does not matter.

Example:

```text
listen
silent
```

Both contain:

```text
l → 1
i → 1
s → 1
t → 1
e → 1
n → 1
```

Therefore:

```text
True
```

---

# Approach 1: Brute Force (Theoretical Only)

## Idea

Generate every possible arrangement (permutation) of the first string and check whether the second string exists among those permutations.

Example:

```text
s = "abc"
```

Possible permutations:

```text
abc
acb
bac
bca
cab
cba
```

If:

```text
t = "cab"
```

Then:

```text
True
```

---

## Why I Did Not Implement This Approach

The number of permutations grows extremely fast.

Example:

```text
Length = 3
Permutations = 6
```

```text
Length = 10
Permutations = 3,628,800
```

The problem allows strings up to:

```text
50,000 characters
```

Generating permutations becomes impossible.

Therefore, this approach is not practical.

---

## Complexity

Time Complexity:

```text
O(n!)
```

Space Complexity:

```text
O(n!)
```

---

# Approach 2: Sorting

## Key Idea

If two strings are anagrams, then after sorting them alphabetically they should become identical.

Example:

```text
listen
silent
```

After sorting:

```text
eilnst
eilnst
```

Both strings become the same.

Therefore:

```text
True
```

---

## My Sorting Solution

```python
class Solution(object):
    def isAnagram(self, s, t):

        if len(s) != len(t):
            return False

        s = sorted(s)
        t = sorted(t)

        if s == t:
            return True

        return False
```

---

## Dry Run

### Input

```python
s = "listen"
t = "silent"
```

Length Check:

```text
6 == 6
```

Continue.

Sort:

```text
s → eilnst
t → eilnst
```

Compare:

```text
eilnst == eilnst
```

Result:

```python
True
```

---

## Another Example

### Input

```python
s = "rat"
t = "car"
```

Sort:

```text
art
acr
```

Compare:

```text
art != acr
```

Result:

```python
False
```

---

## Complexity

Time Complexity:

```text
O(n log n)
```

Space Complexity:

```text
O(n)
```

---

## What I Learned

* How sorting can simplify comparisons.
* Why checking string lengths first is useful.
* How to compare sorted strings directly.
* How sorting can replace complicated comparisons.

---

# Approach 3: Frequency Counting (HashMap) - Optimal

## Key Idea

Instead of sorting, count how many times each character appears.

Dictionary format:

```text
character → frequency
```

Example:

```text
a → 2
b → 1
```

---

## Thought Process

For every character in `s`:

```text
Increase count
```

For every character in `t`:

```text
Decrease count
```

At the end:

If every frequency becomes:

```text
0
```

Then the strings are anagrams.

Otherwise:

```text
False
```

---

## Example

### Input

```python
s = "aab"
t = "aba"
```

Process `s`

```text
a → 1
a → 2
b → 1
```

Dictionary:

```text
a → 2
b → 1
```

---

Process `t`

```text
a → 1
b → 0
a → 0
```

Dictionary:

```text
a → 0
b → 0
```

All values become:

```text
0
```

Result:

```python
True
```

---

## My Optimal Solution

```python
class Solution(object):
    def isAnagram(self, s, t):

        seen = {}

        if len(s) != len(t):
            return False

        for char in s:
            seen[char] = seen.get(char, 0) + 1

        for char in t:
            seen[char] = seen.get(char, 0) - 1

        for count in seen.values():
            if count != 0:
                return False

        return True
```

---

## Dry Run

### Input

```python
s = "listen"
t = "silent"
```

After processing `s`:

```text
l → 1
i → 1
s → 1
t → 1
e → 1
n → 1
```

After processing `t`:

```text
l → 0
i → 0
s → 0
t → 0
e → 0
n → 0
```

All counts are:

```text
0
```

Result:

```python
True
```

---

## Complexity

Time Complexity:

```text
O(n)
```

Space Complexity:

```text
O(n)
```

---

# Comparison of All Approaches

| Approach                     | Time Complexity | Space Complexity |
| ---------------------------- | --------------- | ---------------- |
| Brute Force                  | O(n!)           | O(n!)            |
| Sorting                      | O(n log n)      | O(n)             |
| Frequency Counting (HashMap) | O(n)            | O(n)             |

---

# Concepts Learned

During this problem I learned:

* Strings
* Sorting
* Dictionaries
* HashMaps
* Frequency Counting
* Character Counting
* Time Complexity
* Space Complexity
* Anagrams
* Optimization Techniques

---

# Results

Problem Solved:

**LeetCode #242 - Valid Anagram**

Approaches Learned:

* Brute Force (Theory) ✅
* Sorting ✅
* HashMap / Frequency Counting ✅

Status:

* Accepted on LeetCode ✅
* Understood Sorting Approach ✅
* Understood Frequency Counting Pattern ✅

---

# Reflection

This problem taught me an important lesson:

> Instead of comparing positions, compare frequencies.

I first understood why a brute-force permutation approach was impractical.

Then I solved the problem using sorting and successfully got an Accepted submission.

Finally, I learned the optimal HashMap solution using frequency counting.

This introduced one of the most important DSA patterns:

```text
Character → Count
```

which is used in many interview questions involving strings, HashMaps, and frequency analysis.
