# LeetCode #918 — Maximum Sum Circular Subarray
---

# Problem Statement

Given a circular integer array `nums` of length `n`, return the maximum possible sum of a non-empty subarray.

A circular array means the element after the last element is the first element of the array.

A subarray may only include each element at most once.

---

# Examples

## Example 1

Input

```text
nums = [1,-2,3,-2]
```

Output

```text
3
```

Explanation

The best subarray is

```text
[3]
```

Circular subarrays do not produce a larger answer.

---

## Example 2

Input

```text
nums = [5,-3,5]
```

Output

```text
10
```

Explanation

Choose

```text
5

↓

5
```

by wrapping around the array.

---

## Example 3

Input

```text
nums = [-3,-2,-3]
```

Output

```text
-2
```

---

# Constraints

```text
1 <= nums.length <= 30000

-30000 <= nums[i] <= 30000
```

---

# Understanding the Problem

Unlike a normal array,

a circular array wraps around.

Normal array

```text
1 2 3 4 5
```

After

```text
5
```

the array ends.

---

Circular array

```text
1 2 3 4 5
↑         ↓
└─────────┘
```

After

```text
5
```

comes

```text
1
```

again.

---

# What is the Problem Asking?

Find

```text
The Maximum Sum

of

One Non-Empty Circular Subarray
```

Notice

The subarray can wrap around,

but every element can be used at most once.

---

# Important Observations

## Observation 1

The answer may be completely inside the array.

Example

```text
1 -2 3 -2
```

Answer

```text
3
```

---

## Observation 2

The answer may wrap around.

Example

```text
5 -3 5
```

Instead of taking

```text
5 -3 5

=

7
```

we take

```text
5

↓

5

=

10
```

---

## Observation 3

Sometimes wrapping is useless.

Normal Kadane already gives the answer.

---

# First Thought

Since I already solved

```text
LeetCode #53
```

I immediately thought about Kadane's Algorithm.

But Kadane only works for

```text
Normal Arrays
```

This problem allows

```text
Wrapping Around
```

So a new observation is needed.

---

# The Big Observation

Look carefully.

Original Array

```text
5 -3 5
```

Circular Answer

```text
5

↓

5
```

What was removed?

```text
-3
```

Interesting...

Instead of directly finding the circular subarray,

we can think of it as

```text
Whole Array

-

Middle Part
```

Now the question becomes

```text
Which middle part should we remove?
```

Removing the smallest (minimum) contiguous subarray leaves the largest possible circular sum.

---

# New Formula

Circular Maximum

```text
=

Total Sum

-

Minimum Subarray Sum
```

Example

```text
5 -3 5
```

Total

```text
7
```

Minimum Subarray

```text
-3
```

Circular Answer

```text
7 - (-3)

=

10
```

---

# Why Does This Work?

Imagine cutting out the worst (minimum) contiguous subarray.

Everything that remains automatically forms the maximum circular subarray.

Instead of choosing the circular answer directly,

we remove the worst middle section.

---

# Interview Questions

### Q1

What makes a circular array different from a normal array?

---

### Q2

Why can't normal Kadane alone solve this problem?

---

### Q3

Why do we subtract the minimum subarray?

---

### Q4

What does the removed subarray represent?

---

# Learning Summary

After Part 1, I learned:

- What a circular array is.
- Why Kadane alone is not enough.
- The circular answer can be viewed as the whole array minus one contiguous section.
- The removed section must be the minimum subarray.
- This transforms the problem into a combination of Total Sum and Minimum Kadane.

---

# Optimal Approach

This problem is an extension of **Kadane's Algorithm**.

Instead of creating a completely new algorithm,

we combine three ideas.

```text
1. Maximum Kadane

2. Minimum Kadane

3. Total Sum
```

---

# Revisiting Kadane's Algorithm

From LeetCode #53, we already know how to find

```text
Maximum Contiguous Subarray Sum
```

using Kadane's Algorithm.

Now we learn one more variation.

```text
Minimum Contiguous Subarray Sum
```

The idea is exactly the same.

The only difference is

Instead of choosing the larger value,

we choose the smaller one.

---

# Maximum Kadane

For every element we ask

```text
Continue Current Subarray

OR

Start Again
```

Choose whichever gives

```text
Larger Sum
```

This gives

```text
Maximum Subarray Sum
```

---

# Minimum Kadane

Again ask

```text
Continue Current Subarray

OR

Start Again
```

But now choose

```text
Smaller Sum
```

This gives

```text
Minimum Subarray Sum
```

It is simply Kadane's Algorithm in reverse.

---

# Why Do We Need Both?

There are only two possible answers.

---

## Case 1

The answer is completely inside the array.

Example

```text
1 -2 3 -2
```

Maximum Subarray

```text
3
```

Circular answer

```text
2
```

Correct answer

```text
3
```

Here,

Normal Kadane wins.

---

## Case 2

The answer wraps around.

Example

```text
5 -3 5
```

Maximum Kadane

```text
7
```

Circular

```text
10
```

Correct answer

```text
10
```

Here,

Circular wins.

---

# The Complete Formula

There are only two candidates.

Candidate 1

```text
Maximum Kadane
```

Candidate 2

```text
Total Sum

-

Minimum Kadane
```

Final Answer

```text
max(

Maximum Kadane,

Total Sum - Minimum Kadane

)
```

---

# The Important Edge Case

