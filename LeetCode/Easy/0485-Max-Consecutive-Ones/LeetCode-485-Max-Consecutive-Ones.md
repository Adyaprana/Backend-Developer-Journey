# LeetCode #485 — Max Consecutive Ones

## Problem Understanding

You are given a binary array `nums` containing only `0`s and `1`s.

Your task is to find the maximum number of consecutive `1`s present in the array.

### Example

```text
Input:
nums = [1,1,0,1,1,1]

Output:
3
```

Explanation:

```text
1 1 0 1 1 1
↑ ↑     ↑ ↑ ↑

First consecutive ones = 2
Second consecutive ones = 3

Maximum = 3
```

---

# Approach 1 — Brute Force

## Intuition

For every index, if the element is `1`, continue moving forward until a `0` is found and count the number of consecutive ones.

Repeat this process for every starting position and keep track of the maximum count.

## Algorithm

1. Traverse every index.
2. If the current number is `1`, start counting consecutive ones.
3. Continue until a `0` appears.
4. Update the maximum count.
5. Return the maximum.

## Code

```python
class Solution(object):
    def findMaxConsecutiveOnes(self, nums):
        maximum = 0

        for i in range(len(nums)):
            if nums[i] == 1:
                count = 0
                j = i

                while j < len(nums) and nums[j] == 1:
                    count += 1
                    j += 1

                maximum = max(maximum, count)

        return maximum
```

### Dry Run

```
nums = [1,1,0,1,1,1]

i = 0
Count = 2
Maximum = 2

i = 1
Count = 1
Maximum = 2

i = 2
Skip

i = 3
Count = 3
Maximum = 3

Answer = 3
```

### Complexity

**Time**

```
O(n²)
```

**Space**

```
O(1)
```

---

# Approach 2 — Linear Traversal (Optimal) ✅

## Intuition

Instead of recounting every sequence of `1`s, keep a running count.

Whenever a `1` is found:

- Increase the current count.

Whenever a `0` is found:

- Reset the current count to `0`.

Keep updating the maximum count throughout the traversal.

This allows solving the problem in a single pass.

---

## Algorithm

1. Initialize:

```
count = 0
max_count = 0
```

2. Traverse the array.

3. If the current number is `1`:

- Increment `count`.
- Update `max_count`.

4. Otherwise (`0`):

- Reset `count` to `0`.

5. Return `max_count`.

---

## Code

```python
class Solution(object):
    def findMaxConsecutiveOnes(self, nums):
        count = 0
        max_count = 0

        for num in nums:
            if num == 1:
                count += 1

                if count > max_count:
                    max_count = count

            else:
                count = 0

        return max_count
```

---

## Dry Run

```
nums = [1,1,0,1,1,1]

count = 0
max = 0

1
count = 1
max = 1

1
count = 2
max = 2

0
count = 0

1
count = 1
max = 2

1
count = 2
max = 2

1
count = 3
max = 3

Return 3
```

---

# Time Complexity

```
O(n)
```

Only one traversal of the array.

---

# Space Complexity

```
O(1)
```

Only two variables are used.

---

# Pattern

```
Array
↓

Linear Traversal

↓

Running Counter

↓

Maximum Tracking
```

---

# Key Insight

Instead of checking every possible sequence of `1`s, keep track of the current streak while traversing the array once.

Whenever a `0` appears, the current streak ends, so reset the counter.

The maximum streak encountered during the traversal is the answer.

---

# Interview Notes

- Binary array problem.
- One-pass traversal.
- Running counter pattern.
- Frequently asked easy array question.
- Good introduction to maintaining state during traversal.