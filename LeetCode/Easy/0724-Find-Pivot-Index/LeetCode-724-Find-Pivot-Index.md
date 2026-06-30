# LeetCode #724 — Find Pivot Index

# 📌 Problem Overview

## Problem Statement

Given an integer array `nums`, return the **pivot index**.

The pivot index is the index where:

* The sum of all the numbers **strictly to the left** equals
* The sum of all the numbers **strictly to the right**.

If multiple pivot indexes exist, return the **leftmost** one.

If no pivot index exists, return `-1`.

---

## Examples

### Example 1

```python
Input:
nums = [1,7,3,6,5,6]

Output:
3
```

Explanation:

```
Left  = 1 + 7 + 3 = 11

Right = 5 + 6 = 11
```

Both sums are equal.

Therefore,

```
Pivot Index = 3
```

---

### Example 2

```python
Input:
nums = [1,2,3]

Output:
-1
```

No index satisfies the condition.

---

### Example 3

```python
Input:
nums = [2,1,-1]

Output:
0
```

Left Sum:

```
0
```

Right Sum:

```
1 + (-1) = 0
```

Equal.

---

# Constraints

```
1 <= nums.length <= 10^4

-1000 <= nums[i] <= 1000
```

---

# 🎯 What is a Pivot Index?

Think of the array as balancing on one point.

```
Left Sum  |  Pivot  |  Right Sum
```

If both sides have the same total weight,

that index is the Pivot Index.

Example:

```
1   7   3   6   5   6
        ↑
```

At index 3

```
Left

1 + 7 + 3 = 11

Right

5 + 6 = 11
```

Balanced.

---

# 🚨 Important Observation

The pivot element **is NOT included** in either sum.

For

```
1 7 3 [6] 5 6
```

Left

```
1 + 7 + 3
```

Right

```
5 + 6
```

NOT

```
1 + 7 + 3 + 6

or

6 + 5 + 6
```

This is the biggest mistake beginners make.

---

# 🧠 Understanding the Problem

Suppose

```python
nums = [1,7,3,6,5,6]
```

Check every index.

---

## Index = 0

```
Left

0

Right

7+3+6+5+6

Not Equal
```

---

## Index = 1

```
Left

1

Right

3+6+5+6

Not Equal
```

---

## Index = 2

```
Left

1+7

Right

6+5+6

Not Equal
```

---

## Index = 3

```
Left

1+7+3 = 11

Right

5+6 =11

Equal
```

Return

```
3
```

---

# ✅ Approach 1 — Brute Force

## Intuition

For every index,

calculate

```
Left Sum

and

Right Sum
```

If both sums are equal,

return the current index.

Otherwise,

continue checking.

---

# Algorithm

For every index

```
Calculate

Left Sum

↓

Calculate

Right Sum

↓

Compare

↓

Return index if equal
```

---

# Brute Force Code

```python
class Solution(object):
    def pivotIndex(self, nums):

        for i in range(len(nums)):

            l_sum = sum(nums[:i])
            r_sum = sum(nums[i+1:])

            if l_sum == r_sum:
                return i

        return -1
```

---

# Dry Run

Input

```python
nums = [1,7,3,6,5,6]
```

---

### i = 0

```
Left

0

Right

7+3+6+5+6

Not Equal
```

---

### i =1

```
Left

1

Right

3+6+5+6

Not Equal
```

---

### i =2

```
Left

1+7 =8

Right

6+5+6 =17

Not Equal
```

---

### i =3

```
Left

1+7+3=11

Right

5+6=11

Equal

Return 3
```

---

# ✅ Why This Works

At every index we independently calculate:

```
Left Sum

Right Sum
```

If

```
Left == Right
```

then that index satisfies the Pivot Index definition.

---

# ❌ Why Brute Force is Slow

Look carefully.

For every index,

we call

```python
sum(nums[:i])

sum(nums[i+1:])
```

Again and again.

Example

```
Index 0

Right

7+3+6+5+6
```

Next iteration

