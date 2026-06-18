# LeetCode #217 — Contains Duplicate.
# Brute Force Solution

nums = [1,4,]
def Contains_Duplicate(nums):
    for i in range(len(nums)):
        for j in range(i+1,len(nums)):
            if nums[i] == nums[j]:
                return True
    return False
print(Contains_Duplicate(nums))


# better approach (sort)
nums = [1,4,3,7,2,0,7]
def Contains_Duplicate(nums):
    nums.sort()
    # print(nums)
    for i in range(len(nums)-1):
        if nums[i] == nums[i+1]:
            return True
    return False
print(Contains_Duplicate(nums))



# Optimal Solution for Contains Duplicate.
nums = [1,5,7,1,2]

def Contains_Duplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
print(Contains_Duplicate(nums))



