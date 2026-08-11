# LeetCode #27 — Remove Element

---

# Problem Statement

Given an integer array `nums` and an integer `val`, remove all occurrences of `val` **in-place**.

The relative order of the remaining elements may be changed (although our approach preserves it).

Return the number of elements remaining after removing all occurrences of `val`.

The first `k` elements of `nums` should contain the remaining elements.

The elements beyond the first `k` positions do **not** matter.

---

# Examples

## Example 1

```text
Input:

nums = [3,2,2,3]

val = 3

Output:

2

nums = [2,2,_,_]
```

Explanation

The first two elements are

```
2 2
```

The remaining positions can contain anything.

---

## Example 2

```text
Input

nums = [0,1,2,2,3,0,4,2]

val = 2

Output

5

nums = [0,1,3,0,4,_,_,_]
```

Only the first five elements matter.

---

# Constraints

```
0 <= nums.length <= 100

0 <= nums[i] <= 50

0 <= val <= 100
```

---

# Understanding the Problem

This problem confuses many beginners because of one word:

```
In-place
```

It **does NOT** mean

```
Delete elements from the array.
```

Instead,

it means

```
Modify the same array.

Do not create another array.
```

---

# What Is the Question Asking?

The problem is asking us to

```
Remove every occurrence

of val
```

Example

```
nums

[3,2,2,3]

val = 3
```

After removing

```
3
```

the remaining numbers become

```
2

2
```

Answer

```
2
```

because only

```
2 elements

remain.
```

---

# Important Observation

Many beginners think

```
We have to physically remove the elements.
```

Actually,

we do not.

Suppose

```
nums

[3,2,2,3]
```

After solving,

LeetCode only checks

```
First k elements.
```

Example

```
[2,2,2,3]
```

is completely acceptable.

Why?

Because

```
k = 2
```

Only these positions matter.

```
2

2
```

Everything after that is ignored.

---

# Arrays Have Fixed Size

Unlike Python lists,

arrays have fixed positions.

Suppose

```
Index

0   1   2   3

↓

3   2   2   3
```

Can we simply remove

```
Index 0
```

?

No.

The remaining elements would need to move.

Therefore,

instead of deleting,

we

```
Overwrite
```

the unwanted values.

This is the biggest idea behind this pattern.

---

# Brute Force Idea

The easiest approach is

Whenever we find

```
val
```

Shift every remaining element

one position to the left.

Example

```
3 2 2 3

↓

2 2 3 _
```

Now

effective length

becomes

```
3
```

Continue until the entire array is processed.

---

# Brute Force Algorithm

## Step 1

Traverse the array.

---

## Step 2

Whenever

```
nums[i] == val
```

Shift every element

after it

one position left.

---

## Step 3

Decrease the effective size.

---

## Step 4

Continue scanning until the end.

---

## Step 5

Return the new size.

---

# Brute Force Code

```python
class Solution(object):
    def removeElement(self, nums, val):

        n = len(nums)

        i = 0

        while i < n:

            if nums[i] == val:

                for j in range(i, n - 1):

                    nums[j] = nums[j + 1]

                n -= 1

            else:

                i += 1

        return n
```

---

# Dry Run (Brute Force)

Input

```
nums

[3,2,2,3]

val = 3
```

Initially

```
3 2 2 3
```

---

Remove first

```
3
```

Shift

```
2

↓

Index 0
```

Shift

```
2

↓

Index 1
```

Shift

```
3

↓

Index 2
```

Array

```
2 2 3 _
```

Length

```
3
```

Continue.

---

Again

```
3
```

is found.

Shift

```
Nothing
```

Array

```
2 2 _ _
```

Length

```
2
```

Finished.

Answer

```
2
```

---

# Complexity Analysis (Brute Force)

### Time Complexity

Worst Case

```
O(n²)
```

because every removal may require shifting almost the entire array.

---

### Space Complexity

```
O(1)
```

No extra array is created.

---

# Why Is Brute Force Slow?

Suppose

```
nums

[2,2,2,2,2,2,2]
```

Every time we remove

```
2
```

we shift

almost every remaining element.

```
Shift

↓

Shift

↓

Shift

↓

Shift
```

Many repeated operations.

Therefore,

the algorithm becomes

