# LeetCode 448-Find All Numbers Disappeared in an Array

# Given an array nums of n integers where nums[i] is in the range [1, n], return an array of all the integers in the range [1, n] that do not appear in nums.

# Example 1:
# Input: nums = [4,3,2,7,8,2,3,1]
# Output: [5,6]

# Example 2:
# Input: nums = [1,1]
# Output: [2]
 
# Constraints:
# n == nums.length
# 1 <= n <= 105
# 1 <= nums[i] <= n
 
# Follow up: Could you do it without extra space and in O(n) runtime? You may assume the returned list does not count as extra space.





# Approach 1 — Brute Force
class Solution(object):
    def findDisappearedNumbers(self, nums):
        answer = []
        for number in range(1, len(nums)+1):
            if number not in nums:
                answer.append(number)
        return answer




# Approach 2 — HashSet
class Solution(object):
    def findDisappearedNumbers(self, nums):
        seen = set(nums)
        answer = []
        for number in range(1, len(nums)+1):
            if number not in seen:
                answer.append(number)
        return answer





# Index Marking (Optimal)
class Solution(object):
    def findDisappearedNumbers(self, nums):
        answer = []

        for i in range(len(nums)):
            index = abs(nums[i]) - 1
            if nums[index] > 0:
                nums[index] = -nums[index]

        for i in range(len(nums)):
            if nums[i] > 0:
                answer.append(i + 1)

        return answer