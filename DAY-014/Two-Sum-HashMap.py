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

