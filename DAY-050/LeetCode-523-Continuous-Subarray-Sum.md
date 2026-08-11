# LeetCode #523 — Continuous Subarray Sum

---

# Problem Statement

Given an integer array `nums` and an integer `k`, return `true` if `nums` has a **continuous subarray of size at least two** whose elements sum up to a multiple of `k`, otherwise return `false`.

A multiple of `k` is a number `x` such that:

```
x = n × k
```

where `n` is an integer.

---

## Examples

### Example 1

```text
Input:
nums = [23,2,4,6,7]
k = 6

Output:
true
```

Explanation:

```
2 + 4 = 6

6 % 6 = 0
```

So the answer is `true`.

---

### Example 2

```text
Input:
nums = [23,2,6,4,7]
k = 6

Output:
true
```

Explanation:

```
23 + 2 + 6 + 4 + 7 = 42

42 % 6 = 0
```

---

### Example 3

```text
Input:
nums = [23,2,6,4,7]
k = 13

Output:
false
```

No valid continuous subarray exists.

---

# Constraints

- 1 ≤ nums.length ≤ 100000
- 0 ≤ nums[i] ≤ 10⁹
- 1 ≤ k ≤ 2³¹−1

---

# Understanding the Problem

The problem is asking us to determine whether there exists **at least one continuous subarray** that satisfies two conditions:

1. The subarray length must be **at least 2**.
2. The sum of the subarray must be divisible by `k`.

Notice carefully that the problem **does not ask us to find the subarray** or **count all possible subarrays**.

It only asks:

> **Does such a subarray exist?**

So our answer is simply:

- `True`
- `False`

---

# What is a Continuous Subarray?

A continuous subarray contains consecutive elements.

Example:

```text
nums = [23,2,4,6,7]
```

Valid subarrays:

```
[23,2]
[2,4]
[4,6,7]
[23,2,4]
```

Invalid:

```
[23,4]
[2,7]
```

because elements cannot be skipped.

---

# What Does "Multiple of k" Mean?

A number is a multiple of `k` if dividing it by `k` leaves remainder `0`.

Example:

```
6 % 6 = 0

12 % 6 = 0

18 % 6 = 0

24 % 6 = 0
```

So if

```
Subarray Sum % k == 0
```

then that subarray satisfies the condition.

---

# Important Observations

While reading the problem, we can notice several things:

- We only need to return `True` or `False`.
- We never need to return the actual subarray.
- The sum of a subarray is important.
- Prefix Sum immediately becomes a useful idea.
- A brute-force solution will generate every possible subarray.

---

# Brute Force Approach

The most straightforward idea is:

Start every index.

Extend the subarray one element at a time.

Calculate the sum.

Check whether

```python
current_sum % k == 0
```

If yes and the subarray length is at least 2,

return `True`.

Otherwise continue.

If every subarray is checked,

return `False`.

---

# Brute Force Algorithm

1. Start from every index.
2. Keep extending the subarray.
3. Maintain the running sum.
4. Check whether the sum is divisible by `k`.
5. If yes and length ≥ 2, return `True`.
6. Otherwise continue searching.
7. If no valid subarray exists, return `False`.

---

# Brute Force Code

```python
class Solution(object):
    def checkSubarraySum(self, nums, k):
        for start in range(len(nums)):
            current_sum = 0

            for end in range(start, len(nums)):
                current_sum += nums[end]

                if end - start + 1 >= 2 and current_sum % k == 0:
                    return True

        return False
```

---

# Dry Run (Brute Force)

Example:

```text
nums = [23,2,4,6,7]

k = 6
```

Start at index 0:

```
23
23+2
23+2+4
23+2+4+6
...
```

No answer yet.

Start at index 1:

```
2

2+4 = 6

6 % 6 = 0
```

Length = 2

Return True.

---

# Complexity Analysis (Brute Force)

Time Complexity:

```
O(n²)
```

Space Complexity:

```
O(1)
```

---

# Why is Brute Force Slow?

For every element,

we again traverse the remaining array.

```
n

↓

n-1

↓

n-2

↓

...
```

This creates approximately

```
n²
```

operations.

For an array of size 100000,

this approach becomes far too slow.

---

# Revisiting Prefix Sum

Instead of calculating every subarray sum repeatedly,

we can use Prefix Sum.

Example:

```
nums

23 2 4 6 7
```

Prefix Sum:

```
23

25

29

35

42
```

Each Prefix Sum stores the total sum from index `0` up to the current index.

Using Prefix Sum allows us to calculate subarray sums efficiently.

---

# The Biggest Mathematical Observation

This problem is based on one very important mathematical property.

If two Prefix Sums have the same remainder when divided by `k`,

then their difference is divisible by `k`.

Example:

```
29 % 6 = 5

11 % 6 = 5
```

