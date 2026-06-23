# Day 14 - LeetCode #1: Two Sum

## Overview

Today I solved my first LeetCode problem, **Two Sum**, and learned both the **Brute Force** and **HashMap (Dictionary)** approaches.

Initially, I focused on understanding the problem rather than jumping directly to the optimized solution. My goal was to understand the logic behind the solution and how to think through the problem step by step.

---

## Problem Statement

Given an array of integers `nums` and an integer `target`, return the indices of the two numbers such that they add up to the target.

### Example

**Input**

```python
nums = [2,7,11,15]
target = 9
```

**Output**

```python
[0,1]
```

**Explanation**

```python
2 + 7 = 9
```

Therefore, return:

```python
[0,1]
```

---

## Approach 1: Brute Force

### Thought Process

I first solved the problem using nested loops.

For each element in the array:

* Compare it with every element after it.
* Check if their sum equals the target.
* If yes, return their indices.

### Brute Force Code

```python
class Solution(object):
    def twoSum(self, nums, target):
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
```

### Complexity

**Time Complexity**

```text
O(n²)
```

**Space Complexity**

```text
O(1)
```

### What I Learned

* How nested loops work together.
* Why checking every possible pair guarantees a correct answer.
* How to return indices instead of values.
* Why brute-force solutions become slow for large inputs.

---

## Understanding LeetCode's Class Format

I learned that LeetCode provides code templates such as:

```python
class Solution(object):
    def twoSum(self, nums, target):
```

Instead of writing standalone functions, solutions must be written inside the provided method.

### Key Learnings

* `self` refers to the current object.
* LeetCode automatically creates the object and calls the method.
* I only need to write the logic inside the method.

---

## Approach 2: HashMap (Dictionary)

After solving the brute-force version, I learned the optimized approach using a dictionary.

### Key Idea

Instead of searching the entire array every time, store previously seen numbers and their indices.

Dictionary format:

```text
number → index
```

### Example

```python
{
    2: 0,
    7: 1
}
```

For every number:

1. Calculate the complement:

```python
target - current_number
```

2. Check if the complement already exists in the dictionary.

3. If it exists:

   * The answer is found.
   * Return the stored index and current index.

4. Otherwise:

   * Store the current number and its index.
   * Continue.

---

## HashMap Solution

```python
class Solution(object):
    def twoSum(self, nums, target):
        seen = {}

        for i in range(len(nums)):
            find = target - nums[i]

            if find in seen:
                return [seen[find], i]

            seen[nums[i]] = i
```

---

## Dry Run

### Input

```python
nums = [3,2,4]
target = 6
```

### Iteration 1

```python
num = 3
find = 3
```

Dictionary:

```python
{}
```

Store:

```python
{3:0}
```

---

### Iteration 2

```python
num = 2
find = 4
```

Dictionary:

```python
{3:0}
```

Store:

```python
{3:0, 2:1}
```

---

### Iteration 3

```python
num = 4
find = 2
```

Dictionary:

```python
{3:0, 2:1}
```

Since:

```python
2 in seen
```

Answer found:

```python
[1,2]
```

---

## Challenges Faced

While learning the HashMap approach, I initially struggled with:

* Understanding the difference between index and value.
* Using `len(nums)` incorrectly when I actually needed `nums[i]`.
* Understanding what should be stored in the dictionary.
* Knowing whether to store first or check first.
* Returning the correct indices instead of printing values.

By tracing the algorithm manually, I gradually understood how the dictionary stores:

```text
number → index
```

and why checking before storing prevents matching a number with itself.

---

## Complexity Comparison

| Approach    | Time Complexity | Space Complexity |
| ----------- | --------------- | ---------------- |
| Brute Force | O(n²)           | O(1)             |
| HashMap     | O(n)            | O(n)             |

---

## Final Understanding

The biggest lesson from today was:

> Instead of searching for the complement in the remaining array, store previously seen numbers in a dictionary and check whether the complement already exists.

This reduced the time complexity from:

```text
O(n²)
```

to:

```text
O(n)
```

---

## Concepts Learned

During this problem I learned:

* Arrays
* Nested Loops
* Dictionaries
* HashMaps
* Time Complexity
* Space Complexity
* Index vs Value
* Dictionary Lookup
* LeetCode Class Structure
* Optimization using HashMaps

---

## Results

### Problem Solved

**LeetCode #1 - Two Sum**

### Approaches Learned

* Brute Force ✅
* HashMap (Dictionary) ✅

### Status

* Accepted on LeetCode ✅
* Passed All Test Cases ✅
* Understood the Optimal Solution ✅

---

## Reflection

Today was not just about solving a problem.

It was about understanding how to think through a problem, identify inefficiencies, and improve the solution step by step.

Most importantly, I did not directly copy the optimized solution. I started with the brute-force approach, learned the reasoning behind the HashMap approach, debugged my mistakes, and gradually understood why the optimized solution works.

This was my first practical experience with using a HashMap to reduce time complexity from **O(n²)** to **O(n)**.
