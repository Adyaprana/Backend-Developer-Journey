
#  LeetCode #14 — Longest Common Prefix

# Write a function to find the longest common prefix string amongst an array of strings.
# If there is no common prefix, return an empty string "".

# Example 1:
# Input: strs = ["flower","flow","flight"]
# Output: "fl"

# Example 2:
# Input: strs = ["dog","racecar","car"]
# Output: ""
# Explanation: There is no common prefix among the input strings.

# Constraints:
# 1 <= strs.length <= 200
# 0 <= strs[i].length <= 200
# strs[i] consists of only lowercase English letters if it is non-empty.


# Approach 1: Horizontal Scanning
strs = ["flower","flow","flight"]
def longestCommonPrefix(strs):
    if not strs:
        return ""
    strs.sort(key=len) 
    prefix = strs[0]
    for word in strs:
        while not word.startswith(prefix):
            prefix = prefix[:-1] 
            if not prefix:       
                return ""
    return prefix
print(longestCommonPrefix(strs))


# Approach 2: Vertical Scanning
# Check character by character

# Index 0 across all words
# Index 1 across all words
# Index 2 across all words

# Stop when mismatch occurs
strs = ["flower","flow","flight"]
def longestCommonPrefix(strs):
    if not strs:
        return ""
    shortest = min(strs, key=len)
    for i in range(len(shortest)):
        char = shortest[i]
        for word in strs:
            if word[i] != char:
                return shortest[:i]
    return shortest
print(longestCommonPrefix(strs))


