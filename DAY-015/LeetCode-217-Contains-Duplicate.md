# LeetCode #217 - Contains Duplicate

## Problem Statement

Given an integer array `nums`, return `true` if any value appears at least twice in the array, and return `false` if every element is distinct.

### Example 1

Input:

```python
nums = [1,2,3,1]
```

Output:

```python
True
```

### Example 2

Input:

```python
nums = [1,2,3,4]
```

Output:

```python
False
```

---

# Approach 1: Brute Force

## Idea

Compare every element with every other element after it.

If two elements are equal, a duplicate exists.

## Code

```python
class Solution(object):
    def containsDuplicate(self, nums):
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] == nums[j]:
                    return True
        return False
```

## Dry Run

```python
nums = [1,4,7,9,4]
```

Compare:

```text
1 vs 4
1 vs 7
1 vs 9
1 vs 4

4 vs 7
4 vs 9
4 vs 4  ← Duplicate Found
```

Return:

```python
True
```

## Complexity

Time Complexity:

```text
O(n²)
```

Space Complexity:

```text
O(1)
```

## Drawback

For large inputs, this approach performs too many comparisons and may result in Time Limit Exceeded (TLE).

---

# Approach 2: Sorting

## Idea

Sort the array first.

After sorting, duplicate values become adjacent to each other.

Then compare neighboring elements.

## Code

```python
class Solution(object):
    def containsDuplicate(self, nums):
        nums.sort()

        for i in range(len(nums) - 1):
            if nums[i] == nums[i + 1]:
                return True

        return False
```

## Dry Run

Input:

```python
nums = [1,4,7,3,2,0,7]
```

After sorting:

```python
[0,1,2,3,4,7,7]
```

Compare:

```text
0 vs 1
1 vs 2
2 vs 3
3 vs 4
4 vs 7
7 vs 7 ← Duplicate Found
```

Return:

```python
True
```

## Important Learning

When comparing:

```python
nums[i]
nums[i+1]
```

the loop must run until:

```python
range(len(nums)-1)
```

Otherwise, the last iteration would try:

```python
nums[len(nums)]
```

which causes an IndexError.

## Complexity

Time Complexity:

```text
O(n log n)
```

Space Complexity:

```text
O(1) to O(n)
```

(depending on sorting implementation)

---

# Approach 3: HashSet (Optimal)

## Idea

Keep a set of previously seen numbers.

For each number:

1. Check whether it already exists in the set.
2. If yes, return True.
3. Otherwise add it to the set.

## Code

```python
class Solution(object):
    def containsDuplicate(self, nums):
        seen = set()

        for num in nums:
            if num in seen:
                return True

            seen.add(num)

        return False
```

## Dry Run

Input:

```python
nums = [1,5,7,1,2]
```

Start:

```python
seen = {}
```

Read:

```text
1
```

Add:

```python
{1}
```

Read:

```text
5
```

Add:

```python
{1,5}
```

Read:

```text
7
```

Add:

```python
{1,5,7}
```

Read:

```text
1
```

Already exists in set.

Return:

```python
True
```

## Complexity

Time Complexity:

```text
O(n)
```

Space Complexity:

```text
O(n)
```

---

# Comparison of All Approaches

| Approach    | Time Complexity | Space Complexity |
| ----------- | --------------- | ---------------- |
| Brute Force | O(n²)           | O(1)             |
| Sorting     | O(n log n)      | O(1) / O(n)      |
| HashSet     | O(n)            | O(n)             |

---

# Key Learnings

* Learned the difference between Brute Force, Sorting, and HashSet approaches.
* Understood why O(n²) solutions can cause Time Limit Exceeded.
* Learned how HashSet helps track previously seen elements.
* Learned the difference between Dictionary and Set in Python.
* Learned why `range(len(nums)-1)` is needed when comparing `nums[i]` and `nums[i+1]`.
* Practiced debugging edge cases and IndexError problems.
* Understood that the optimal solution is not always the first solution.

---

# Final Conclusion

For interviews and LeetCode:

* Brute Force is useful for understanding the problem.
* Sorting is a good intermediate optimization.
* HashSet is the preferred optimal solution for Contains Duplicate because it achieves O(n) time complexity.
