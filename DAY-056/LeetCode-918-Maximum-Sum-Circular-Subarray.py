# LeetCode-918 Maximum Sum Circular Subarray

# Given a circular integer array nums of length n, return the maximum possible sum of a non-empty subarray of nums.
# A circular array means the end of the array connects to the beginning of the array. Formally, the next element of nums[i] is nums[(i + 1) % n] and the previous element of nums[i] is nums[(i - 1 + n) % n].
# A subarray may only include each element of the fixed buffer nums at most once. Formally, for a subarray nums[i], nums[i + 1], ..., nums[j], there does not exist i <= k1, k2 <= j with k1 % n == k2 % n.

# Example 1:
# Input: nums = [1,-2,3,-2]
# Output: 3
# Explanation: Subarray [3] has maximum sum 3.

# Example 2:
# Input: nums = [5,-3,5]
# Output: 10
# Explanation: Subarray [5,5] has maximum sum 5 + 5 = 10.

# Example 3:
# Input: nums = [-3,-2,-3]
# Output: -2
# Explanation: Subarray [-2] has maximum sum -2.

# Constraints:
# n == nums.length
# 1 <= n <= 3 * 104
# -3 * 104 <= nums[i] <= 3 * 104


class Solution(object):
    def maxSubarraySumCircular(self, nums):
        total_sum = nums[0]

        min_current = nums[0]
        min_subarr = nums[0]

        max_current = nums[0]
        max_subarr = nums[0]
        for i in range(1, len(nums)):
            total_sum += nums[i]
            if nums[i] < (min_current + nums[i]):
                min_current = nums[i]
            else:
                min_current += nums[i]
            if min_current < min_subarr:
                min_subarr = min_current

            if nums[i] > (max_current + nums[i]):
                max_current = nums[i]
            else:
                max_current += nums[i]
            if max_current > max_subarr:
                max_subarr = max_current

        if min_subarr == total_sum:
            return max_subarr
        return max(max_subarr, total_sum - min_subarr)



# Small style improvement (optional)
# Write Kadane using max() and min() because it highlights the idea more clearly:

# max_current = max(nums[i], max_current + nums[i])
# max_subarr = max(max_subarr, max_current)

# min_current = min(nums[i], min_current + nums[i])
# min_subarr = min(min_subarr, min_current)

# it's the same as the if/else version. Since for the learning the algorithm, your explicit if/else implementation is actually great because it makes the "Continue or Start Again" decision very clear.