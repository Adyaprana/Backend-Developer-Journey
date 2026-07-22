# LeetCode #414 — Third Maximum Number

## Problem Statement

Given an integer array `nums`, return the **third distinct maximum** number in the array.

If the third distinct maximum does **not** exist, return the **maximum** number.

**Note:** Duplicate values should only be counted once.

---

## Example 1

```text
Input:
nums = [3,2,1]

Output:
1
```

Explanation:

Distinct numbers are:

3, 2, 1

The third maximum is:

1

---

## Example 2

```text
Input:
nums = [1,2]

Output:
2
```

Explanation:

There are only two distinct numbers.

Return the maximum number.

---

## Example 3

```text
Input:
nums = [2,2,3,1]

Output:
1
```

Explanation:

Distinct numbers:

3,2,1

Third maximum = 1
```

---

# Understanding the Problem

The question is **not asking for the third largest element**.

It is asking for the **third distinct largest element**.

Example:

```text
nums = [5,5,4,4,3]

Distinct numbers:

5
4
3

Answer = 3
```

Duplicates are ignored.

---

# Approach 1 — Sorting (Easy to Understand)

## Intuition

Remove duplicate values first.

Then sort the remaining numbers in descending order.

- If there are at least three distinct numbers, return the third one.
- Otherwise, return the largest.

This is the most straightforward solution.

---

## Algorithm

1. Remove duplicates.
2. Sort in descending order.
3. If size < 3
   - return first element.
4. Else
   - return third element.

---

## Code

```python
class Solution(object):
    def thirdMax(self, nums):

        nums = list(dict.fromkeys(nums))

        nums.sort(reverse=True)

        if len(nums) < 3:
            return nums[0]

        return nums[2]
```

---

## Dry Run

```text
nums = [2,2,3,1]

Remove duplicates

↓

[2,3,1]

Sort descending

↓

[3,2,1]

Third maximum

↓

1
```

Return

```text
1
```

---

## Complexity

### Time

```text
O(n log n)
```

Sorting dominates the complexity.

### Space

```text
O(n)
```

Extra space is used to remove duplicates.

---

# Approach 2 — One Pass (Optimal)

## Intuition

We do **not** need to sort the entire array.

We only care about three numbers:

- First Maximum
- Second Maximum
- Third Maximum

Traverse the array only once while maintaining these three values.

Whenever a larger number is found:

- Shift previous maximums down.
- Update the correct position.

Ignore duplicate values.

At the end:

- If third maximum exists → return it.
- Otherwise → return the first maximum.

---

## Algorithm

1. Initialize

```text
first = None
second = None
third = None
```

2. Traverse every number.

3. Ignore duplicates.

4. If number > first

Shift

```text
first → second

second → third
```

Update first.

5. Else if number > second

Shift

```text
second → third
```

Update second.

6. Else if number > third

Update third.

7. Return

```text
third

OR

first
```

depending on whether the third maximum exists.

---

## Code

```python
class Solution(object):
    def thirdMax(self, nums):

        first = None
        second = None
        third = None

        for num in nums:

            if num == first or num == second or num == third:
                continue

            if first is None or num > first:
                third = second
                second = first
                first = num

            elif second is None or num > second:
                third = second
                second = num

            elif third is None or num > third:
                third = num

        return third if third is not None else first
```

---

## Dry Run

```text
nums = [2,2,3,1]
```

Start

```text
First  = None

Second = None

Third  = None
```

---

Read

```text
2
```

```text
First = 2
Second = None
Third = None
```

---

Read

```text
2
```

Duplicate

Skip.

---

Read

```text
3
```

```text
First = 3

Second = 2

Third = None
```

---

Read

```text
1
```

```text
First = 3

Second = 2

Third = 1
```

Return

```text
1
```

---

# Visualization

Suppose

```text
First = 20

Second = 15

Third = 10
```

A new number

```text
25
```

arrives.

Shift

```text
20 → Second

15 → Third
```

Result

```text
First = 25

Second = 20

Third = 15
```

---

Another number

```text
17
```

arrives.

```text
17 > Second ?

Yes
```

Shift

```text
15 → Third
```

Result

```text
First = 25

Second = 17

Third = 15
```

---

# Time Complexity

## Sorting

```text
O(n log n)
```

## Optimal

```text
O(n)
```

---

# Space Complexity

## Sorting

```text
O(n)
```

## Optimal

```text
O(1)
```

---

# Pattern

```text
Array

↓

Top K Elements

↓

Tracking Maximum Values

↓

One Pass Traversal
```

---

# Key Insight

Sorting the entire array is unnecessary.

The problem only asks for the **top three distinct numbers**.

Maintain those three values while traversing once.

Whenever a larger number appears, shift the previous maximum values accordingly.

This reduces the complexity from **O(n log n)** to **O(n)**.

---

# Interview Notes

- Very common "Top K Elements" pattern.
- Distinct values only.
- Do not sort if asked for the optimal solution.
- Learn how to maintain multiple maximum values.
- Good introduction to one-pass tracking algorithms.

---

# LeetCode Submission

## Intuition

Instead of sorting the entire array, maintain the first, second, and third distinct maximum values while traversing the array once. Ignore duplicates and update the three maximum values whenever a larger number is found.

## Approach

Use three variables (`first`, `second`, and `third`) to track the largest distinct numbers.

- Skip duplicate values.
- If the current number is larger than `first`, shift `first` to `second` and `second` to `third`.
- Otherwise, update `second` or `third` if appropriate.
- Return `third` if it exists; otherwise return `first`.

## Complexity

- **Time complexity:** `O(n)`

- **Space complexity:** `O(1)`