```
O(n²)
```

---

# A Better Observation

Instead of moving

every bad element,

what if we only move

the good elements?

Think about this.

```
nums

3 2 2 3
```

Ignore

```
3
```

Only keep

```
2

2
```

Instead of deleting,

what if we simply place

the good elements

at the beginning

of the same array?

This idea leads to the

```
In-place Modification Pattern.
```

---

# Introducing the In-place Modification Pattern

This pattern appears in many interview questions.

Instead of creating another array,

we rebuild the answer

inside the original array.

We use

```
Two Pointers
```

One pointer

reads every element.

The other pointer

writes only the valid elements.

This reduces

```
O(n²)

↓

O(n)
```

without using extra space.

---

# Pattern Connection

This is the beginning of a new DSA pattern.

```
Remove Element (#27)

        ↓

Remove Duplicates from Sorted Array (#26)

        ↓

Move Zeroes (#283)

        ↓

Sort Array By Parity (#905)

        ↓

Duplicate Zeros (#1089)
```

All these problems use the same

```
Reader + Writer
```

thinking.

---

# Interview Questions

### Q1

What does

```
In-place
```

mean?

---

### Q2

Why can't we directly delete elements from an array?

---

### Q3

Why does shifting make the brute-force solution

```
O(n²)?
```

---

### Q4

Does LeetCode care about the values after the first `k` elements?

---

### Q5

What idea can reduce the complexity from

```
O(n²)

↓

O(n)?
```

Answer

```
Move only the good elements,

instead of shifting every bad one.
```

---

# Learning Summary

After solving this part, I learned:

- What "in-place" modification really means.
- Arrays cannot physically remove elements.
- The first `k` positions are the only ones that matter.
- Brute force works by repeatedly shifting elements.
- Repeated shifting makes the algorithm O(n²).
- A better idea is to move only the valid elements.
- This problem introduces the **In-place Modification** pattern, which will be reused in many upcoming array problems.

---

# Optimal Approach — Two Pointers (Reader & Writer)

Instead of shifting every unwanted element,

we use **two pointers**.

One pointer reads every element.

The other pointer writes only the valid elements.

This is called the **Reader & Writer Pattern**.

It is one of the most common **In-place Modification** techniques used in interviews.

---

# The Reader & Writer Analogy

Imagine two people working together.

## 👀 Reader (`i`)

The Reader's only job is

```
Look at every element.
```

He never writes.

He never modifies the array.

He simply checks

```
Is this element good or bad?
```

---

## ✍️ Writer (`k`)

The Writer's only job is

```
Write good elements.
```

The Writer never searches.

The Writer only copies the elements that the Reader approves.

---

# Initial State

Example

```
nums = [3,2,2,3]

val = 3
```

Initially

```
Index

0   1   2   3

↓

3   2   2   3

↑
k

↑
i
```

Both pointers start at index `0`.

---

# Step 1

Reader looks at

```
3
```

Question

```
Should we keep it?
```

```
3 == val

↓

YES
```

This means

```
Bad element.
```

Reader skips it.

Writer does nothing.

Pointers become

```
3   2   2   3

↑
k

    ↑
    i
```

Notice

Writer did not move.

---

# Step 2

Reader now sees

```
2
```

Question

```
Should we keep it?
```

```
2 == 3 ?

↓

NO
```

This is a good element.

Writer copies it.

```
nums[k] = nums[i]
```

means

```
nums[0] = nums[1]
```

Array becomes

```
2   2   2   3
```

Writer moves.

```
2   2   2   3

    ↑
    k

        ↑
        i
```

---

# Step 3

Reader sees

```
2
```

Again

Good element.

Writer copies

```
nums[1] = nums[2]
```

Array

```
2   2   2   3
```

Writer moves.

```
2   2   2   3

        ↑
        k

            ↑
            i
```

---

# Step 4

Reader sees

```
3
```

Bad element.

Skip it.

Reader reaches the end.

Finished.

---

# Final Array

```
2   2   2   3
```

Writer stopped at

```
k = 2
```

This means

```
Only first two positions

are valid.
```

LeetCode ignores everything after index `1`.

So we return

```
2
```

---

# Understanding

```python
nums[k] = nums[i]
```

This is the most important line.

Never memorize it.

