# LeetCode #88 — Merge Sorted Array

---

# Problem Statement

You are given two integer arrays `nums1` and `nums2`, sorted in non-decreasing order.

- `nums1` has a length of `m + n`.
- The first `m` elements are valid.
- The last `n` elements are empty spaces (represented by `0`) reserved for merging.
- `nums2` has `n` valid elements.

Merge `nums2` into `nums1` so that the final array is also sorted.

The merge must be done **in-place**.

---

# Examples

## Example 1

```text
Input

nums1 = [1,2,3,0,0,0]

m = 3

nums2 = [2,5,6]

n = 3
```

Output

```text
[1,2,2,3,5,6]
```

---

## Example 2

```text
Input

nums1 = [1]

m = 1

nums2 = []

n = 0
```

Output

```text
[1]
```

---

## Example 3

```text
Input

nums1 = [0]

m = 0

nums2 = [1]

n = 1
```

Output

```text
[1]
```

---

# Constraints

```text
nums1.length == m + n

nums2.length == n

0 <= m,n <= 200

-10⁹ <= nums1[i], nums2[i] <= 10⁹
```

---

# Understanding the Problem

This is the first thing that confuses almost everyone.

Suppose

```text
nums1 = [1,2,3,0,0,0]

m = 3
```

Many beginners think

```text
nums1

↓

1 2 3 0 0 0
```

contains six valid numbers.

It doesn't.

Only

```text
1

2

3
```

are valid.

The last three zeros are **not real data**.

They are simply **empty spaces reserved for nums2**.

A better way to visualize it is

```text
nums1

1 2 3 _ _ _
```

where

```text
_
```

means

```
Empty Space
```

---

# What Is the Problem Asking?

We already have two sorted arrays.

```text
nums1

1 2 3
```

```text
nums2

2 5 6
```

The goal is to merge them into one sorted array.

```text
1 2 2 3 5 6
```

without creating another array.

---

# Important Observations

### Observation 1

Both arrays are already sorted.

We should use that information.

Sorting again wastes time.

---

### Observation 2

The extra zeros inside `nums1` are placeholders.

They are not actual values.

Think of them as

```text
Empty Boxes
```

waiting to be filled.

---

### Observation 3

The problem requires

```text
In-place
```

This means

```
Modify nums1 itself.

Do not create another array.
```

---

### Observation 4

The final array must remain sorted.

Simply appending `nums2` is not enough.

Example

```text
1 2 3

+

2 5 6
```

becomes

```text
1 2 3 2 5 6
```

which is not sorted.

---

# First Attempt — Append + Sort

A very common beginner idea is

1. Copy all elements of `nums2` into the empty spaces.
2. Sort the entire array.

Example

Initially

```text
1 2 3 _ _ _
```

Copy

```text
2 5 6
```

Result

```text
1 2 3 2 5 6
```

Sort

```text
1 2 2 3 5 6
```

This works.

---

# Why Isn't It the Best Solution?

Because we are ignoring an important fact.

Both arrays are already sorted.

Sorting again costs

```text
O((m+n) log(m+n))
```

while the optimal solution takes only

```text
O(m+n)
```

Interviewers expect us to use the sorted property.

---

# Why Doesn't Merging From the Front Work?

Suppose

```text
nums1

1 2 3 _ _ _
```

and

```text
nums2

2 5 6
```

Imagine starting from the front.

The first few values seem easy.

Eventually, we need to place another

```text
2
```

at index `2`.

But index `2` already contains

```text
3
```

If we overwrite it,

```text
1 2 2 _ _ _
```

the original

```text
3
```

is lost before we have a chance to use it.

This is why merging from the front destroys important data.

---

# The Big Observation

Instead of filling

```text
Front

↓

Back
```

what if we fill

```text
Back

↓

Front
```

Why?

Because the back already contains empty spaces.

Example

```text
nums1

1 2 3 _ _ _
```

Compare

```text
3

and

6
```

The larger value

```text
6
```

belongs at the very end.

```text
1 2 3 _ _ 6
```

No useful data is destroyed because the last position was empty.

