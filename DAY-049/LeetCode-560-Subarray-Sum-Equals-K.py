# 560. Subarray Sum Equals K

# Given an array of integers nums and an integer k, return the total number of subarrays whose sum equals to k.
# A subarray is a contiguous non-empty sequence of elements within an array.

# Example 1:
# Input: nums = [1,1,1], k = 2
# Output: 2

# Example 2:
# Input: nums = [1,2,3], k = 3
# Output: 2

# Constraints:
# 1 <= nums.length <= 2 * 104
# -1000 <= nums[i] <= 1000
# -107 <= k <= 107


# Brute Force Approach
class Solution(object):
    def subarraySum(self, nums, k):
        count = 0
        for start in range(len(nums)):
            current_sum = 0
            for i in range(start, len(nums)):
                current_sum += nums[i]
                if current_sum == k:
                    count += 1
        return count


# Optimal Approach - Prefix Sum + HashMap
class Solution(object):
    def subarraySum(self, nums, k):
        prefix_sum = 0
        count = 0
        HashMap = {0:1}
        for i in range(len(nums)):
            prefix_sum += nums[i]
            need = prefix_sum - k
            if need in HashMap:
                count += HashMap[need]
            HashMap[prefix_sum] = HashMap.get(prefix_sum, 0) + 1
        return count 