Read it like English.

```
Copy the good element

that Reader found

into the next free position

where Writer is standing.
```

That's all it means.

---

# Why Does Reader Always Move?

Reader's job is

```
Inspect every element.
```

If Reader stops,

we will never reach the end.

Therefore

Reader always moves.

Rule

```
Reader

Always Moves
```

---

# Why Doesn't Writer Always Move?

Suppose Reader finds

```
3
```

Should Writer copy it?

```
No.
```

Then why move?

There is nothing to write.

Writer only moves

after successfully writing

a valid element.

Rule

```
Good Element

↓

Write

↓

Move Writer
```

Bad Element

↓

```
Skip

↓

Writer Stays
```

---

# Why Return `k`?

At the end

```
2   2   2   3

        ↑

        k
```

Writer has written

```
2

valid elements.
```

Therefore

```
k

=

New Length
```

Return

```python
return k
```

---

# Complete Algorithm

Step 1

Create

```
Writer = 0
```

---

Step 2

Traverse the array using Reader.

---

Step 3

If

```
Current element

!= val
```

copy it

to Writer's position.

---

Step 4

Move Writer.

---

Step 5

Continue until Reader reaches the end.

---

Step 6

Return Writer.

---

# Final Code

```python
class Solution(object):
    def removeElement(self, nums, val):
        k = 0

        for i in range(len(nums)):

            if nums[i] != val:

                nums[k] = nums[i]

                k += 1

        return k
```

---

# Complete Dry Run

Input

```
nums = [0,1,2,2,3,0,4,2]

val = 2
```

| Reader (`i`) | Value | Keep? | Writer (`k`) Before | Action | Writer (`k`) After |
|--------------|-------|-------|---------------------|--------|--------------------|
|0|0|✅|0|nums[0]=0|1|
|1|1|✅|1|nums[1]=1|2|
|2|2|❌|2|Skip|2|
|3|2|❌|2|Skip|2|
|4|3|✅|2|nums[2]=3|3|
|5|0|✅|3|nums[3]=0|4|
|6|4|✅|4|nums[4]=4|5|
|7|2|❌|5|Skip|5|

Final array

```
0

1

3

0

4

...

...
```

Return

```
5
```

---

# Complexity Analysis

### Time Complexity

```
O(n)
```

Each element is visited exactly once.

---

### Space Complexity

```
O(1)
```

No extra array is created.

---

# Common Mistakes

## Mistake 1

Trying to delete elements.

Arrays cannot remove elements in-place.

Overwrite instead.

---

## Mistake 2

Moving Writer every iteration.

Wrong.

Writer only moves

after writing.

---

## Mistake 3

Returning the array.

Wrong.

Return

```
k
```

which represents the new length.

---

## Mistake 4

Creating another array.

The problem specifically asks

```
In-place
```

---

## Mistake 5

Thinking the remaining elements matter.

LeetCode only checks

```
First k elements.
```

Everything after that is ignored.

---

# Pattern Recognition

Whenever you read

```
Modify array

In-place

Remove

Move

Keep

Overwrite
```

Immediately think

```
Reader Pointer

↓

Writer Pointer

↓

Overwrite

↓

Return New Length
```

---

# Interview Questions

### Q1

Why do we need two pointers?

---

### Q2

Why doesn't the Writer move every iteration?

---

### Q3

Why can we overwrite the array?

---

### Q4

Why don't we delete elements?

---

### Q5

Why is this solution O(n)?

---

### Q6

Why is the space complexity O(1)?

---

# Key Takeaways

- Arrays cannot physically remove elements.
- In-place means modifying the original array.
- The Reader scans every element.
- The Writer rebuilds the valid portion of the array.
- The Reader always moves.
- The Writer moves only after writing a valid element.
- `nums[k] = nums[i]` simply copies a valid element to the next available position.
- Returning `k` tells LeetCode how many valid elements remain.
- This Reader + Writer pattern is the foundation for many future array problems.

---

# Pattern Family

```
Remove Element (#27)

        ↓

Remove Duplicates from Sorted Array (#26)

        ↓

Move Zeroes (#283)

        ↓

Sort Array By Parity (#905)

        ↓

Duplicate Zeros (#1089)
```

Learning this one pattern will make all these problems much easier.

---