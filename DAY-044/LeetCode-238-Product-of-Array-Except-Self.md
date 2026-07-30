# LeetCode #238 — Product of Array Except Self

---

# Problem Statement

Given an integer array `nums`, return an array `answer` such that:

```text
answer[i]
```

is equal to the product of **all the elements of `nums` except `nums[i]`**.

You **must not use division**, and your algorithm should run in **O(n)** time.

---

# Example 1

```text
Input

nums = [1,2,3,4]

Output

[24,12,8,6]
```

### Explanation

```text
Index 0

Ignore 1

2 × 3 × 4 = 24

----------------------

Index 1

Ignore 2

1 × 3 × 4 = 12

----------------------

Index 2

Ignore 3

1 × 2 × 4 = 8

----------------------

Index 3

Ignore 4

1 × 2 × 3 = 6
```

---

# Example 2

```text
Input

nums = [-1,1,0,-3,3]

Output

[0,0,9,0,0]
```

---

# Constraints

```text
2 <= nums.length <= 10⁵

-30 <= nums[i] <= 30
```

---

# Understanding the Problem

At first glance, this problem looks very simple.

For every index,

multiply every number except the current one.

Example

```text
nums

[1,2,3,4]
```

Need

```text
For 1

↓

2×3×4

↓

24

-------------------

For 2

↓

1×3×4

↓

12

-------------------

For 3

↓

1×2×4

↓

8

-------------------

For 4

↓

1×2×3

↓

6
```

Final Answer

```text
[24,12,8,6]
```

---

# What Makes This Problem Difficult?

There are **two important conditions**.

## Condition 1

You cannot use

```text
Division
```

Even though it looks like the easiest solution.

---

## Condition 2

Your solution must run in

```text
O(n)
```

This means

```text
One traversal

or

A few traversals

```

are allowed.

Nested loops are **not**.

---

# Important Things To Think About

Whenever you see this question,

don't immediately think about multiplication.

Instead ask yourself

> **What numbers should each index multiply?**

Example

```text
nums

[1,2,3,4]
```

For

```text
Index 0
```

Need

```text
2×3×4
```

Notice

Everything is on the

```text
RIGHT
```

---

For

```text
Index 1
```

Need

```text
1×3×4
```

Notice

```text
Left Part

×

Right Part
```

---

For

```text
Index 2
```

Need

```text
1×2×4
```

Again

```text
Left

×

Right
```

---

For

```text
Index 3
```

Need

```text
1×2×3
```

Again

```text
Left

×

Right
```

This observation is the biggest hint in the entire problem.

---

# First Thought (Brute Force)

The simplest idea is

For every index,

multiply every other element.

---

## Algorithm

For every position

```text
i
```

Traverse the whole array.

Skip

```text
nums[i]
```

Multiply all remaining numbers.

Store the answer.

Repeat for every index.

---

## Dry Run

```text
nums

[1,2,3,4]

------------------

Index 0

Multiply

2×3×4

↓

24

------------------

Index 1

Multiply

1×3×4

↓

12

------------------

Index 2

Multiply

1×2×4

↓

8

------------------

Index 3

Multiply

1×2×3

↓

6
```

Answer

```text
[24,12,8,6]
```

---

## Time Complexity

Outer Loop

```text
O(n)
```

Inner Loop

```text
O(n)
```

Total

```text
O(n²)
```

---

## Space Complexity

```text
O(1)
```

(Excluding the answer array.)

---

# Second Thought — Division

Most people (including me) immediately think:

```text
Find Product of Entire Array

↓

Divide by Current Number
```

Example

```text
nums

[1,2,3,4]
```

Total Product

```text
24
```

Then

```text
24÷1 = 24

24÷2 = 12

24÷3 = 8

24÷4 = 6
```

Looks perfect.

---

# Why Does It Fail?

## Problem 1

The problem explicitly says

```text
Do NOT use Division.
```

So this approach is rejected.

---

## Problem 2

Division completely breaks when zeros appear.

Example

```text
nums

[1,2,0,4]
```

Total Product

```text
0
```

Now

```text
0 ÷ 0
```

is impossible.

---

Another example

```text
nums

[0,2,0,4]
```

Now there are

```text
Two zeros.
```

The logic becomes even more complicated.

Handling all zero cases separately makes the solution messy.

This is exactly why interviewers forbid division.

---

# What Did I Initially Try?

My first idea was exactly this.

```text
Calculate Total Product

↓

Divide by Current Number
```

Then I tried handling

```text
If product == 0

↓

Return 0
```

or

```text
If nums[i] == 0

↓

Return product
```

But this only works for a few cases.

It completely fails when multiple zeros appear.

More importantly,

it violates the problem requirement.

