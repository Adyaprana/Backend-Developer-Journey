# LeetCode #20 Valid Parentheses

# Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', 
# determine if the input string is valid.

# An input string is valid if:
# Open brackets must be closed by the same type of brackets.
# Open brackets must be closed in the correct order.
# Every close bracket has a corresponding open bracket of the same type.
 

# Example 1:
# Input: s = "()"
# Output: true

# Example 2:
# Input: s = "()[]{}"
# Output: true

# Example 3:
# Input: s = "(]"
# Output: false

# Example 4:
# Input: s = "([])"
# Output: true

# Example 5:
# Input: s = "([)]"
# Output: false

# Constraints:
# 1 <= s.length <= 104
# s consists of parentheses only '()[]{}'.

s= "()"
def isValid(s):
    stack = []

    d = {
        ")": "(",
        "}": "{",
        "]": "["
    }
    print(d.values())
    for i in s:
        if i in d.values():
            stack.append(i)
            print(stack)    
        if i in d.keys():
            if len(stack) == 0:
                return False
            if d[i] != stack[-1]:
                return False
            if d[i] == stack[-1]:
                stack.pop(-1)
    if len(stack) == 0:
        return True
    return False
        
print(isValid(s))


# s = "()"

# def isValid(s):
#     stack = []

#     d = {
#         ")": "(",
#         "}": "{",
#         "]": "["
#     }

#     for i in s:
#         if i in d.values():
#             stack.append(i)

#         if i in d.keys():
#             if len(stack) == 0:
#                 return False

#             if d[i] != stack[-1]:
#                 return False

#             if d[i] == stack[-1]:
#                 stack.pop(-1)

#     if len(stack) == 0:
#         return True

#     return False