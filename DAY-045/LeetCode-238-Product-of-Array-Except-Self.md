# LeetCode #238 — Product of Array Except Self (Version 2 - Optimal Solution)

---

# Approach 4 — Prefix Product + One Right Product Variable (Optimal)

This is the **optimal interview solution**.

Instead of storing both **Left** and **Right** arrays, we reuse the **answer array** to store the Left Products.

Then, while traversing from **right to left**, we maintain a single variable called `right_product` and multiply it directly with the values already stored in the answer array.

This reduces the **extra space complexity from O(n) to O(1)** (excluding the output array).

---

# Intuition

For every index,

```text
Answer

=

Left Product

×

Right Product
```

Earlier we stored

```text
Left Array

+

Right Array
```

But notice something.

The final answer array is empty at the beginning.

So instead of creating another array,

we can temporarily let

```text
Answer Array

↓

Store Left Products
```

Then,

during the second traversal,

multiply every element by the current

```text
Right Product
```

and directly convert it into the final answer.

---

# Key Observation

Suppose

```text
nums

[1,2,3,4]
```

### First Pass

Store only Left Products.

```text
answer

[1,1,2,6]
```

Notice

This is exactly the Left Product array.

---

### Second Pass

Traverse from right.

Initially

```text
right_product = 1
```

Multiply

```text
answer[i]

×

right_product
```

Then update

```text
right_product

*=

nums[i]
```

Eventually,

```text
answer

↓

[24,12,8,6]
```

No Right Array required.

---

# Algorithm

## Step 1

Create an answer array filled with `1`.

---

## Step 2

Traverse from left to right.

Store the product of all elements before the current index inside the answer array.

---

## Step 3

Initialize

```text
right_product = 1
```

---

## Step 4

Traverse from right to left.

For every index

- Multiply the current answer by `right_product`.
- Update `right_product` by multiplying it with the current number.

---

## Step 5

Return the answer array.

---

# Code

```python
class Solution(object):

    def productExceptSelf(self, nums):

        answer = [1] * len(nums)

        for i in range(len(nums)):

            if i == 0:
                left_product = 1

            else:
                left_product *= nums[i-1]

            answer[i] = left_product

        for i in reversed(range(len(nums))):

            if i == len(nums)-1:
                right_product = 1

            else:
                right_product *= nums[i+1]

            answer[i] *= right_product

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

Initially

```text
left_product = 1

answer

[1,1,1,1]
```

---

### i = 0

Nothing on left.

```text
answer

[1,1,1,1]
```

---

### i = 1

```text
left_product

1
```

```text
answer

[1,1,1,1]
```

---

### i = 2

```text
left_product

1×2

=

2
```

```text
answer

[1,1,2,1]
```

---

### i = 3

```text
left_product

1×2×3

=

6
```

```text
answer

[1,1,2,6]
```

Now,

the answer array stores all Left Products.

---

## Second Pass

Initially

```text
right_product = 1
```

---

### i = 3

```text
answer[3]

=

6×1

=

6
```

Update

```text
right_product

=

1×4

=

4
```

---

### i = 2

```text
answer[2]

=

2×4

=

8
```

Update

```text
right_product

=

4×3

=

12
```

---

### i = 1

```text
answer[1]

=

1×12

=

12
```

Update

```text
right_product

=

12×2

=

24
```

---

### i = 0

```text
answer[0]

=

1×24

=

24
```

Update

```text
right_product

=

24×1

=

24
```

Final Answer

```text
[24,12,8,6]
```

---

# Why Does This Work?

During the first traversal,

the answer array stores

```text
Everything on the LEFT
```

During the second traversal,

the variable

```text
right_product
```

stores

```text
Everything on the RIGHT
```

So,

```text
answer[i]

=

Left Product

×

Right Product
```

without ever creating another array.

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

Total

```text
O(n)
```

---

## Space Complexity

Extra Variables

```text
left_product

right_product
```

Only

```text
O(1)
```

The answer array is required by the problem, so it is **not counted as extra space**.

---

# Why This Is Better Than My Previous Solution

| Previous Solution | Optimal Solution |
|-------------------|------------------|
| Left Array ✅ | Left Array ❌ |
| Right Array ✅ | Right Array ❌ |
| Answer Array ✅ | Answer Array ✅ |
| Extra Space = O(n) | Extra Space = O(1) |
| Three Arrays | One Array + One Variable |

---

# Pattern Learned

```text
Prefix Product

↓

Store in Answer Array

↓

Suffix Product

↓

Single Variable

↓

Combine

↓

Optimal Solution
```

---

# Key Insight

The answer array can temporarily store the Left Products.

Later,

instead of building a complete Right Product array,

we only keep one running variable.

This simple optimization removes an entire array from memory while preserving the same O(n) time complexity.

---

# Interview Notes

This is the **expected solution** in most product-company interviews.

Interviewers want to see whether you can:

- Identify Prefix and Suffix Product patterns.
- Optimize unnecessary auxiliary arrays.
- Reuse the output array for intermediate computation.
- Reduce extra space from O(n) to O(1).

---

# LeetCode Submission

## Intuition

For each index, the required value is the product of all elements to its left and all elements to its right. Store the left products directly in the answer array, then traverse from right to left while maintaining a running right product and combine both values in-place.

## Approach

- Initialize the answer array with `1`s.
- Traverse left to right and store the product of all previous elements in the answer array.
- Traverse right to left while maintaining a running `right_product`.
- Multiply each answer by the current `right_product`.
- Update `right_product` after processing each index.

## Complexity

- **Time Complexity:** `O(n)`
- **Space Complexity:** `O(1)` (excluding the output array)