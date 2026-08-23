# LeetCode #53 — Maximum Subarray

---

# Problem Statement

Given an integer array `nums`, find the **contiguous subarray** (containing at least one number) which has the **largest sum**, and return its sum.

---

# Examples

## Example 1

```text
Input

nums = [-2,1,-3,4,-1,2,1,-5,4]
```

Output

```text
6
```

Explanation

```text
The subarray

[4,-1,2,1]

has the maximum sum.

4 + (-1) + 2 + 1 = 6
```

---

## Example 2

```text
Input

nums = [1]
```

Output

```text
1
```

---

## Example 3

```text
Input

nums = [5,4,-1,7,8]
```

Output

```text
23
```

---

# Constraints

```text
1 <= nums.length <= 10⁵

-10⁴ <= nums[i] <= 10⁴
```

---

# Understanding the Problem

The most important word in this problem is

```text
Contiguous
```

A contiguous subarray means

```text
All elements must stay together.
```

You cannot skip any element.

---

## Example

```text
nums

4  -1  2  1
```

Allowed

```text
[4,-1]

[-1,2]

[2,1]

[4,-1,2]

[4,-1,2,1]
```

---

Not Allowed

```text
4 2

4 1

-1 1
```

because elements were skipped.

---

# What Is the Problem Asking?

The problem is asking us to find

```text
One Contiguous Subarray

↓

Having

↓

Maximum Sum
```

It is **not** asking for

- The largest number
- The longest subarray
- The maximum prefix sum
- The sum of the entire array

Only the contiguous subarray with the largest sum.

---

# Important Observations

## Observation 1

The answer can start from **any index**.

Example

```text
5 -10 20
```

The answer is

```text
20
```

not

```text
5 -10 20
```

---

## Observation 2

The answer can end at **any index**.

It does not have to end at the last element.

---

## Observation 3

The array may contain negative numbers.

Example

```text
[-2,-3,-1,-5]
```

The answer is

```text
-1
```

not

```text
0
```

---

## Observation 4

Sometimes extending a subarray makes the sum worse.

Example

```text
5 -10
```

Current sum

```text
-5
```

Carrying this negative sum into the future may not be a good idea.

This observation leads to Kadane's Algorithm.

---

# My First Idea (Why It Fails)

My first idea was similar to a Prefix Sum.

```python
prefix_sum += nums[i]
```

I thought if I kept adding numbers, I could find the maximum sum.

---

## Why This Doesn't Work

A Prefix Sum always represents

```text
Index 0

↓

Current Index
```

It never starts from another index.

---

## Example

```text
nums

5 -10 20
```

Prefix sums

```text
5

↓

-5

↓

15
```

The maximum prefix sum is

```text
15
```

But the correct answer is

```text
20
```

because

```text
[20]
```

is also a valid contiguous subarray.

My Prefix Sum approach never considered starting from index 2.

---

# Brute Force Approach

The simplest solution is to generate every possible contiguous subarray.

For every starting position

keep extending the subarray

calculate its sum

update the maximum sum.

---

## Algorithm

```text
Choose Start Index

↓

Current Sum = 0

↓

Keep Extending

↓

Add Current Number

↓

Update Maximum Sum

↓

Move Start Index

↓

Repeat
```

---

# Example Dry Run

```text
nums

[-2,1,-3]
```

Possible contiguous subarrays

```text
[-2]

[-2,1]

[-2,1,-3]

[1]

[1,-3]

[-3]
```

Their sums

```text
-2

-1

-4

1

-2

-3
```

Maximum Sum

```text
1
```

Subarray

```text
[1]
```

---

# Brute Force Code

```python
class Solution(object):
    def maxSubArray(self, nums):

        maximum = nums[0]

        for start in range(len(nums)):

            current_sum = 0

            for end in range(start, len(nums)):

                current_sum += nums[end]

                if current_sum > maximum:
                    maximum = current_sum

        return maximum
```

---

# Complexity Analysis (Brute Force)

## Time Complexity

```text
O(n²)
```