```
Index1

Right

3+6+5+6
```

Next

```
Index2

Right

6+5+6
```

Notice something?

We already calculated almost all of these numbers.

Yet Python recalculates everything from scratch.

That means we repeat the same work many times.

---

# Time Complexity

Outer Loop

```
O(n)
```

Each

```
sum()
```

takes

```
O(n)
```

Overall

```
O(n²)
```

---

# Space Complexity

```
O(1)
```

(Interview analysis ignores Python slicing overhead.)

---

# 🚀 Prefix Sum Intuition (How We Discovered It)

While solving the brute-force solution, we noticed something important.

Every iteration recalculated the same sums repeatedly.

Example

```
Left

0

↓

1

↓

1+7

↓

1+7+3

↓

1+7+3+6
```

Instead of recalculating

```
1+7+3
```

again,

we can simply

```
add one new element.
```

The Left Sum keeps **growing**.

---

Now observe the Right Sum.

```
7+3+6+5+6

↓

3+6+5+6

↓

6+5+6

↓

5+6

↓

6

↓

0
```

Instead of recalculating,

we can simply

```
remove one element
```

every iteration.

The Right Sum keeps **shrinking**.

---

This gives us the key insight.

Instead of computing sums repeatedly,

maintain two running sums.

```
Left Sum

← grows

Right Sum

← shrinks
```

Now every iteration only updates two integers.

No repeated calculations.

---

# ⭐ The Most Important Discovery

The order of updates is critical.

At every index,

the Pivot element must belong to neither side.

So the correct order becomes:

```
Right Sum

↓

Remove Current Pivot

↓

Compare

↓

Add Pivot to Left Sum

↓

Move to Next Index
```

Why?

Suppose the current element is the Pivot.

```
Left | Pivot | Right
```

Before comparing,

remove the Pivot from the Right.

Now

```
Left

Pivot

Right
```

The Pivot belongs to neither side.

Compare.

Finally,

move the Pivot into the Left side

for the next iteration.

This transforms the brute-force

```
O(n²)
```

solution into an

```
O(n)
```

Prefix Sum solution.


# ✅ Approach 2 — Prefix Sum (Optimal Solution)

## Intuition

Instead of calculating the left and right sums from scratch for every index, we can reuse previously computed information.

The idea is simple:

* Maintain a running **Left Sum**.
* Maintain a running **Right Sum**.
* Initially, the Right Sum is the sum of the entire array.
* At every index:

  1. Remove the current element from the Right Sum.
  2. Compare Left Sum and Right Sum.
  3. Add the current element to the Left Sum.

This avoids repeated calculations and reduces the complexity from **O(n²)** to **O(n)**.

---

# Algorithm

1. Calculate the total sum of the array.
2. Initialize:

   * `left_sum = 0`
   * `right_sum = total_sum`
3. Traverse the array.
4. Remove the current element from `right_sum`.
5. Compare:

   * If `left_sum == right_sum`, return the current index.
6. Add the current element to `left_sum`.
7. Continue.
8. If no pivot is found, return `-1`.

---

# Optimal Prefix Sum Code (Submitted Solution)

```python
class Solution(object):
    def pivotIndex(self, nums):

        l_sum = 0
        r_sum = sum(nums)

        for i in range(len(nums)):

            r_sum -= nums[i]

            if l_sum == r_sum:
                return i

            l_sum += nums[i]

        return -1
```

---

# Complete Dry Run

Input

```python
nums = [1,7,3,6,5,6]
```

Initial

```text
Left Sum  = 0

Right Sum = 28
```

---

| Index | Pivot | Left Sum | Right Sum (after removing pivot) |   Equal?   |
| ----: | ----: | -------: | -------------------------------: | :--------: |
|     0 |     1 |        0 |                               27 |      ❌     |
|     1 |     7 |        1 |                               20 |      ❌     |
|     2 |     3 |        8 |                               17 |      ❌     |
|     3 |     6 |       11 |                               11 | ✅ Return 3 |

---

# Step-by-Step Visualization

