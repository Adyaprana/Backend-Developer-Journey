# LeetCode #125 Valid Palindrome:

# A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, 
# it reads the same forward and backward. Alphanumeric characters include letters and numbers.

# Given a string s, return true if it is a palindrome, or false otherwise.
# Example 1:
# Input: s = "A man, a plan, a canal: Panama"
# Output: true
# Explanation: "amanaplanacanalpanama" is a palindrome.

# Example 2:
# Input: s = "race a car"
# Output: false
# Explanation: "raceacar" is not a palindrome.

# Example 3:
# Input: s = " "
# Output: true
# Explanation: s is an empty string "" after removing non-alphanumeric characters.
# Since an empty string reads the same forward and backward, it is a palindrome. 

# Constraints:
# 1 <= s.length <= 2 * 105
# s consists only of printable ASCII characters.



# Approach 1: Clean + Reverse + Compare
s = "A man, a plan, a canal: Panama"
def isPalindrome(s):
    cleaned = "".join(char for char in s if char.isalnum())
    cleaned = cleaned.lower()
    print(cleaned)
    reversed_s = cleaned[::-1]
    print(reversed_s)
    if cleaned == reversed_s:
        return True
    return False

print(isPalindrome(s))



# Approach 2: Two Pointers (optimal)
# left  → starts from beginning
# right → starts from end
s = "A man, a plan, a canal: Panama"
def isPalindrome(s):
    cleaned = "".join(char for char in s if char.isalnum())
    cleaned = cleaned.lower()
    left = 0
    right = len(cleaned)-1
    while left < right:
        if cleaned[left] != cleaned[right]:
            return False
        left += 1
        right -= 1
    return True
print(isPalindrome(s))