Both have the same remainder.

Now subtract them:

```
29 - 11 = 18

18 % 6 = 0
```

The difference becomes divisible by `6`.

This is the core idea of the entire problem.

Everything else in the solution simply implements this observation efficiently.

---

# Building the Intuition

Instead of storing the entire Prefix Sum,

we only care about its remainder.

For example,

```
23 % 6 = 5

25 % 6 = 1

29 % 6 = 5
```

Notice that remainder `5` appears again.

That immediately tells us:

```
29 - 23 = 6

6 % 6 = 0
```

So the subarray between those two Prefix Sums has a sum divisible by `6`.

That means we have found our answer.

---

# Pattern Connection

This problem continues the Prefix Sum learning journey.

```
Running Sum
        ↓
Prefix Sum
        ↓
Prefix Sum + HashMap
        ↓
Prefix Sum % k + HashMap
```

Previous problems:

- LeetCode #1480 — Running Sum
- LeetCode #303 — Range Sum Query
- LeetCode #560 — Subarray Sum Equals K
- LeetCode #523 — Continuous Subarray Sum

Each problem builds on the previous one.

---

# Interview Questions

### Why is Prefix Sum useful here?

Because it allows us to calculate subarray sums efficiently without recalculating them repeatedly.

---

### Why don't we store every subarray?

That would lead to an O(n²) solution.

---

### What is the most important mathematical observation?

If two Prefix Sums have the same remainder when divided by `k`, then their difference is divisible by `k`.

---

### What data structure will help us?

A HashMap.

It allows O(1) lookup to check whether a remainder has already appeared.

---

# Learning Summary

In this problem, I learned:

- How to recognize when Prefix Sum can optimize a brute-force solution.
- Why recalculating every subarray sum is inefficient.
- The mathematical property behind equal remainders.
- Why the problem is solved using Prefix Sum instead of checking every subarray.
- How this problem extends the Prefix Sum pattern learned in previous LeetCode problems.

The next step is to combine this mathematical observation with a HashMap to build the optimal O(n) solution.




# LeetCode #523 — Continuous Subarray Sum (Part 2)

---

# Optimal Approach

From Part 1, we discovered one important mathematical property:

> If two Prefix Sums have the same remainder when divided by `k`, then their difference is divisible by `k`.

Instead of checking every subarray, we can simply check whether the same remainder has appeared before.

This reduces the time complexity from **O(n²)** to **O(n)**.

---

# Why Does the Same Remainder Work?

Suppose:

```
29 % 6 = 5

11 % 6 = 5
```

Both Prefix Sums leave the same remainder.

Subtract them:

```
29 - 11 = 18

18 % 6 = 0
```

Since the difference is divisible by `6`, the subarray between these two Prefix Sums also has a sum divisible by `6`.

This single mathematical property is the foundation of the entire algorithm.

---

# Why Do We Need a HashMap?

Imagine calculating Prefix Sums.

```
23

25

29

35

42
```

Their remainders are

```
5

1

5

5

0
```

Whenever we get a remainder, we need to know:

> **"Have I seen this remainder before?"**

Searching every previous remainder would take O(n).

Instead, we use a HashMap.

HashMap lookup takes approximately O(1), making the overall algorithm O(n).

---

# What Does the HashMap Store?

The HashMap stores:

```
Remainder
        ↓
First Index
```

Example:

```
{
    5 : 0,
    1 : 1
}
```

This means:

- Remainder `5` first appeared at index `0`.
- Remainder `1` first appeared at index `1`.

Notice that we **do not store Prefix Sums**.

We only store their **remainders**.

---

# Why Store the First Index?

Suppose the same remainder appears multiple times.

```
Index

0   1   2   3

5       5   5
```

The first occurrence is at index `0`.

Later it appears at index `2`.

Later again at index `3`.

If we overwrite the first index,

```
5 : 3
```

we lose valuable information.

Keeping the earliest index gives the largest possible subarray and correctly checks the required length.

Therefore,

we only store the remainder the **first time** it appears.

---

# Why Don't We Overwrite?

Suppose

```
5

↓

Index 0
```

Later,

```
5

↓

Index 2
```

If we overwrite,

```
5 : 2
```

then when another `5` appears at index `3`,

```
diff = 3 - 2 = 1
```

which is incorrect because we lost the earlier occurrence.

Keeping

```
5 : 0
```

gives

```
diff = 3 - 0 = 3
```

which correctly represents the longest valid subarray.

---

# Why Do We Initialize the HashMap with `{0: -1}`?

Initially,

our Prefix Sum is

```
0
```

before reading any element.

We imagine that this Prefix Sum exists at index `-1`.

```
Index

-1   0   1

     6   6
```

HashMap:

```
{
    0 : -1
}
```

When the Prefix Sum becomes divisible by `k`,

