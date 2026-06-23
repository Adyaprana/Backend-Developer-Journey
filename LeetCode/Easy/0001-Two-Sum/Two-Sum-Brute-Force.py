# LeetCode #1 Two Sum
# Brute Force Solution

nums  = [2,7, 11,15]
target = 9
def two_sum(nums, target):

    for i in range(len(nums)):
        for j in range(i+1,len(nums)):
            if nums[i] + nums[j] == target:
                return[i,j]
                
print(two_sum(nums, target))


# LeetCode #1 Two Sum
# HashMap Solution

nums  = [2,7, 11,15]
target = 9
def two_sum(nums, target):
    seen = {}
    for i in range(len(nums)):
        find = target - nums[i]
        if find in seen:
            return [seen[find],i]
        else:
            seen[nums[i]] = i

print(two_sum(nums, target))

