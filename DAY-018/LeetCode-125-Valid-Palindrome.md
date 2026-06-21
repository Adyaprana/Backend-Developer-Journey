# Day 16 - LeetCode #125: Valid Palindrome

## Overview

Today I solved **LeetCode #125 - Valid Palindrome** and learned the **Two Pointer** technique.

This was my first problem using two pointers, which is one of the most important patterns in Data Structures and Algorithms.

I also learned how to:

* Remove special characters.
* Ignore spaces.
* Convert uppercase letters to lowercase.
* Compare characters from both ends of a string.

---

# Problem Statement

A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.

Return:

* `True` if the string is a palindrome.
* `False` otherwise.

---

## Example 1

### Input

```python
s = "A man, a plan, a canal: Panama"
```

### Output

```python
True
```

### Explanation

After cleaning:

```text
amanaplanacanalpanama
```

Forward:

```text
amanaplanacanalpanama
```

Backward:

```text
amanaplanacanalpanama
```

Same string.

Therefore:

```python
True
```

---

## Example 2

### Input

```python
s = "race a car"
```

### Output

```python
False
```

### Explanation

After cleaning:

```text
raceacar
```

Reverse:

```text
racaecar
```

Different.

Therefore:

```python
False
```

---

# Constraints

```text
1 <= s.length <= 2 × 10^5
```

The string may contain:

* Uppercase letters
* Lowercase letters
* Numbers
* Spaces
* Special characters

---

# Understanding the Problem

The original string cannot be compared directly.

Example:

```python
"A man, a plan, a canal: Panama"
```

contains:

```text
Spaces
Commas
Colon
Uppercase letters
```

These characters must be ignored.

Therefore:

```python
"A man, a plan, a canal: Panama"
```

becomes:

```text
amanaplanacanalpanama
```

Then we check whether it reads the same forward and backward.

---

# Approach 1: Reverse and Compare

## Key Idea

1. Clean the string.
2. Convert to lowercase.
3. Create a reversed copy.
4. Compare both strings.

---

## Solution

```python
class Solution(object):
    def isPalindrome(self, s):

        cleaned = "".join(char for char in s if char.isalnum())
        cleaned = cleaned.lower()

        reversed_s = cleaned[::-1]

        if cleaned == reversed_s:
            return True

        return False
```

---

## Dry Run

### Input

```python
s = "racecar"
```

Cleaned:

```text
racecar
```

Reverse:

```text
racecar
```

Compare:

```text
racecar == racecar
```

Result:

```python
True
```

---

### Input

```python
s = "hello"
```

Reverse:

```text
olleh
```

Compare:

```text
hello != olleh
```

Result:

```python
False
```

---

## Complexity

### Time Complexity

```text
O(n)
```

### Space Complexity

```text
O(n)
```

Because an additional reversed string is created.

---

## What I Learned

* String slicing.
* Reverse operation.
* String cleaning.
* Case conversion.

---

# Approach 2: Two Pointers (Optimal)

## Key Idea

Instead of creating a reversed copy, compare characters directly from both ends.

Use:

```text
left pointer
right pointer
```

---

## Visual Representation

```text
racecar

left          right
 ↓              ↓
r a c e c a r
```

Compare:

```text
r == r
```

Move:

```text
left += 1
right -= 1
```

---

Next:

```text
  left      right
    ↓         ↓
r a c e c a r
```

Compare:

```text
a == a
```

Move again.

Continue until:

```text
left >= right
```

If no mismatch is found:

```python
True
```

---

## My Two Pointer Solution

```python
class Solution(object):
    def isPalindrome(self, s):

        cleaned = "".join(char for char in s if char.isalnum())
        cleaned = cleaned.lower()

        left = 0
        right = len(cleaned) - 1

        while left < right:

            if cleaned[left] != cleaned[right]:
                return False

            left += 1
            right -= 1

        return True
```

---

## Dry Run

### Input

```python
s = "racecar"
```

Cleaned:

```text
racecar
```

Pointers:

```text
left = 0
right = 6
```

Check:

```text
r == r
```

Move.

```text
a == a
```

Move.

```text
c == c
```

Move.

Eventually:

```text
left >= right
```

No mismatch found.

Result:

```python
True
```

---

### Input

```python
s = "raceacar"
```

Pointers:

```text
r == r
a == a
c == c
e != a
```

Mismatch found.

Result:

```python
False
```

---

## Why This Approach Is Better

Reverse Approach:

```text
Create a new reversed string
Compare
```

Two Pointer Approach:

```text
Compare directly
No reversed copy needed
```

Less memory is used.

---

## Complexity

### Time Complexity

```text
O(n)
```

### Space Complexity

```text
O(n)
```

because we still create the cleaned string.

---

# Comparison of Approaches

| Approach          | Time | Space |
| ----------------- | ---- | ----- |
| Reverse & Compare | O(n) | O(n)  |
| Two Pointers      | O(n) | O(n)  |

---

# Concepts Learned

During this problem I learned:

* Strings
* String Cleaning
* Lowercase Conversion
* Reverse String
* Two Pointers
* Palindrome Checking
* Time Complexity
* Space Complexity

---

# Results

Problem Solved:

**LeetCode #125 - Valid Palindrome**

Approaches Learned:

* Reverse & Compare ✅
* Two Pointers ✅

Status:

* Accepted on LeetCode ✅
* Learned Two Pointer Pattern ✅

---

# Reflection

This was my first Two Pointer problem.

Initially, I thought only about reversing the string and comparing it.

Later, I learned a more efficient way using two pointers.

The biggest lesson from this problem was:

> Compare from both ends and move toward the center.

This pattern is widely used in string and array problems and is one of the most important interview techniques.
