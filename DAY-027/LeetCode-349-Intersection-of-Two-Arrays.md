# Day 25 - LeetCode #349: Intersection of Two Arrays

# Overview

Today I solved **LeetCode #349 - Intersection of Two Arrays**.

This problem introduces:

* HashSet
* Set Operations
* Duplicate Removal
* Fast Membership Lookup

The goal is to return all unique elements that appear in both arrays.

---

# Problem Statement

Given two integer arrays:

```python
nums1 = [1,2,2,1]
nums2 = [2,2]
```

Return an array containing their intersection.

Each element in the result must:

```text
Appear in both arrays
Appear only once
```

Order does not matter.

---

# Example 1

Input:

```python
nums1 = [1,2,2,1]
nums2 = [2,2]
```

Output:

```python
[2]
```

Explanation:

```text
2 exists in both arrays.
```

Duplicates are removed.

---

# Example 2

Input:

```python
nums1 = [4,9,5]
nums2 = [9,4,9,8,4]
```

Output:

```python
[9,4]
```

or

```python
[4,9]
```

Both are accepted.

---

# Constraints

```text
1 <= nums1.length, nums2.length <= 1000
0 <= nums1[i], nums2[i] <= 1000
```

---

# Understanding the Problem

We need:

```text
Common Elements
```

between two arrays.

Example:

```python
nums1 = [1,2,2,1]
nums2 = [2,2]
```

Common values:

```text
2
```

Not:

```text
2,2
```

because duplicates must be removed.

---

# Approach 1: Brute Force (Nested Loops)

# Intuition

For every element in nums1:

```text
Check every element in nums2
```

If a match is found:

```text
Add it to the result
```

while avoiding duplicates.

---

# Code

```python
class Solution(object):

    def intersection(self, nums1, nums2):

        result = []

        for i in nums1:

            for j in nums2:

                if i == j and i not in result:
                    result.append(i)

        return result
```

---

# Dry Run

Input:

```python
nums1 = [1,2,2,1]
nums2 = [2,2]
```

Check:

```text
1 vs 2
1 vs 2
```

No match.

---

Check:

```text
2 vs 2
```

Match.

Result:

```python
[2]
```

---

Check remaining values.

Already present:

```python
[2]
```

Do not add again.

Final:

```python
[2]
```

---

# Complexity

Time Complexity:

```text
O(n × m)
```

Space Complexity:

```text
O(k)
```

where:

```text
k = number of common elements
```

---

# Approach 2: HashSet Intersection (Optimal)

# Intuition

Sets automatically:

```text
Remove duplicates
```

Example:

```python
set([1,2,2,1])
```

becomes:

```python
{1,2}
```

Then we can directly compute:

```python
set1 & set2
```

which means:

```text
Intersection of Sets
```

---

# Accepted Solution (Your Solution)

```python
class Solution(object):

    def intersection(self, nums1, nums2):

        set1 = set(nums1)
        set2 = set(nums2)

        return list(set1 & set2)
```

---

# Dry Run

Input:

```python
nums1 = [1,2,2,1]
nums2 = [2,2]
```

---

Convert to Sets

```python
set1 = {1,2}
set2 = {2}
```

---

Intersection

```python
set1 & set2
```

Result:

```python
{2}
```

Convert back:

```python
list({2})
```

Output:

```python
[2]
```

---

# Visualization

Original Arrays:

```text
nums1 = [1,2,2,1]
nums2 = [2,2]
```

Convert:

```text
{1,2}
{2}
```

Intersection:

```text
{2}
```

Result:

```text
[2]
```

---

# Why This Works

A set stores:

```text
Only Unique Values
```

Therefore:

```python
set(nums1)
```

automatically removes duplicates.

The operator:

```python
&
```

returns only elements present in both sets.

---

# Complexity Analysis

## Time Complexity

Creating sets:

```text
O(n + m)
```

Set intersection:

```text
O(min(n,m))
```

Overall:

```text
O(n + m)
```

---

## Space Complexity

Two sets are created.

```text
O(n + m)
```

---

# Approach 3: HashSet Membership Check

# Intuition

Store one array in a set.

Traverse the other array.

If a value exists inside the set:

```text
Add it to result
```

Use another set to avoid duplicates.

---

# Code

```python
class Solution(object):

    def intersection(self, nums1, nums2):

        seen = set(nums1)

        result = set()

        for num in nums2:

            if num in seen:
                result.add(num)

        return list(result)
```

---

# Complexity

Time:

```text
O(n + m)
```

Space:

```text
O(n + m)
```

---

# Comparison of Approaches

| Approach         | Time     | Space    |
| ---------------- | -------- | -------- |
| Brute Force      | O(n × m) | O(k)     |
| Set Intersection | O(n + m) | O(n + m) |
| HashSet Lookup   | O(n + m) | O(n + m) |

---

# Interview Pattern

This problem teaches:

```text
HashSet
```

The same pattern appears in:

* Contains Duplicate (#217)
* Missing Number (#268)
* Happy Number (#202)
* Longest Consecutive Sequence (#128)

---

# Concepts Learned

* Arrays
* HashSet
* Set Intersection
* Duplicate Removal
* Membership Lookup
* Time Complexity Analysis

---

# Results

Problem Solved:

**LeetCode #349 - Intersection of Two Arrays**

Approaches Learned:

* Brute Force ✅
* Set Intersection ✅
* HashSet Membership Lookup ✅

Status:

* Accepted on LeetCode ✅
* Passed All Test Cases ✅

---

# Reflection

The biggest lesson from this problem was:

> Sets automatically remove duplicates and provide efficient operations like intersection.

Instead of manually checking duplicates, Python's set operations allow us to solve the problem in a clean and efficient way.

This problem reinforced the importance of HashSets for fast lookups and duplicate handling.
