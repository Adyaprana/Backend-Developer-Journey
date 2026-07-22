# LeetCode 414 - Third Maximum Number

# Given an integer array nums, return the third distinct maximum number in this array. If the third maximum does not exist, return the maximum number.

 # Example 1:
# Input: nums = [3,2,1]
# Output: 1
# Explanation:
# The first distinct maximum is 3.
# The second distinct maximum is 2.
# The third distinct maximum is 1.

# Example 2:
# Input: nums = [1,2]
# Output: 2
# Explanation:
# The first distinct maximum is 2.
# The second distinct maximum is 1.
# The third distinct maximum does not exist, so the maximum (2) is returned instead.

# Example 3:
# Input: nums = [2,2,3,1]
# Output: 1
# Explanation:
# The first distinct maximum is 3.
# The second distinct maximum is 2 (both 2's are counted together since they have the same value).
# The third distinct maximum is 1.
 
# Constraints:
# 1 <= nums.length <= 104
# -231 <= nums[i] <= 231 - 1
 
# Follow up: Can you find an O(n) solution?






# Sorting 
class Solution(object):
    def thirdMax(self, nums):
        nums = list(dict.fromkeys(nums))
        nums.sort(reverse=True)
        if len(nums) < 3:
            return nums[0]
        return nums[2]



# One Pass (Optimal)
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