There are

- `n` choices for the starting index.
- For each start, we extend to the end of the array.

---

## Space Complexity

```text
O(1)
```

No extra data structure is used.

---

# Why Brute Force Is Rejected

Although it checks every possible contiguous subarray,

it becomes too slow for large inputs.

Suppose

```text
Length = 100000
```

Checking every subarray requires millions (actually billions) of operations.

We need something faster.

---

# The Big Observation

While solving this problem, an important question appears.

Instead of checking

```text
Every Possible Subarray
```

Can we immediately discard

```text
Bad Subarrays
```

that can never become part of the maximum answer?

This simple observation leads to one of the most famous algorithms in Data Structures and Algorithms.

```text
Kadane's Algorithm
```

---

# Interview Questions

### Q1

What does "contiguous" mean?

---

### Q2

Why doesn't a Prefix Sum solve this problem?

---

### Q3

Can the answer start from any index?

---

### Q4

Can the maximum subarray contain negative numbers?

---

### Q5

Why is the brute-force approach too slow?

---

# Learning Summary

After solving Part 1, I learned:

- A contiguous subarray cannot skip elements.
- The maximum subarray can start and end at any index.
- Prefix Sum cannot solve this problem because it always starts from index `0`.
- Brute force checks every possible contiguous subarray and works correctly.
- However, the brute-force solution has `O(n²)` time complexity, making it too slow for large inputs.
- The key insight is that some running sums become so bad that they are never worth extending. This observation leads to **Kadane's Algorithm**, which solves the problem in linear time.

---

# Optimal Approach — Kadane's Algorithm

Kadane's Algorithm is one of the most famous algorithms in Data Structures and Algorithms.

It finds the maximum sum contiguous subarray in

```text
O(n)
```

time.

Instead of checking every possible subarray,

it makes a decision at every element.

---

# What is Kadane's Algorithm?

Kadane's Algorithm asks only one question at every element.

```text
Should I

Continue

OR

Start Again?
```

That's it.

This simple decision makes the algorithm extremely fast.

---

# The Core Idea

Suppose

```text
Current Sum = 5

Current Number = -2
```

We have two choices.

### Choice 1

Continue the current subarray.

```text
5 + (-2)

=

3
```

---

### Choice 2

Start a brand-new subarray.

```text
-2
```

Which is better?

```text
3
```

So

```text
Continue
```

wins.

---

Now suppose

```text
Current Sum = -10

Current Number = 20
```

Choices

Continue

```text
-10 + 20

=

10
```

Start Again

```text
20
```

Which is better?

```text
20
```

So we throw away the old subarray

and start a new one.

---

# Why Negative Running Sum Is Bad

Example

```text
5  -10  20
```

Current Sum after

```text
5 -10
```

is

```text
-5
```

Now we reach

```text
20
```

Choices

Continue

```text
-5 + 20

=

15
```

Start Again

```text
20
```

Obviously

```text
20
```

is better.

A negative running sum only reduces future sums.

So whenever starting fresh is better,

we discard the previous subarray.

---

# Current Sum vs Best Sum

Kadane's Algorithm uses two variables.

---

## Current Sum

Represents

```text
The best subarray

Ending At

Current Index
```

This value changes every iteration.

Sometimes we continue.

Sometimes we start again.

---

## Best Sum

Represents

```text
The Best Answer

Found So Far
```

Once a better answer is found,

we save it.

Even if future subarrays become worse,

the best answer remains.

---

# Understanding the Algorithm

For every number

we compare

```text
Continue

↓

Current Sum + Current Number
```

with

```text
Start Again

↓

Current Number
```

Whichever is larger

becomes the new

```text
Current Sum
```

Then compare

```text
Current Sum
```

with

```text
Best Sum
```

If

```text
Current Sum
```

is larger,

update

```text
Best Sum
```

Repeat until the end.

---

# My Final Code

