nums1 = [1,2,3,0,0,0]
m = 3 
nums2 = [2,5,6]
n = 3

def merge(nums1, m, nums2, n):
        for i in nums1:
            if m == len(nums1)+1:
                nums1 = nums1
            else:
                nums1 = nums1.pop()
            print(nums1)
print(merge(nums1,m, nums2, n))