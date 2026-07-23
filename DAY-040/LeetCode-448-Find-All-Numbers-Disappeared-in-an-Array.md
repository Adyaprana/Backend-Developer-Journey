# LeetCode #448 — Find All Numbers Disappeared in an Array

## Problem Statement

Given an integer array `nums` of size `n`, where:

- `1 <= nums[i] <= n`
- Some elements appear **once**.
- Some elements appear **twice**.

Return **all the integers** in the range `[1, n]` that **do not appear** in the array.

You must solve it in **O(n)** time and **without using extra space** (excluding the returned answer array).

---

## Example 1

```text
Input:
nums = [4,3,2,7,8,2,3,1]

Output:
[5,6]
```

### Explanation

The array length is **8**, so the numbers should be:

```text
1 2 3 4 5 6 7 8
```

Present numbers:

```text
1 ✓
2 ✓
3 ✓
4 ✓
5 ✗
6 ✗
7 ✓
8 ✓
```

Missing numbers are:

```text
[5,6]
```

---

## Example 2

```text
Input:
nums = [1,1]

Output:
[2]
```

---

# Understanding the Problem

The question is **not** asking us to sort the array.

The question is **not** asking us to remove duplicates.

It simply asks:

> Which numbers from **1 to n** are missing from the array?

Think of it like this:

```text
Expected Numbers

1
2
3
4
5
6
7
8

↓

Array

4
3
2
7
8
2
3
1

↓

Missing Numbers

5
6
```

---

# Approach 1 — Brute Force

## Intuition

Check every number from **1** to **n**.

For every number, search whether it exists inside the array.

If it doesn't exist, add it to the answer.

---

## Algorithm

1. Create an empty answer list.
2. Traverse numbers from `1` to `n`.
3. Check whether the current number exists in the array.
4. If not, add it to the answer.
5. Return the answer.

---

## Code

```python
class Solution(object):
    def findDisappearedNumbers(self, nums):

        answer = []

        for number in range(1, len(nums)+1):

            if number not in nums:
                answer.append(number)

        return answer
```

---

## Dry Run

```text
nums = [4,3,2,7,8,2,3,1]

Check 1 ✓

Check 2 ✓

Check 3 ✓

Check 4 ✓

Check 5 ✗

answer = [5]

Check 6 ✗

answer = [5,6]

Check 7 ✓

Check 8 ✓

Return

[5,6]
```

---

## Time Complexity

```text
O(n²)
```

Because every search (`number in nums`) takes **O(n)**.

---

## Space Complexity

```text
O(1)
```

(Excluding the output list.)

---

# Approach 2 — HashSet

## Intuition

The expensive operation is:

```python
number in nums
```

Searching inside a list takes **O(n)**.

Instead, convert the array into a **HashSet**.

Searching inside a HashSet takes **O(1)**.

---

## Algorithm

1. Convert the array into a HashSet.
2. Traverse numbers from `1` to `n`.
3. If the number is not inside the HashSet, add it to the answer.
4. Return the answer.

---

## Code

```python
class Solution(object):

    def findDisappearedNumbers(self, nums):

        seen = set(nums)

        answer = []

        for number in range(1, len(nums)+1):

            if number not in seen:
                answer.append(number)

        return answer
```

---

## Dry Run

```text
HashSet

{1,2,3,4,7,8}

Check

1 ✓

2 ✓

3 ✓

4 ✓

5 ✗

6 ✗

7 ✓

8 ✓

Return

[5,6]
```

---

## Time Complexity

```text
O(n)
```

---

## Space Complexity

```text
O(n)
```

Because of the HashSet.

---

# Approach 3 — Index Marking (Optimal)

## Intuition

This is the most important and tricky approach.

The key observation is:

```text
1 <= nums[i] <= n
```

Since every value lies between **1** and **n**, every value can represent an index.

```text
Value      Index

1   →   0

2   →   1

3   →   2

4   →   3

...

n   →   n-1
```

Instead of using another HashSet, we use the **array itself** to store information.

---

# The Main Idea

Suppose

```text
nums =

[4,3,2,7,8,2,3,1]
```

Read the first number:

```text
4
```

Instead of remembering:

> "I have seen 4"

Go to

```text
Index

4 - 1

=

3
```

and make that position negative.

```text
[4,3,2,-7,8,2,3,1]
```

This means:

```text
Number 4 exists.
```

---

Read

```text
3
```

Go to

```text
Index

2
```

Mark it.

```text
[4,3,-2,-7,8,2,3,1]
```

Meaning:

```text
Number 3 exists.
```

Repeat this for every number.

After the first traversal,

every existing number has marked its corresponding index.

---

# Why do we use abs()?

This was the biggest confusion while solving.

Suppose the array becomes

```text
[4,3,-2,-7,8,2,3,1]
```

Now

```python
nums[2]
```

is

```text
-2
```

But the original number is still

```text
2
```

The negative sign is **only a mark**.

If we directly calculate

```python
nums[nums[i]-1]
```

then

```python
nums[-2-1]
```

becomes

```python
nums[-3]
```

which is the wrong index.

Therefore,

every time we calculate the index,

we ignore the sign.

```python
abs(-2)
```

becomes

