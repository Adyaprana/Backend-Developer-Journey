# Day 20 - LeetCode #58: Length of Last Word

## Overview

Today I solved **LeetCode #58 - Length of Last Word**.

This problem helped me understand:

* String Manipulation
* String Splitting
* Reverse Traversal
* Pointer-Based Thinking
* Time and Space Complexity Analysis

Initially, I solved the problem using Python's built-in `split()` function. After getting the solution accepted, I learned the optimal Reverse Traversal approach that uses constant extra space.

---

# Problem Statement

Given a string `s` consisting of words and spaces, return the length of the last word in the string.

A word is defined as a maximal substring consisting of non-space characters only.

---

## Example 1

Input:

```python
s = "Hello World"
```

Output:

```python
5
```

Explanation:

```text
Last Word = World
Length = 5
```

---

## Example 2

Input:

```python
s = "   fly me   to   the moon  "
```

Output:

```python
4
```

Explanation:

```text
Last Word = moon
Length = 4
```

---

## Example 3

Input:

```python
s = "luffy is still joyboy"
```

Output:

```python
6
```

Explanation:

```text
Last Word = joyboy
Length = 6
```

---

# Constraints

```text
1 <= s.length <= 10⁴
s consists of English letters and spaces.
There will be at least one word.
```

---

# Understanding the Problem

We need to find:

```text
The last word
```

and then return:

```text
Its length
```

For example:

```python
s = "Hello World"
```

Last word:

```text
World
```

Length:

```text
5
```

---

# My First Thought

Initially I tried:

```python
last_word = s[-1]
```

But I realized:

```python
s[-1]
```

returns:

```text
Last Character
```

not:

```text
Last Word
```

Example:

```python
s = "Hello World"
```

```python
s[-1]
```

returns:

```python
'd'
```

not:

```python
'World'
```

---

# Approach 1: Split Solution

## Thought Process

Python provides:

```python
split()
```

which converts:

```python
"   fly me   to   the moon  "
```

into:

```python
["fly","me","to","the","moon"]
```

Then:

```python
[-1]
```

gives:

```python
"moon"
```

Finally:

```python
len()
```

returns:

```python
4
```

---

# Split Solution Code

```python
class Solution(object):
    def lengthOfLastWord(self, s):
        return len(s.split()[-1])
```

---

# Dry Run

Input:

```python
s = "   fly me   to   the moon  "
```

After:

```python
s.split()
```

Result:

```python
["fly","me","to","the","moon"]
```

Last word:

```python
["fly","me","to","the","moon"][-1]
```

Result:

```python
"moon"
```

Length:

```python
len("moon")
```

Result:

```python
4
```

Return:

```python
4
```

---

# Complexity (Split Solution)

Time Complexity:

```text
O(n)
```

Space Complexity:

```text
O(n)
```

Reason:

```python
split()
```

creates a new list containing all words.

---

# Approach 2: Reverse Traversal (Optimal)

## Thought Process

Instead of creating a list:

```python
split()
```

we start from the end of the string.

### Step 1

Skip trailing spaces.

Example:

```text
"   fly me   to   the moon  "
                           ^
```

Move left until we reach:

```text
n
```

---

### Step 2

Count letters.

```text
n -> 1
o -> 2
o -> 3
m -> 4
```

When we reach:

```text
(space)
```

stop.

Return:

```text
4
```

---

# Reverse Traversal Code

```python
class Solution(object):
    def lengthOfLastWord(self, s):

        right = len(s) - 1

        count = 0

        while s[right] == ' ':
            right -= 1

        while right >= 0 and s[right] != ' ':
            count += 1
            right -= 1

        return count
```

---

# Dry Run

Input:

```python
s = "   fly me   to   the moon  "
```

Initial:

```python
right = len(s) - 1
count = 0
```

Pointer:

```text
"   fly me   to   the moon  "
                           ^
```

---

## First While Loop

Skip spaces.

```text
(space)
```

Move left.

```text
(space)
```

Move left.

Now:

```text
"   fly me   to   the moon  "
                         ^
```

Character:

```text
n
```

Stop.

---

## Second While Loop

Count characters.

```text
n -> count = 1
o -> count = 2
o -> count = 3
m -> count = 4
```

Next character:

```text
(space)
```

Stop.

Return:

```python
4
```

---

# Why Reverse Traversal Is Better

Split solution:

```python
s.split()
```

creates:

```python
["fly","me","to","the","moon"]
```

which requires extra memory.

Reverse Traversal:

```python
right
count
```

uses only two variables.

No additional list is created.

---

# Complexity Comparison

| Approach          | Time | Space |
| ----------------- | ---- | ----- |
| Split Solution    | O(n) | O(n)  |
| Reverse Traversal | O(n) | O(1)  |

---

# Concepts Learned

During this problem I learned:

* String Manipulation
* String Splitting
* Reverse Traversal
* Pointer-Based Thinking
* Trailing Space Handling
* Time Complexity Analysis
* Space Complexity Analysis

---

# Results

Problem Solved:

**LeetCode #58 - Length of Last Word**

Approaches Learned:

* Split Solution ✅
* Reverse Traversal Solution ✅

Status:

* Accepted on LeetCode ✅
* Passed All Test Cases ✅

---

# Reflection

The biggest lesson from this problem was:

> A string can be traversed from the end just as easily as from the beginning.

The split solution was simple and easy to understand.

The reverse traversal solution taught me how to solve the same problem with:

```text
O(1) Space
```

which is often preferred in coding interviews.

This problem strengthened my understanding of string traversal and pointer-based problem solving.
