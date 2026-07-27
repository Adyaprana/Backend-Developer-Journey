# LeetCode #1480 — Running Sum of 1d Array

---

# Problem Statement

Given an array `nums`.

Return the **running sum** of `nums`.

The **running sum** of an array is defined as:

```text
runningSum[i] = sum(nums[0] ... nums[i])
```

In simple words,

each element in the answer is the sum of all elements from the beginning of the array up to the current index.

---

# Example 1

```text
Input

nums = [1,2,3,4]

Output

[1,3,6,10]
```

Explanation

```text
Index 0

1

----------------

Index 1

1 + 2 = 3

----------------

Index 2

1 + 2 + 3 = 6

----------------

Index 3

1 + 2 + 3 + 4 = 10
```

---

# Example 2

```text
Input

nums = [1,1,1,1,1]

Output

[1,2,3,4,5]
```

---

# Example 3

```text
Input

nums = [3,1,2,10,1]

Output

[3,4,6,16,17]
```

---

# Constraints

```text
1 <= nums.length <= 1000

-10^6 <= nums[i] <= 10^6
```

---

# Understanding the Problem

The question asks us to calculate the **running total** while moving through the array.

Instead of finding the total sum only once,

we must calculate the sum **at every index**.

Example

```text
nums

[1,2,3,4]

↓

Running Sum

Index 0

1

↓

Index 1

1+2

↓

Index 2

1+2+3

↓

Index 3

1+2+3+4

↓

Answer

[1,3,6,10]
```

---

# Visual Representation

```text
nums

1     2     3     4

↓

Running Sum

1

↓

3

↓

6

↓

10
```

---

# Approach 1 — Brute Force

## Intuition

For every index,

calculate the sum from the beginning of the array until that index.

Store the result.

Repeat for every index.

---

## Algorithm

1. Create an empty answer array.
2. Traverse every index.
3. Calculate the sum from index `0` to current index.
4. Store the sum.
5. Return the answer.

---

## Code

```python
class Solution(object):

    def runningSum(self, nums):

        answer = []

        for i in range(len(nums)):

            answer.append(sum(nums[:i+1]))

        return answer
```

---

## Dry Run

```text
nums

[1,2,3,4]

-----------------

i = 0

sum([1])

=

1

Answer

[1]

-----------------

i = 1

sum([1,2])

=

3

Answer

[1,3]

-----------------

i = 2

sum([1,2,3])

=

6

Answer

[1,3,6]

-----------------

i = 3

sum([1,2,3,4])

=

10

Answer

[1,3,6,10]
```

---

## Time Complexity

```text
O(n²)
```

Because every iteration recalculates the sum again.

---

## Space Complexity

```text
O(n)
```

---

# Approach 2 — Prefix Sum (Optimal)

## Intuition

Instead of calculating the previous sum again,

remember it.

The running sum follows a simple relationship.

```text
Current Running Sum

=

Previous Running Sum

+

Current Number
```

Once we know the previous total,

we only need to add the current element.

This avoids recalculating everything.

---

# Key Observation

```text
nums

[1,2,3,4]

Running Sum

1

↓

1+2

↓

1+2+3

↓

1+2+3+4
```

Notice

```text
RunningSum[1]

=

RunningSum[0]

+

nums[1]

------------------

RunningSum[2]

=

RunningSum[1]

+

nums[2]

------------------

RunningSum[3]

=

RunningSum[2]

+

nums[3]
```

We only need to remember the previous sum.

---

# Algorithm

1. Create an empty answer array.
2. Initialize a variable `running_sum = 0`.
3. Traverse the array.
4. Add the current element to `running_sum`.
5. Store `running_sum` in the answer.
6. Return the answer.

---

## Code

```python
class Solution(object):

    def runningSum(self, nums):

        runningSum = []

        running_sum = 0

        for i in range(len(nums)):

            running_sum += nums[i]

            runningSum.append(running_sum)

        return runningSum
```

---

## Dry Run

```text
nums

[1,2,3,4]

Initially

running_sum = 0

answer = []

-----------------

Read 1

running_sum

0 + 1

=

1

answer

[1]

-----------------

Read 2

running_sum

1 + 2

=

3

answer

[1,3]

-----------------

Read 3

running_sum

3 + 3

=

6

answer

[1,3,6]

-----------------

Read 4

running_sum

6 + 4

=

10

answer

[1,3,6,10]

Return
```

---

# Why is this Optimal?

The brute-force approach repeatedly recalculates previous sums.

Example

```text
1

↓

1+2

↓

1+2+3

↓

1+2+3+4
```

The same numbers are added multiple times.

The Prefix Sum approach remembers the previous answer.

Instead of

```text
1+2+3
```

again,

it simply does

```text
Previous Sum

+

Current Number
```

```text
3

+

3

=

6
```

Only one addition is required.

---

# Prefix Sum Concept

```text
Previous Running Sum

↓

Add Current Element

↓

New Running Sum
```

Formula

```text
running_sum

=

running_sum

+

nums[i]
```

This idea is called the **Prefix Sum Pattern**.

---

# Time Complexity

## Brute Force

```text
O(n²)
```

---

## Prefix Sum

```text
O(n)
```

Only one traversal.

---

# Space Complexity

## Brute Force

```text
O(n)
```

---

## Prefix Sum

```text
O(n)
```

---

# Comparison

| Approach | Time | Space | Interview Friendly |
|----------|------|-------|--------------------|
| Brute Force | O(n²) | O(n) | ⭐⭐⭐ |
| Prefix Sum | O(n) | O(n) | ⭐⭐⭐⭐⭐ |

---

# Pattern

```text
Array

↓

Prefix Sum

↓

Running Total

↓

Single Traversal
```

---

# Key Insight

Instead of calculating the previous sum every time,

store it in a variable.

Each new answer is simply

```text
Previous Running Sum

+

Current Element
```

This reduces the complexity from

```text
O(n²)

↓

O(n)
```

---

# Mistakes I Faced While Solving

## Mistake 1

I initialized

```python
runningSum = [] * len(nums)
```

This creates an empty list,

not a list of fixed size.

---

## Mistake 2

I tried

```python
runningSum[i] = ...
```

on an empty list.

The index did not exist.

---

## Mistake 3

I wrote

```python
sum[nums[i]]
```

But `sum` is a function,

not a list.

The correct usage is

```python
sum(...)
```

---

## Mistake 4

I tried to calculate

```python
sum(runningSum)
```

inside every iteration.

This recalculates everything again,

making the algorithm inefficient.

The better approach is to store the previous running total.

---

# What I Learned

Instead of recomputing previous work,

store it.

Many DSA problems become faster by remembering previously computed information.

This is called the **Prefix Sum Pattern**.

---

# Interview Notes

- First Prefix Sum problem.
- Introduces cumulative sum.
- Frequently asked in coding interviews.
- Foundation for many Medium problems.
- Learn the idea of reusing previous computation instead of recalculating it.

Related Problems:

- 724. Find Pivot Index
- 303. Range Sum Query - Immutable
- 560. Subarray Sum Equals K
- 238. Product of Array Except Self

---

# LeetCode Submission

## Intuition

Maintain a running total while traversing the array. Instead of recalculating the sum from the beginning for every index, keep adding the current element to the previous running sum.

## Approach

Initialize a variable to store the running sum.

Traverse the array once:

- Add the current element to the running sum.
- Append the updated running sum to the answer.

Return the resulting array.

## Complexity

- **Time Complexity:** `O(n)`
- **Space Complexity:** `O(n)`