```text
2
```

Now

```text
2

↓

Index 1
```

Correct.

---

# Why don't we always do

```python
nums[index] = -nums[index]
```

Suppose

```text
nums = [2,2]
```

First `2`

marks

```text
Index 1

↓

-2
```

Perfect.

Now the second `2`

again points to

```text
Index 1
```

If we again do

```text
-(-2)

↓

2
```

The mark disappears.

That is wrong.

Therefore,

before making a value negative,

check:

```python
if nums[index] > 0
```

Only positive numbers should be turned negative.

Negative numbers stay negative forever.

---

# Algorithm

## First Pass

Traverse the array.

For every value:

```text
value
```

Find

```text
index

=

abs(value)-1
```

If that index contains a positive value,

make it negative.

---

## Second Pass

Traverse the array again.

Every position that is still positive

means

that number never appeared.

```text
Index

+

1

=

Missing Number
```

Store it in the answer.

---

## Code

```python
class Solution(object):

    def findDisappearedNumbers(self, nums):

        answer = []

        # First Pass

        for i in range(len(nums)):

            index = abs(nums[i]) - 1

            if nums[index] > 0:
                nums[index] = -nums[index]

        # Second Pass

        for i in range(len(nums)):

            if nums[i] > 0:
                answer.append(i + 1)

        return answer
```

---

## Complete Dry Run

Input

```text
nums =

[4,3,2,7,8,2,3,1]
```

### First Pass (Marking)

```text
Read 4

↓

Mark Index 3

↓

[4,3,2,-7,8,2,3,1]

--------------------------------

Read 3

↓

Mark Index 2

↓

[4,3,-2,-7,8,2,3,1]

--------------------------------

Read 2

↓

Mark Index 1

↓

[4,-3,-2,-7,8,2,3,1]

--------------------------------

Read 7

↓

Mark Index 6

↓

[4,-3,-2,-7,8,2,-3,1]

--------------------------------

Read 8

↓

Mark Index 7

↓

[4,-3,-2,-7,8,2,-3,-1]

--------------------------------

Read 2

Already marked

Skip

--------------------------------

Read 3

Already marked

Skip

--------------------------------

Read 1

↓

Mark Index 0

↓

[-4,-3,-2,-7,8,2,-3,-1]
```

---

### Second Pass

```text
Index 0

Negative

Skip

-----------------

Index 1

Negative

Skip

-----------------

Index 2

Negative

Skip

-----------------

Index 3

Negative

Skip

-----------------

Index 4

Positive

↓

Answer

5

-----------------

Index 5

Positive

↓

Answer

6

-----------------

Index 6

Negative

Skip

-----------------

Index 7

Negative

Skip
```

Return

```text
[5,6]
```

---

# Complexity

## Brute Force

**Time**

```text
O(n²)
```

**Space**

```text
O(1)
```

---

## HashSet

**Time**

```text
O(n)
```

**Space**

```text
O(n)
```

---

## Index Marking (Optimal)

**Time**

```text
O(n)
```

**Space**

```text
O(1)
```

(Excluding the returned answer array.)

---

# Pattern

```text
Array

↓

Index Mapping

↓

Array Marking

↓

In-place Hashing
```

---

# Key Insight

Whenever a problem says:

```text
1 <= nums[i] <= n
```

always ask yourself:

> Can the value itself be used as an index?

If yes,

the array can often act as a HashSet,

allowing an **O(n)** solution without extra memory.

---

# Mistakes I Faced While Solving

### Mistake 1

I made every element negative.

```python
nums[i] = -nums[i]
```

This marks every position, so it doesn't tell us which numbers actually appeared.

---

### Mistake 2

I forgot to use `abs()`.

After marking, values become negative.

Without `abs()`, Python uses negative indexing, leading to incorrect indices.

---

### Mistake 3

I accidentally removed marks by writing:

```python
nums[index] = -nums[index]
```

twice.

The fix was:

```python
if nums[index] > 0:
```

Only convert positive values to negative.

---

### Mistake 4

I tried to find missing numbers during the marking pass.

The correct approach is:

1. First pass → Mark visited numbers.
2. Second pass → Collect positive indices.

---

# Interview Notes

- Very common in-place array marking pattern.
- No extra HashSet required.
- Learn the relationship:
  - Value → Index
  - Index → Missing Number
- Always use `abs()` while reading values.
- Mark only once by checking `nums[index] > 0`.
- Frequently reused in problems like:
  - 448. Find All Numbers Disappeared in an Array
  - 442. Find All Duplicates in an Array
  - 41. First Missing Positive (advanced variation)

---

# LeetCode Submission

## Intuition

Since every number is in the range `[1, n]`, each value can represent an index. Use the input array itself to mark which numbers have appeared by making the corresponding index negative. After marking, any index that still contains a positive value represents a missing number.

## Approach

- Traverse the array and use `abs(nums[i]) - 1` to find the corresponding index.
- If the value at that index is positive, make it negative to mark that the number exists.
- Traverse the array again.
- Every positive value indicates its corresponding number (`index + 1`) is missing.

## Complexity

- **Time Complexity:** `O(n)`
- **Space Complexity:** `O(1)` (excluding the output array)