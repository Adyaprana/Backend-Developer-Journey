# LeetCode #58 — Length of Last Word

# Given a string s consisting of words and spaces, return the length of the last word in the string.
# A word is a maximal substring consisting of non-space characters only.

# Example 1:
# Input: s = "Hello World"
# Output: 5
# Explanation: The last word is "World" with length 5.

# Example 2:
# Input: s = "   fly me   to   the moon  "
# Output: 4
# Explanation: The last word is "moon" with length 4.

# Example 3:
# Input: s = "luffy is still joyboy"
# Output: 6
# Explanation: The last word is "joyboy" with length 6.
 
# Constraints:
# 1 <= s.length <= 104
# s consists of only English letters and spaces ' '.
# There will be at least one word in s.

# Using Split Method
s = "   fly me   to   the moon  "
def lengthOfLastWord(s):
    last_word = s.split()[-1]
    return len(last_word)
# lengthOfLastWord(s)
print(lengthOfLastWord(s))


# Reverse Traversal Optimal Solution.
s = "   fly me   to   the moon  "
def lengthOfLastWord(s):
    right = len(s) - 1
    count = 0
    while s[right] == ' ':
        right -= 1

    while right >= 0 and s[right] != ' ':
        count += 1
        right -= 1
    return count

print(lengthOfLastWord(s))