Start

```text
Left = 0

Right = 28
```

---

### Index 0

```text
Left | Pivot | Right

0 | 1 | 7+3+6+5+6

Left = 0

Right = 27
```

Not Equal

Move Pivot to Left

```text
Left = 1
```

---

### Index 1

```text
Left | Pivot | Right

1 | 7 | 3+6+5+6

Left = 1

Right = 20
```

Not Equal

Move Pivot

```text
Left = 8
```

---

### Index 2

```text
Left | Pivot | Right

1+7 | 3 | 6+5+6

Left = 8

Right = 17
```

Not Equal

Move Pivot

```text
Left = 11
```

---

### Index 3

```text
Left | Pivot | Right

1+7+3 | 6 | 5+6

Left = 11

Right = 11
```

Equal

Return

```text
3
```

---

# Why the Order Matters

The correct order is:

```text
Remove Pivot from Right

↓

Compare Left and Right

↓

Move Pivot to Left
```

Suppose we add the Pivot to the Left first.

Then the Pivot becomes part of the Left Sum, which violates the definition of a Pivot Index.

Similarly, if we compare before removing it from the Right, the Pivot incorrectly becomes part of the Right Sum.

Therefore, the update order is essential.

---

# Visualization

```
Iteration 0

Left | Pivot | Right

0 | 1 | 7+3+6+5+6

↓

Iteration 1

1 | 7 | 3+6+5+6

↓

Iteration 2

1+7 | 3 | 6+5+6

↓

Iteration 3

1+7+3 | 6 | 5+6

↓

Pivot Found
```

---

# Complexity Analysis

## Brute Force

Time Complexity

```text
O(n²)
```

Space Complexity

```text
O(1)
```

---

## Prefix Sum

Time Complexity

```text
O(n)
```

Space Complexity

```text
O(1)
```

---

# Comparison of Approaches

| Approach    | Time  | Space |
| ----------- | ----- | ----- |
| Brute Force | O(n²) | O(1)  |
| Prefix Sum  | O(n)  | O(1)  |

---

# Interview Notes

This problem is one of the classic introductions to the **Prefix Sum** pattern.

Interviewers expect candidates to recognize repeated summation and optimize it using running sums.

The same pattern appears in many important interview questions.

Examples:

* LeetCode #560 — Subarray Sum Equals K
* LeetCode #303 — Range Sum Query
* LeetCode #1480 — Running Sum of 1D Array
* LeetCode #238 — Product of Array Except Self (similar left/right accumulation idea)

Mastering this problem makes those questions much easier.

---

# Patterns Learned

* Prefix Sum
* Running Sum
* Left/Right Accumulation
* Space Optimization
* Incremental Computation
* Eliminating Repeated Work

---

# Key Takeaways

* A Pivot Index excludes the pivot element itself.
* Brute Force recalculates the same sums repeatedly.
* Running sums eliminate unnecessary work.
* The order of updating Left and Right sums is crucial.
* Prefix Sum is a reusable interview pattern.

---

# Reflection

Instead of recomputing the left and right sums for every index, I realized both sums can be updated incrementally.

The Left Sum grows by one element after every iteration, while the Right Sum shrinks by removing the current element.

This transforms the brute-force **O(n²)** solution into an **O(n)** Prefix Sum solution by reusing previously computed information.

This problem taught me that recognizing repeated calculations is often the first step toward optimization.

---

# LeetCode Submission Notes

## Intuition

Instead of recalculating the left and right sums for every index, maintain two running sums. Remove the current element from the right sum, compare both sides, and then add the current element to the left sum.

## Approach

1. Compute the total sum of the array.
2. Initialize `left_sum = 0` and `right_sum = total_sum`.
3. Traverse the array.
4. Remove the current element from `right_sum`.
5. If `left_sum == right_sum`, return the current index.
6. Add the current element to `left_sum`.
7. If no pivot exists, return `-1`.

## Complexity

* **Time complexity:** `O(n)`
* **Space complexity:** `O(1)`
