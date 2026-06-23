# Day 23 - LeetCode #2108: Find First Palindromic String in the Array

# Overview

Today I solved **LeetCode #2108 - Find First Palindromic String in the Array**.

This problem combines:

* Arrays
* Strings
* Two Pointers
* Palindrome Checking

The goal is to find the first palindrome string present in the array.

---

# Problem Statement

Given an array of strings:

```python
words = ["abc","car","ada","racecar","cool"]
```

Return the **first palindromic string** in the array.

If there is no palindrome string, return:

```python
""
```

---

# Example 1

Input:

```python
words = ["abc","car","ada","racecar","cool"]
```

Output:

```python
"ada"
```

Explanation:

```text
abc      -> Not Palindrome
car      -> Not Palindrome
ada      -> Palindrome ✅
racecar  -> Palindrome
cool     -> Not Palindrome
```

The first palindrome encountered is:

```python
"ada"
```

---

# Example 2

Input:

```python
words = ["notapalindrome","racecar"]
```

Output:

```python
"racecar"
```

---

# Example 3

Input:

```python
words = ["def","ghi"]
```

Output:

```python
""
```

No palindrome exists.

---

# Constraints

```text
1 <= words.length <= 100
1 <= words[i].length <= 100
words[i] consists only of lowercase English letters.
```

---

# Understanding the Problem

We need to:

```text
Check every word one by one.
```

For each word:

```text
Determine whether it is a palindrome.
```

The moment we find a palindrome:

```text
Return it immediately.
```

If no palindrome is found:

```text
Return an empty string.
```

---

# What is a Palindrome?

A palindrome reads the same from left to right and right to left.

Examples:

```text
madam
racecar
ada
level
```

Not palindromes:

```text
hello
abc
cool
```

---

# Approach 1: Two Pointers + Pointer Crossing (Preferred)

# Intuition

A palindrome must satisfy:

```text
First Character == Last Character
Second Character == Second Last Character
...
```

We can use two pointers:

```text
left
right
```

If all comparisons succeed:

```text
Pointers will meet or cross.
```

This means:

```python
left >= right
```

and the word is a palindrome.

---

# Algorithm

For each word:

1. Place left pointer at start.
2. Place right pointer at end.
3. Compare characters.
4. If mismatch occurs, stop checking that word.
5. If pointers cross successfully, return the word.
6. If no palindrome is found, return "".

---

# Accepted Solution (Your Solution)

```python
class Solution(object):

    def firstPalindrome(self, words):

        for word in words:

            left = 0
            right = len(word) - 1

            while left < right:

                if word[left] != word[right]:
                    break

                left += 1
                right -= 1

            if left >= right:
                return word

        return ""
```

---

# Dry Run

Input:

```python
words = ["abc","car","ada","racecar","cool"]
```

---

## Word = "abc"

```text
a != c
```

Break.

Pointers:

```python
left = 0
right = 2
```

Check:

```python
left >= right
```

```text
0 >= 2
```

False.

Not a palindrome.

---

## Word = "car"

```text
c != r
```

Break.

Not palindrome.

---

## Word = "ada"

```text
a == a
```

Move:

```python
left = 1
right = 1
```

Loop ends.

Check:

```python
left >= right
```

```text
1 >= 1
```

True.

Return:

```python
"ada"
```

---

# Why Pointer Crossing Works

For a palindrome:

```text
a d a
↑   ↑
```

After matching:

```text
d
↑
```

Pointers meet:

```python
left == right
```

Palindrome confirmed.

---

For even length:

```text
a b b a
↑     ↑
```

Pointers cross:

```python
left > right
```

Palindrome confirmed.

---

# Complexity Analysis

## Time Complexity

```text
O(n × m)
```

Where:

```text
n = number of words
m = average word length
```

Worst case:

Every character of every word is checked.

---

## Space Complexity

```text
O(1)
```

Only two pointers are used.

---

# Approach 2: Two Pointers + Boolean Flag

# Intuition

Instead of using pointer crossing, maintain a flag:

```python
is_palindrome = True
```

Whenever a mismatch occurs:

```python
is_palindrome = False
```

After checking the entire word:

```python
if is_palindrome:
```

return the word.

---

# Code

```python
class Solution(object):

    def firstPalindrome(self, words):

        for word in words:

            is_palindrome = True

            left = 0
            right = len(word) - 1

            while left < right:

                if word[left] != word[right]:
                    is_palindrome = False
                    break

                left += 1
                right -= 1

            if is_palindrome:
                return word

        return ""
```

---

# Dry Run

Word:

```python
"ada"
```

Initially:

```python
is_palindrome = True
```

Compare:

```text
a == a
```

Move pointers.

Loop ends.

Flag still:

```python
True
```

Return:

```python
"ada"
```

---

Word:

```python
"abc"
```

Compare:

```text
a != c
```

Set:

```python
is_palindrome = False
```

Break.

Do not return.

Move to next word.

---

# Comparison of Approaches

| Approach         | Time     | Space | Preferred |
| ---------------- | -------- | ----- | --------- |
| Pointer Crossing | O(n × m) | O(1)  | ✅ Yes     |
| Boolean Flag     | O(n × m) | O(1)  | Good      |

---

# Why Approach 1 is Better

Approach 1 directly uses the property of the algorithm:

```text
If all comparisons succeed,
the pointers must meet or cross.
```

No extra variable is required.

This makes the solution:

```text
Cleaner
More Elegant
More Interview-Friendly
```

---

# Alternative Python Solution

Using string reversal:

```python
class Solution(object):

    def firstPalindrome(self, words):

        for word in words:

            if word == word[::-1]:
                return word

        return ""
```

---

# Why We Didn't Use This

Although accepted:

```python
word[::-1]
```

hides the palindrome logic.

The Two Pointer approach demonstrates:

```text
String Traversal
Pointer Manipulation
Problem Solving
```

which is usually preferred during interviews.

---

# Concepts Learned

* Arrays
* Strings
* Palindrome Checking
* Two Pointers
* Pointer Crossing
* Boolean Flag Technique
* Time Complexity Analysis
* Space Complexity Analysis

---

# Interview Pattern

This problem reinforces:

```text
Two Pointers
```

The same pattern appears in:

* Valid Palindrome (#125)
* Reverse String (#344)
* Squares of a Sorted Array (#977)
* Two Sum II (#167)

---

# Results

Problem Solved:

**LeetCode #2108 - Find First Palindromic String in the Array**

Approaches Learned:

* Two Pointers + Pointer Crossing ✅
* Two Pointers + Boolean Flag ✅
* Reverse String Method ✅

Status:

* Accepted on LeetCode ✅
* Passed All Test Cases ✅

---

# Reflection

The biggest lesson from this problem was:

> A palindrome can be detected without any extra variable by observing the positions of the pointers.

If all comparisons succeed:

```python
left >= right
```

must eventually become true.

This makes the Pointer Crossing approach a clean and elegant Two Pointer solution.