its remainder becomes `0`.

Example:

```
Prefix Sum = 12

12 % 6 = 0
```

Current index:

```
1
```

Distance:

```
1 - (-1) = 2
```

Subarray length:

```
2
```

which satisfies the condition.

Without `{0:-1}`,

subarrays beginning at index `0` would never be detected correctly.

---

# Why Do We Check `diff >= 2`?

The problem states:

> The subarray must contain **at least two elements**.

Suppose

```
Previous remainder

↓

Index 0
```

Current remainder

↓

```
Index 2
```

Then

```
diff = 2 - 0 = 2
```

The subarray lies between them.

```
Index

0   1   2

23  2   4
```

The actual subarray is

```
[2,4]
```

Length:

```
2
```

Valid.

---

Suppose instead

```
Previous Index = 4

Current Index = 5
```

Then

```
diff = 1
```

The subarray contains only one element.

This violates the problem's condition.

Therefore,

```python
if diff >= 2:
    return True
```

simply checks whether the subarray length is at least two.

---

# Complete Algorithm

1. Initialize Prefix Sum as `0`.
2. Create a HashMap with `{0:-1}`.
3. Traverse the array.
4. Update the Prefix Sum.
5. Calculate the remainder.
6. If the remainder has appeared before:
   - Calculate the distance between indices.
   - If the distance is at least `2`, return `True`.
7. Otherwise, store the remainder and its first index.
8. If the loop finishes, return `False`.

---

# Final Python Code

```python
class Solution(object):
    def checkSubarraySum(self, nums, k):
        Running_Prefix = 0
        HashMap = {0: -1}

        for i in range(len(nums)):
            Running_Prefix += nums[i]
            remainder = Running_Prefix % k

            if remainder in HashMap:
                diff = i - HashMap[remainder]

                if diff >= 2:
                    return True
            else:
                HashMap[remainder] = i

        return False
```

---

# Complete Dry Run

Input:

```
nums = [23,2,4,6,7]

k = 6
```

Initial State

```
Running_Prefix = 0

HashMap = {0:-1}
```

| Index | Number | Prefix Sum | Remainder | HashMap | Action |
|------:|-------:|-----------:|----------:|----------|--------|
|0|23|23|5|{0:-1}|Store `5:0`|
|1|2|25|1|{0:-1,5:0}|Store `1:1`|
|2|4|29|5|Already exists|diff = 2 - 0 = 2 → Return True|

The algorithm stops immediately because a valid subarray has been found.

---

# Complexity Analysis

### Time Complexity

```
O(n)
```

Each element is visited exactly once.

HashMap operations are O(1).

---

### Space Complexity

Worst Case:

```
O(n)
```

In practice,

at most one index is stored for each unique remainder.

So the effective space complexity is often written as

```
O(min(n,k))
```

---

# Common Mistakes

### ❌ Storing Prefix Sum instead of Remainder

Wrong

```
HashMap[Running_Prefix]
```

Correct

```
HashMap[Running_Prefix % k]
```

---

### ❌ Storing Frequency

Frequency is useful in LeetCode #560.

This problem needs the **first index**, not the count.

---

### ❌ Overwriting the First Index

Always keep the earliest occurrence.

Never overwrite it.

---

### ❌ Forgetting `{0:-1}`

Without it,

subarrays starting from index `0` cannot be handled correctly.

---

### ❌ Forgetting `diff >= 2`

The problem requires

```
Subarray Length ≥ 2
```

This condition checks exactly that.

---

# Pattern Recognition

Whenever a problem contains:

- Continuous Subarray
- Sum
- Divisible by `k`
- Multiple of `k`

Think immediately:

```
Running Sum
        ↓
Prefix Sum
        ↓
Modulo
        ↓
HashMap
```

This pattern appears frequently in interview questions involving Prefix Sum and modular arithmetic.

---

# Interview Questions

### Why do we store the first index instead of the latest one?

To preserve the longest possible distance and correctly satisfy the minimum subarray length requirement.

---

### Why is the HashMap initialized with `{0:-1}`?

To correctly detect valid subarrays that begin at index `0`.

---

### Why don't we store frequencies?

Because we only need to know whether a valid subarray exists, not how many exist.

---

### What if `k = 0`?

LeetCode guarantees

```
1 ≤ k ≤ 2³¹−1
```

So this edge case never occurs.

If it did, we would need special handling because modulo by zero is undefined.

---

# Key Takeaways

- Prefix Sum avoids recalculating subarray sums.
- Equal remainders imply a divisible difference.
- Store the **first occurrence** of each remainder.
- `{0:-1}` handles subarrays starting at index `0`.
- `diff >= 2` ensures the subarray length is valid.
- HashMap reduces the solution from **O(n²)** to **O(n)**.

---
