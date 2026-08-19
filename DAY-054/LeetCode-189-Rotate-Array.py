# LeetCode 189 Rotate Array

# Given an integer array nums, rotate the array to the right by k steps, where k is non-negative.

#  Example 1:
# Input: nums = [1,2,3,4,5,6,7], k = 3
# Output: [5,6,7,1,2,3,4]
# Explanation:
# rotate 1 steps to the right: [7,1,2,3,4,5,6]
# rotate 2 steps to the right: [6,7,1,2,3,4,5]
# rotate 3 steps to the right: [5,6,7,1,2,3,4]

# Example 2:
# Input: nums = [-1,-100,3,99], k = 2
# Output: [3,99,-1,-100]
# Explanation: 
# rotate 1 steps to the right: [99,-1,-100,3]
# rotate 2 steps to the right: [3,99,-1,-100]
 
# Constraints:
# 1 <= nums.length <= 105
# -231 <= nums[i] <= 231 - 1
# 0 <= k <= 105

# Follow up:
# Try to come up with as many solutions as you can. There are at least three different ways to solve this problem.
# Could you do it in-place with O(1) extra space?



# Approach 1: Using Extra Array
class Solution(object):
    def rotate(self, nums, k):
        arr = [0] * len(nums)
        k = k % len(nums)
        for i in range(len(nums)):
            New_Index = (i + k) % len(nums)
            arr[New_Index] = nums[i]
        nums[:] = arr


# Approach 2: Using Reverse Method
class Solution(object):
    def rotate(self, nums, k):
        k = k % len(nums)
        nums.reverse()
        nums[0:k] = nums[0:k][::-1]
        nums[k:] = nums[k:][::-1]

# Approach 3: reverse (self, start, end)

