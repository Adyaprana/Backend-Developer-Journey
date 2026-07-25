# LeetCode 1929 - Concatenation of Array

# Given an integer array nums of length n, you want to create an array ans of length 2n where ans[i] == nums[i] and ans[i + n] == nums[i] for 0 <= i < n (0-indexed).

# Specifically, ans is the concatenation of two nums arrays.
# Return the array ans.

# Example 1:
# Input: nums = [1,2,1]
# Output: [1,2,1,1,2,1]
# Explanation: The array ans is formed as follows:
# - ans = [nums[0],nums[1],nums[2],nums[0],nums[1],nums[2]]
# - ans = [1,2,1,1,2,1]

# Example 2:
# Input: nums = [1,3,2,1]
# Output: [1,3,2,1,1,3,2,1]
# Explanation: The array ans is formed as follows:
# - ans = [nums[0],nums[1],nums[2],nums[3],nums[0],nums[1],nums[2],nums[3]]
# - ans = [1,3,2,1,1,3,2,1]
 
# Constraints:
# n == nums.length
# 1 <= n <= 1000
# 1 <= nums[i] <= 1000


# Approach 1 (Manual Solution)
class Solution(object):
    def getConcatenation(self, nums):
        ans = []
        for i in range(len(nums)):
            ans.append(nums[i])
        for i in range(len(nums)):
            ans.append(nums[i])
        return ans

        

# Approach 2  (One loop)
class Solution(object):
    def getConcatenation(self, nums):
        ans = [0] * (2 * len(nums))
        for i in range(len(nums)):
            ans[i] = nums[i]
            ans[i+len(nums)] = nums[i]
        return ans



# Approach 3 (Pythonic)
class Solution(object):
    def getConcatenation(self, nums):
        return nums * 2

#       OR     
#  
class Solution(object):
    def getConcatenation(self, nums):
        return nums + nums