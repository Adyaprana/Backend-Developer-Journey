# LeetCode #242 — Valid Anagram


# Given two strings s and t, return true if t is an anagram of s, and false otherwise.

# Example 1:
# Input: s = "anagram", t = "nagaram"
# Output: true

# Example 2:
# Input: s = "rat", t = "car"
# Output: false

# Constraints:
# 1 <= s.length, t.length <= 5 * 104
# s and t consist of lowercase English letters.
 

## Why I Did Not Implement the Brute Force Approach
# A theoretical brute-force solution would generate all possible permutations of the first string and check whether the second string matches one of them.

# Example:
# s = "abc"

# Possible permutations:
# abc
# acb
# bac
# bca
# cab
# cba

# If the second string exists among these permutations, the strings are anagrams.
# However, the number of permutations grows extremely fast as the string length increases. 
# Since the problem allows strings up to 50,000 characters, generating all permutations is not practical.
# Because of this, I skipped implementing the brute-force solution and focused on more realistic approaches:
# 1. Sorting Approach - O(n log n)
# 2. Frequency Counting (HashMap/Dictionary) - O(n)
# These approaches are suitable for the given constraints and are commonly expected in interviews.
# For this problem, I would follow:

# Theory:
# Brute Force Idea (understand only)

# Implementation:
# Sorting Approach

# Then:
# HashMap / Frequency Counting Approach (Optimal)

# Approach 1: Sorting (Accepted)
s = "listen"
t = "silent"

def Valid_Anagram(s,t):
    if len(s) != len(t):
        return False
    s = sorted(s)
    t = sorted(t)
    if s == t:
        return True
    return False

print(Valid_Anagram(s,t))



# Approach 2: Frequency Counting / HashMap (Optimal)
s = "lisen"
t = "silent"

def Valid_Anagram(s,t):
    seen = {}
    num = 0
    if len(s) != len(t):
        return False
    for i in s:
        seen[i] = seen.get(i, 0) + 1
        print(seen)
    for j in t:
        seen[j] = seen.get(j, 0) - 1
        print(seen)
    for count in seen.values():
        if count != num:
            return False
    return True
print(Valid_Anagram(s,t))