---

# The Real Observation

Forget the total product.

Instead,

look at one index.

Example

```text
nums

[1,2,3,4]
```

Suppose we want the answer for

```text
Index 2
```

Need

```text
1×2×4
```

Split it.

```text
Left Side

1×2

=

2

-------------------

Right Side

4

-------------------

Answer

2×4

=

8
```

---

Another example

```text
Index 1
```

Need

```text
1×3×4
```

Split again.

```text
Left Product

1

----------------

Right Product

3×4

=

12

----------------

Answer

1×12

=

12
```

Interesting...

Every answer can be written as

```text
Left Product

×

Right Product
```

---

# Pattern Explanation

This problem introduces a completely new pattern.

Until now,

we learned

```text
Running Sum

↓

Prefix Sum
```

Now,

instead of sums,

we work with

```text
Running Product

↓

Prefix Product

↓

Suffix Product
```

Think about

```text
nums

[1,2,3,4]
```

Left Products

```text
1

1

2

6
```

Meaning

```text
Everything BEFORE me
```

---

Right Products

```text
24

12

4

1
```

Meaning

```text
Everything AFTER me
```

Finally,

```text
Answer

=

Left Product

×

Right Product
```

This idea completely avoids

- Division
- Zero problems
- Nested loops

---

# Key Insight

Whenever a question asks

```text
Everything except the current element
```

Don't think

```text
Total Product
```

Instead think

```text
Everything on the LEFT

×

Everything on the RIGHT
```

This single observation transforms the problem from

```text
O(n²)

↓

O(n)
```

and introduces one of the most important interview patterns:

```text
Prefix Product

+

Suffix Product
```

---

# What I Learned From Part 1

- Brute force is simple but too slow.
- Division seems correct but violates the problem requirements.
- Zero values make division unreliable.
- Instead of thinking about the whole array, think about **left** and **right** of each index.
- The solution is based on **Prefix Product** and **Suffix Product**, not total product.
- This problem is one of the most famous interview questions because it teaches you to break a problem into reusable patterns instead of relying on arithmetic shortcuts.

---

# LeetCode #238 — Product of Array Except Self (Part 2)

---

# Approach 3 — Prefix Product + Suffix Product (My Accepted Solution)

This is the first **O(n)** solution that I discovered after struggling with the problem for almost **4 hours**.

Instead of using division,

I built two arrays.

- Left Product Array
- Right Product Array

Then multiplied them together.

Although this is **not the most space-optimized solution**, it is completely correct and accepted.

Tomorrow I'll optimize it to the **O(1) Extra Space** solution.

---

# Intuition

Instead of asking

```text
What is the product of the whole array?
```

Ask

```text
For every index,

What is the product of everything

LEFT

and

RIGHT
```

Example

```text
nums

[1,2,3,4]
```

For

```text
Index 2
```

Need

```text
1×2×4
```

Break it.

```text
Left

1×2

=

2

--------------

Right

4

--------------

Answer

2×4

=

8
```

Every index follows exactly the same idea.

```text
Answer

=

Left Product

×

Right Product
```

---

# Left Product Array

For

```text
nums

[1,2,3,4]
```

The Left Product stores

```text
Everything BEFORE the current index.
```

Example

```text
Index 0

Nothing

↓

1

----------------

Index 1

1

↓

1

----------------

Index 2

1×2

↓

2

----------------

Index 3

1×2×3

↓

6
```

Left Array

```text
[1,1,2,6]
```

---

# Right Product Array

Now move from

```text
RIGHT

↓

LEFT
```

Store

```text
Everything AFTER the current index.
```

Example

```text
Index 3

Nothing

↓

1

----------------

Index 2

4

↓

4

----------------

Index 1

3×4

↓

12

----------------

Index 0

2×3×4

↓

24
```

Right Array

```text
[24,12,4,1]
```

---

# Final Answer

Multiply

```text
Left

×

Right
```

```text
Left

[1,1,2,6]

Right

[24,12,4,1]

↓

Answer

24

12

8

6
```

---

# Algorithm

## Step 1

Create the Left Product array.

---

## Step 2

Create the Right Product array.

---

## Step 3

Traverse both arrays.

Multiply

```text
Left[i]

×

Right[i]
```

Store inside Answer.

---

## Code

```python
class Solution(object):

    def productExceptSelf(self, nums):

        answer = []

        left = []

        right = [1] * len(nums)

        for i in range(len(nums)):

            if i == 0:
                left_product = 1

            else:
                left_product *= nums[i-1]

            left.append(left_product)

        for i in reversed(range(len(nums))):

            if i == len(nums)-1:
                right_product = 1

            else:
                right_product *= nums[i+1]

            right[i] = right_product

        for i in range(len(nums)):

            answer.append(left[i] * right[i])

        return answer
```

