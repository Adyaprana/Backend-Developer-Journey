# LeetCode #169 Majority Element: 

# Given an array nums of size n, return the majority element.
# The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.

# Example 1:
# Input: nums = [3,2,3]
# Output: 3

# Example 2:
# Input: nums = [2,2,1,1,1,2,2]
# Output: 2

# Constraints:
# n == nums.length
# 1 <= n <= 5 * 104
# -109 <= nums[i] <= 109
# The input is generated such that a majority element will exist in the array.
 
# Follow-up: Could you solve the problem in linear time and in O(1) space


# HashMap approach:
nums = [2,2,1,1,1,2,2]
def majorityElement(nums):
    count = {}
    max_count = 0
    majority = 0
    for num in nums:
        count[num] = count.get(num, 0)+ 1
    for key, values in count.items():
        if values > max_count:
            max_count = values
            majority = key
    return majority

print(majorityElement(nums))


# Boyer-Moore Voting Algorithm:
nums = [3, 3, 4, 2, 4, 4, 2, 4, 4]
def majorityElement(nums):
    candidate = None
    votes = 0
    for num in nums:
        if votes == 0:
            candidate = num
            votes += 1
        elif num == candidate:
            votes +=1
        else:
            votes -= 1
    return candidate
            
print(majorityElement(nums))