This observation leads to the optimal solution.

---

# New Pattern Learned

This problem introduces a new Two Pointer pattern.

Instead of reading from the beginning,

we compare the largest remaining elements.

The thinking becomes

```text
Compare

↓

Take Bigger

↓

Place at Last Empty Position

↓

Repeat
```

This pattern is different from the Reader & Writer pattern used in

- Remove Element (#27)
- Move Zeroes (#283)

Here we compare two sorted arrays from the end.

---

# Pattern Connection

```text
Arrays
│
├── Running Sum
│
├── Prefix Sum
│
├── In-place Modification
│
└── Two Pointers (Merge from End)
        │
        └── Merge Sorted Array (#88)
```

---

# Interview Questions

### Q1

Why are the last `n` zeros in `nums1` not considered valid elements?

---

### Q2

Why is sorting after appending not the optimal solution?

---

### Q3

Why does merging from the front overwrite important values?

---

### Q4

Why is merging from the back safer?

---

### Q5

What information given in the problem helps us achieve an O(m+n) solution?

Answer:

```
Both arrays are already sorted.
```

---

# Learning Summary

After solving Part 1, I learned:

- `nums1` contains only the first `m` valid elements.
- The remaining zeros are empty spaces, not real values.
- Simply appending and sorting works but is not optimal.
- Starting from the front can overwrite values that have not been used yet.
- Starting from the back avoids overwriting because the empty spaces are already at the end.
- This problem introduces the **Merge from the End** two-pointer pattern.

---

# Optimal Approach — Three Pointers (Merge From The End)

The main idea is very simple.

Instead of merging from the front,

we merge from the back.

Why?

Because the back of `nums1` already has empty spaces.

Nothing important will be overwritten.

---

# The Three Pointers

We use three pointers.

## Pointer 1 (`p1`)

Points to the **last valid element** of `nums1`.

```python
p1 = m - 1
```

Example

```text
nums1

1 2 3 _ _ _

      ↑
      p1
```

---

## Pointer 2 (`p2`)

Points to the last element of `nums2`.

```python
p2 = n - 1
```

Example

```text
nums2

2 5 6

      ↑
      p2
```

---

## Write Pointer (`write`)

Points to the last position of `nums1`.

```python
write = m + n - 1
```

Example

```text
nums1

1 2 3 _ _ _

          ↑
        write
```

---

# Why Three Pointers?

Each pointer has one responsibility.

```
p1

↓

Current largest remaining number in nums1
```

```
p2

↓

Current largest remaining number in nums2
```

```
write

↓

Where the next largest number should be placed
```

---

# The Main Idea

Every iteration asks only one question.

```
Which number is bigger?

nums1[p1]

or

nums2[p2]
```

The bigger number belongs at

```
write
```

Then move the pointer of the winner.

Finally,

move

```
write
```

one step left.

Repeat.

---

# Why Compare From The End?

Suppose

```text
nums1

1 2 3 _ _ _
```

```text
nums2

2 5 6
```

Largest numbers

```text
3

6
```

Winner

```
6
```

Place it.

```text
1 2 3 _ _ 6
```

Notice

Nothing was destroyed.

The last position was empty.

This is why we merge from the back.

---

# Why Does Only The Winner Move?

Imagine

```
3

vs

6
```

Winner

```
6
```

We already used

```
6
```

So

```
p2
```

moves left.

But

```
3
```

has not been used yet.

Therefore

```
p1
```

stays.

---

Next

```
3

vs

5
```

Winner

```
5
```

Again

```
Move p2
```

---

Next

```
3

vs

2
```

Winner

```
3
```

Now

```
Move p1
```

Rule

```
Winner moves.

Loser waits.
```

---

# Why Does write Always Move?

Every iteration fills exactly one empty position.

So

```
write
```

always moves left.

No exceptions.

---

# Understanding The Condition

```python
if p1 >= 0 and nums1[p1] > nums2[p2]:
```

Let's understand every part.

---

## Part 1

```python
p1 >= 0
```

Meaning

```
Does nums1 still have valid elements?
```

If

```
p1 = -1
```

then

```
nums1
```

has no remaining valid numbers.

We must take numbers only from

```
nums2
```

---

## Part 2

```python
nums1[p1] > nums2[p2]
```

Meaning

```
Which number is bigger?
```

If

```
nums1
```

is bigger,

copy it.

Otherwise,

copy from

```
nums2
```

---

# Complete Algorithm

1. Create three pointers.

```
p1

↓

Last valid element of nums1
```

```
p2

↓

Last element of nums2
```

```
write

↓

Last position of nums1
```

---

2. While `nums2` still has elements

Compare

```
nums1[p1]

and

nums2[p2]
```

---

3. Put the larger element at

```
write
```

---

4. Move the pointer of the larger element.

---

5. Move

```
write
```

---

6. Repeat until

```
nums2
```

is empty.

---

# Final Code

```python
class Solution(object):
    def merge(self, nums1, m, nums2, n):

        p1 = m - 1
        p2 = n - 1
        write = m + n - 1

        while p2 >= 0:

            if p1 >= 0 and nums1[p1] > nums2[p2]:

                nums1[write] = nums1[p1]
                p1 -= 1

            else:

                nums1[write] = nums2[p2]
                p2 -= 1

            write -= 1
```

---

# Complete Dry Run

Input

```text
nums1 = [1,2,3,0,0,0]

nums2 = [2,5,6]
```

Initial pointers

```text
p1 -> 3

p2 -> 6

write -> last
```

---

### Step 1

Compare

```
3

6
```

Winner

```
6
```

```text
1 2 3 _ _ 6
```

Move

```
p2

write
```

---

### Step 2

Compare

```
3

5
```

Winner

```
5
```

```text
1 2 3 _ 5 6
```

Move

```
p2

write
```

---

### Step 3

Compare

```
3

2
```

Winner

```
3
```

```text
1 2 3 3 5 6
```

Move

```
p1

write
```

---

### Step 4

Compare

```
2

2
```

Take from

```
nums2
```

```text
1 2 2 3 5 6
```

Move

```
p2

write
```

---

### Step 5

`nums2` is finished.

Stop.

Final Answer

```text
1 2 2 3 5 6
```

---

# Another Dry Run (Important Edge Case)

Input

```text
nums1 = [4,5,6,0,0,0]

nums2 = [1,2,3]
```

Comparison order

```
6 vs 3

↓

5 vs 3

↓

4 vs 3
```

Eventually

```
p1 = -1
```

Now there are no valid elements left in

```
nums1
```

The remaining

```
3

2

1
```

are copied directly from

```
nums2
```

This is exactly why we check

```python
p1 >= 0
```

before comparing.

---

# Complexity Analysis

## Time Complexity

```
O(m+n)
```

Every element is processed exactly once.

---

## Space Complexity

```
O(1)
```

No extra array is created.

Everything is done inside

```
nums1
```

---

# Common Mistakes

## ❌ Sorting After Merge

```python
nums1.sort()
```

Works,

but slower.

---

## ❌ Merging From The Front

Destroys elements that are still needed.

---

## ❌ Forgetting

```python
p1 >= 0
```

Can access invalid elements after all values from `nums1` have been used.

---

## ❌ Moving The Wrong Pointer

Remember

```
Winner moves.

Loser waits.
```

---

## ❌ Forgetting To Move write

Every iteration fills one position.

So

```
write
```

must always move left.

---

# Pattern Recognition

Whenever you see

```
Two Sorted Arrays

+

Merge In-place
```

Immediately think

```
Three Pointers

↓

Compare From End

↓

Take Bigger

↓

Winner Moves

↓

write Moves

↓

Repeat
```

---

# Interview Questions

### Q1

Why do we merge from the back instead of the front?

---

### Q2

Why do we need three pointers?

---

### Q3

Why does only the winner's pointer move?

---

### Q4

Why does the write pointer always move?

---

### Q5

Why do we check

```python
p1 >= 0
```

before comparing?

---

### Q6

Why is only one loop (`while p2 >= 0`) enough?

---