```python
class Solution(object):
    def maxSubArray(self, nums):

        Current_Sum = 0
        ans = nums[0]

        for i in range(len(nums)):

            if nums[i] > (Current_Sum + nums[i]):
                Current_Sum = nums[i]

            else:
                Current_Sum += nums[i]

            if ans < Current_Sum:
                ans = Current_Sum

        return ans
```

---

# Dry Run

Input

```text
nums = [-2,1,-3,4,-1,2,1,-5,4]
```

| Current Number | Continue | Start Again | Current Sum | Best Sum |
|---------------:|---------:|------------:|------------:|----------:|
| -2 | -2 | -2 | -2 | -2 |
| 1 | -1 | 1 | 1 | 1 |
| -3 | -2 | -3 | -2 | 1 |
| 4 | 2 | 4 | 4 | 4 |
| -1 | 3 | -1 | 3 | 4 |
| 2 | 5 | 2 | 5 | 5 |
| 1 | 6 | 1 | 6 | 6 |
| -5 | 1 | -5 | 1 | 6 |
| 4 | 5 | 4 | 5 | 6 |

Final Answer

```text
6
```

Subarray

```text
[4,-1,2,1]
```

---

# Why Kadane Works

Imagine carrying a backpack.

The backpack is your

```text
Current Sum
```

If the backpack is helping you,

keep carrying it.

Example

```text
Current Sum = 8
```

Next Number

```text
2
```

New Sum

```text
10
```

Great.

Keep going.

---

Now imagine the backpack becomes heavy.

```text
Current Sum = -20
```

Next Number

```text
5
```

Choices

```text
-20 + 5

=

-15
```

or

```text
5
```

Why carry the extra weight?

Drop the backpack.

Start fresh.

That is exactly what Kadane's Algorithm does.

---

# Complexity Analysis

## Time Complexity

```text
O(n)
```

Every element is visited exactly once.

---

## Space Complexity

```text
O(1)
```

Only two variables are used.

---

# Common Mistakes

## ❌ Initializing

```python
ans = 0
```

Fails for

```text
[-5]
```

Correct Answer

```text
-5
```

---

## ❌ Returning Current Sum

Always return

```text
Best Sum
```

because the current subarray may not be the maximum one.

---

## ❌ Confusing Prefix Sum with Kadane

Prefix Sum always starts from

```text
Index 0
```

Kadane can start a new subarray at any index.

---

## ❌ Thinking HashMap Is Needed

Kadane uses

```text
Current Sum

+

Best Sum
```

No HashMap is required.

---

## ❌ Updating Best Sum Inside Only One Branch

Best Sum should be checked after every iteration,

regardless of whether we continued or started again.

---

# Pattern Recognition

Whenever you see words like

```text
Maximum

Minimum

Best

Largest

Contiguous Subarray
```

Think

```text
Kadane's Algorithm
```

---

# Where Is Kadane Used?

- LeetCode #53 — Maximum Subarray
- LeetCode #918 — Maximum Sum Circular Subarray
- LeetCode #152 — Maximum Product Subarray (variation)
- Maximum Sum Rectangle in a Matrix (2D Kadane)
- Dynamic Programming optimization problems
- Stock profit style problems (some variations)

---

# Interview Questions

### Q1

What is the main idea behind Kadane's Algorithm?

---

### Q2

Why do we sometimes start a new subarray?

---

### Q3

What is the difference between Current Sum and Best Sum?

---

### Q4

Why doesn't Prefix Sum solve this problem?

---

### Q5

Why isn't a HashMap needed?

---

### Q6

What happens if all numbers are negative?

---
## Alternative Approach

This problem can also be solved using the Divide & Conquer technique.

- Time Complexity: O(n log n)
- Space Complexity: O(log n) (recursion stack)

However, since Kadane's Algorithm solves the problem in O(n) time with O(1) extra space, it is the preferred solution for interviews and competitive programming.

I will learn the Divide & Conquer solution later when studying the Recursion and Divide & Conquer pattern.


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
├── Two Pointers (Merge from End)
│
├── Array Rotation
│
└── Kadane's Algorithm
      │
      └── #53 Maximum Subarray
```

---
