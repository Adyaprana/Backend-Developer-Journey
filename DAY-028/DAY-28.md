# Day 28 - Rest Day + DSA Revision

# Overview

According to my roadmap, Day 28 was a **Rest Day**.

Instead of learning a new Python topic, I focused on reinforcing what I had already learned throughout Month 1.

I also solved **two LeetCode Easy problems**, which helped strengthen my understanding of HashMaps, Bit Manipulation, and optimized algorithms.

---

# Roadmap Status

✔ Rest Day

✔ Revision Day

✔ No new Python concepts

✔ DSA Practice

---

# LeetCode Problems Solved

## 1. LeetCode #136 - Single Number

### Concepts Learned

- HashMap (Frequency Counter)
- Dictionary Traversal
- Bit Manipulation
- XOR Operator
- Time Complexity Analysis
- Space Complexity Analysis

### Approaches

- HashMap (Accepted)
- XOR Optimization (Optimal)

### Best Complexity

Time

```
O(n)
```

Space

```
O(1)
```

using XOR.

---

## 2. LeetCode #169 - Majority Element

### Concepts Learned

- Frequency Counting
- HashMap
- Majority Element
- Boyer-Moore Voting Algorithm
- Pair Cancellation Technique
- Time & Space Optimization

### Approaches

- Brute Force
- HashMap
- Boyer-Moore Voting Algorithm

### Best Complexity

Time

```
O(n)
```

Space

```
O(1)
```

using Boyer-Moore Voting Algorithm.

---

# Month 1 Revision

Today I reviewed the Python concepts I learned during the first month.

## Python Fundamentals

- Variables
- Data Types
- Input / Output
- Operators
- Strings
- Conditional Statements
- Loops
- Functions

---

## Python Data Structures

- Lists
- Tuples
- Dictionaries
- Sets

---

## Intermediate Python

- File Handling
- Exception Handling
- Modules
- OOP
- Decorators
- Generators
- Requests Library
- APIs
- JSON

---

## Backend Concepts Learned

- HTTP
- REST APIs
- GET Request
- POST Request
- JSON Response
- GitHub API
- Weather API
- Python Requests Library

---

# DSA Patterns Revised

## HashMap / Frequency Counter

Used in:

- Two Sum
- Contains Duplicate
- Single Number
- Majority Element

Pattern:

```python
count = {}

for num in nums:
    count[num] = count.get(num, 0) + 1
```

---

## XOR

Important Properties

```text
a ^ a = 0

a ^ 0 = a
```

Used in

- Single Number
- Bit Manipulation

---

## Boyer-Moore Voting Algorithm

Key Idea

Different elements cancel each other.

Since the majority element appears more than ⌊n/2⌋ times, it can never be completely cancelled.

Only the majority element survives.

Complexity

Time

```
O(n)
```

Space

```
O(1)
```

---

# Important Takeaways

During Month 1, I realized that solving interview problems is not only about getting an accepted solution.

A better workflow is:

1. Understand the problem.
2. Write the brute-force solution.
3. Improve the solution.
4. Learn the optimal approach.
5. Analyze time complexity.
6. Analyze space complexity.
7. Understand the interview pattern.

This approach helps me understand the reasoning behind algorithms instead of memorizing code.

---

# Progress Summary

## Python

✅ Python Basics

✅ Functions

✅ OOP

✅ File Handling

✅ Exception Handling

✅ Modules

✅ Decorators

✅ Generators

✅ Requests Library

---

## Backend

✅ HTTP

✅ APIs

✅ JSON

✅ GitHub API

---

## DSA Progress (Month 1)

By the end of Month 1, I completed the following LeetCode problems:

| #   | Problem | Difficulty | Main Concept |
|-----|---------|------------|--------------|
| 1   | Two Sum | Easy | HashMap |
| 217 | Contains Duplicate | Easy | HashSet |
| 242 | Valid Anagram | Easy | HashMap / Sorting |
| 125 | Valid Palindrome | Easy | Two Pointers |
| 20  | Valid Parentheses | Easy | Stack |
| 121 | Best Time to Buy and Sell Stock | Easy | Sliding Window / Greedy |
| 14  | Longest Common Prefix | Easy | Strings |
| 58  | Length of Last Word | Easy | Strings |
| 26  | Remove Duplicates from Sorted Array | Easy | Two Pointers |
| 28  | Find the Index of the First Occurrence in a String | Easy | String Matching |
| 2108| Find First Palindromic String in the Array | Easy | Strings |
| 387 | First Unique Character in a String | Easy | HashMap |
| 349 | Intersection of Two Arrays | Easy | HashSet |
| 136 | Single Number | Easy | XOR / Bit Manipulation |
| 169 | Majority Element | Easy | Boyer-Moore Voting Algorithm |

### Total Solved

- ✅ 15 Easy LeetCode Problems
- ✅ Multiple Solution Approaches
- ✅ Time & Space Complexity Analysis
- ✅ Dry Runs
- ✅ Interview Notes

---

# Month 1 Reflection

# Month 1 Reflection

Month 1 was focused on building a strong Python foundation while gradually developing problem-solving skills through LeetCode.

By the end of the month, I had solved **15 Easy LeetCode problems**, covering a variety of fundamental interview patterns including HashMaps, HashSets, Two Pointers, Strings, Stacks, Sliding Window, Bit Manipulation, and Boyer-Moore Voting Algorithm.

Instead of simply collecting accepted submissions, I documented each problem with:
- Problem Statement
- Brute Force Solution
- Better Solution
- Optimal Solution
- Dry Run
- Complexity Analysis
- Interview Notes
- Personal Reflection

This helped me understand *why* an algorithm works rather than just memorizing code.

Month 1 gave me a strong foundation in both Python and DSA, preparing me for more advanced backend development and medium-level interview problems in the coming months.

---

# What's Next?

Month 2 will focus on:

- Advanced Python
- FastAPI
- Backend Development
- SQL
- Databases
- More DSA
- Real Backend Projects

The goal is to gradually transition from learning Python syntax to building production-ready backend applications.

---

# Today's Stats

Roadmap Day

**Day 28**

Python Topic

**Rest / Revision**

LeetCode Problems Solved

- #136 Single Number
- #169 Majority Element

Status

✅ Completed

GitHub Commit

```
Day 28: Rest day, Month 1 revision, and DSA practice (#136 Single Number & #169 Majority Element)
```

---

# Final Thoughts

> "Progress isn't measured only by learning something new every day. Sometimes the biggest improvement comes from revisiting what you've already learned, understanding it more deeply, and recognizing patterns that connect different problems."

Month 1 Complete ✅

On to Month 2 🚀