Consider

```text
[-3,-2,-5]
```

Maximum Kadane

```text
-2
```

Minimum Kadane

```text
-10
```

Total Sum

```text
-10
```

Circular Formula

```text
-10 - (-10)

=

0
```

But

```text
0
```

is impossible.

Why?

Because

```text
Minimum Subarray

=

Entire Array
```

Removing the entire array leaves

```text
Nothing
```

which means

```text
Empty Subarray
```

The problem requires

```text
At Least One Element
```

Therefore

If

```text
Minimum Subarray

==

Total Sum
```

we cannot use the circular answer.

Simply return

```text
Maximum Kadane
```

---

# Complete Algorithm

```text
Initialize

↓

Total Sum

↓

Maximum Kadane

↓

Minimum Kadane

↓

Traverse Array Once

↓

Update

Total Sum

Maximum Kadane

Minimum Kadane

↓

If

Minimum == Total

↓

Return Maximum Kadane

↓

Else

Return

max(

Maximum Kadane,

Total - Minimum

)
```

---

# My Final Code

```python
class Solution(object):
    def maxSubarraySumCircular(self, nums):

        total_sum = nums[0]

        min_current = nums[0]
        min_subarr = nums[0]

        max_current = nums[0]
        max_subarr = nums[0]

        for i in range(1, len(nums)):

            total_sum += nums[i]

            # Minimum Kadane
            if nums[i] < (min_current + nums[i]):
                min_current = nums[i]
            else:
                min_current += nums[i]

            if min_current < min_subarr:
                min_subarr = min_current

            # Maximum Kadane
            if nums[i] > (max_current + nums[i]):
                max_current = nums[i]
            else:
                max_current += nums[i]

            if max_current > max_subarr:
                max_subarr = max_current

        if min_subarr == total_sum:
            return max_subarr

        return max(max_subarr, total_sum - min_subarr)
```

---

# Dry Run

Input

```text
nums = [5,-3,5]
```

Initial Values

```text
Total = 5

Max Current = 5
Max Subarray = 5

Min Current = 5
Min Subarray = 5
```

---

Element

```text
-3
```

Total

```text
2
```

Maximum Kadane

```text
Continue

5 + (-3)

=

2

↓

Max Current = 2

↓

Max Subarray = 5
```

Minimum Kadane

```text
Start Again

-3

↓

Min Current = -3

↓

Min Subarray = -3
```

---

Element

```text
5
```

Total

```text
7
```

Maximum Kadane

```text
Continue

2 + 5

=

7

↓

Max Current = 7

↓

Max Subarray = 7
```

Minimum Kadane

```text
Start Again

5

↓

Min Current = 2

↓

Min Subarray = -3
```

---

Final Values

```text
Maximum Kadane = 7

Minimum Kadane = -3

Total Sum = 7
```

Circular Answer

```text
7 - (-3)

=

10
```

Return

```text
max(7,10)

=

10
```

---

# Why This Works

Instead of directly finding the circular subarray,

we remove the worst contiguous part.

```text
Whole Array

↓

Remove Minimum Subarray

↓

Remaining Elements

↓

Maximum Circular Subarray
```

If removing the minimum subarray removes the entire array,

we ignore the circular answer and use the normal Kadane result.

---

# Complexity Analysis

## Time Complexity

```text
O(n)
```

The array is traversed only once.

---

## Space Complexity

```text
O(1)
```

Only a few variables are used.

---

# Common Mistakes

## ❌ Forgetting the Edge Case

```python
return max(max_subarr, total_sum - min_subarr)
```

fails for

```text
[-3,-2,-5]
```

Always check

```python
if min_subarr == total_sum:
    return max_subarr
```

---

## ❌ Updating Minimum Kadane Incorrectly

Minimum Kadane chooses

```text
Smaller
```

not

```text
Larger
```

---

## ❌ Forgetting Maximum Kadane

Some people compute only

```text
Total - Minimum
```

This fails when the normal subarray is better.

---

## ❌ Removing the Entire Array

A circular subarray must contain

```text
At Least One Element
```

Removing the whole array creates an empty subarray, which is invalid.

---

# Pattern Recognition

Whenever you see

```text
Circular Array

+

Maximum Sum
```

Think

```text
Kadane's Algorithm

+

Minimum Kadane

+

Total Sum
```

---

# Related Problems

- LeetCode #53 — Maximum Subarray
- LeetCode #152 — Maximum Product Subarray
- LeetCode #918 — Maximum Sum Circular Subarray
- Maximum Sum Rectangle (2D Kadane)

---

# Interview Questions

### Q1

Why isn't normal Kadane enough?

---

### Q2

Why do we subtract the minimum subarray?

---

### Q3

Why do we need both Maximum and Minimum Kadane?

---

### Q4

Why do we compare two answers?

---

### Q5

Why does the all-negative case need special handling?

---

# Pattern Library Update

```text
Arrays
│
├── Running Sum
│
├── Prefix Sum
│
├── Prefix Sum + HashMap
│
├── In-place Modification
│
├── Merge from End
│
├── Array Rotation
│
└── Kadane's Algorithm
    │
    ├── #53 Maximum Subarray
    │
    └── #918 Maximum Sum Circular Subarray
         │
         ├── Maximum Kadane
         ├── Minimum Kadane
         ├── Total Sum
         └── Circular Array Pattern
```

---