---

# Complete Dry Run

Input

```text
nums

[1,2,3,4]
```

---

## First Pass

Build Left Array

Initially

```text
left_product = 1

left = []
```

---

### i = 0

Nothing on left.

```text
left

[1]
```

---

### i = 1

```text
1
```

```text
left

[1,1]
```

---

### i = 2

```text
1×2

↓

2
```

```text
left

[1,1,2]
```

---

### i = 3

```text
1×2×3

↓

6
```

```text
left

[1,1,2,6]
```

---

## Second Pass

Build Right Array

Initially

```text
right_product = 1

right

[1,1,1,1]
```

---

### i = 3

Nothing on right.

```text
right

[1,1,1,1]
```

---

### i = 2

```text
4
```

```text
right

[1,1,4,1]
```

---

### i = 1

```text
3×4

↓

12
```

```text
right

[1,12,4,1]
```

---

### i = 0

```text
2×3×4

↓

24
```

```text
right

[24,12,4,1]
```

---

## Third Pass

Multiply

```text
24 × 1

↓

24
```

---

```text
12 × 1

↓

12
```

---

```text
4 × 2

↓

8
```

---

```text
1 × 6

↓

6
```

Answer

```text
[24,12,8,6]
```

---

# Complexity Analysis

## Time Complexity

First Pass

```text
O(n)
```

Second Pass

```text
O(n)
```

Third Pass

```text
O(n)
```

Total

```text
O(3n)

↓

O(n)
```

---

## Space Complexity

Left Array

```text
O(n)
```

Right Array

```text
O(n)
```

Answer Array

```text
O(n)
```

Overall

```text
O(n)
```

(Answer array is required by the problem.)

---

# Mistakes I Made During My 4-Hour Struggle

## Mistake 1

I immediately thought

```text
Product of all numbers

↓

Divide
```

I completely ignored the condition

```text
No Division
```

---

## Mistake 2

I tried handling

```text
If Product == 0
```

But multiple zeros completely broke my logic.

---

## Mistake 3

I tried calculating

Left Product

and

Right Product

inside the same loop.

Later I realized

```text
Right Product

cannot be known

until we actually visit

the right side.
```

So

two passes

are necessary.

---

## Mistake 4

I stored

```python
left_product
```

inside one variable.

Later I realized

every index needs

its own Left Product.

That is why an array is required.

---

## Mistake 5

The biggest bug.

I wrote

```python
right.append(right_product)
```

while traversing

```text
Right

↓

Left
```

The values were correct,

but the positions became

```text
[1,4,12,24]
```

instead of

```text
[24,12,4,1]
```

Finally,

I understood

I should place the value

directly at

```python
right[i]
```

instead of using

```python
append()
```

---

# Biggest Lesson

The answer wasn't difficult.

The thinking process was.

The biggest realization was

```text
Product Except Self

≠

Whole Product
```

Instead

```text
Everything Left

×

Everything Right
```

---

# Pattern Learned

```text
Array

↓

Prefix Product

↓

Suffix Product

↓

Combine

↓

Answer
```

---

# Interview Notes

This is one of the most famous interview questions.

It tests

- Prefix Thinking
- Suffix Thinking
- Array Traversal
- Space Optimization
- Problem Decomposition

Most candidates first think about

```text
Division
```

Strong candidates notice

```text
Left

+

Right
```

Excellent candidates further optimize

the extra space.

---

# My Learning Journey

Time Taken

```text
Nearly 4 Hours
```

During those four hours I learned

- Why division is not enough.
- Why zero breaks division.
- Why Left Product and Right Product work.
- Why Right Product must be built from right to left.
- Why storing values at the correct index matters.
- Why patterns are more important than memorizing solutions.

This problem taught me much more than just one algorithm.

It taught me a new way of thinking.

---

# LeetCode Submission

## Intuition

For each index, the answer is the product of all elements to its left and all elements to its right. Instead of using division, precompute the left and right products separately and multiply them together for each position.

## Approach

- Build a Left Product array where each element stores the product of all elements before the current index.
- Build a Right Product array by traversing from right to left, where each element stores the product of all elements after the current index.
- Multiply the corresponding values from both arrays to obtain the final answer.

## Complexity

- **Time Complexity:** `O(n)`
- **Space Complexity:** `O(n)`

---

# Next Improvement (Tomorrow)

Tomorrow's goal is to optimize this solution.

Current

```text
Left Array

+

Right Array

+

Answer
```

Tomorrow

```text
Answer Array

+

One Variable

↓

O(1) Extra Space
```

That version is the optimal interview solution and builds directly on the understanding gained from this approach.