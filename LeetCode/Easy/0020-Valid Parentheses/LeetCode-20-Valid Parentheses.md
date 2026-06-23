# Day 17 - LeetCode #20: Valid Parentheses

## Overview

Today I solved **LeetCode #20 - Valid Parentheses** and learned the **Stack** data structure.

This was my first Stack-based problem and helped me understand how to match opening and closing brackets correctly.

During this problem, I learned:

* What a Stack is
* Push operation
* Pop operation
* LIFO (Last In First Out)
* Matching brackets
* Why Stacks are useful

---

# Problem Statement

Given a string containing only:

```text
(
)
{
}
[
]
```

Determine whether the input string is valid.

A string is valid if:

1. Every opening bracket has a matching closing bracket.
2. Brackets close in the correct order.
3. Every closing bracket corresponds to the most recent unmatched opening bracket.

---

## Example 1

### Input

```python
s = "()"
```

### Output

```python
True
```

---

## Example 2

### Input

```python
s = "()[]{}"
```

### Output

```python
True
```

---

## Example 3

### Input

```python
s = "(]"
```

### Output

```python
False
```

---

## Example 4

### Input

```python
s = "([)]"
```

### Output

```python
False
```

---

## Example 5

### Input

```python
s = "{[]}"
```

### Output

```python
True
```

---

# Constraints

```text
1 <= s.length <= 10⁴
```

The string contains only:

```text
(
)
{
}
[
]
```

---

# Understanding the Problem

Consider:

```python
s = "({})"
```

Process:

```text
(
{
}
)
```

The closing brackets appear in reverse order of opening brackets.

```text
Open:
(
{

Close:
}
)
```

This is why a Stack works perfectly.

---

# What is a Stack?

A Stack follows:

```text
Last In First Out (LIFO)
```

Example:

```python
stack = []
```

Push:

```python
stack.append("(")
```

Stack:

```python
["("]
```

Push:

```python
stack.append("{")
```

Stack:

```python
["(", "{"]
```

Pop:

```python
stack.pop()
```

Stack:

```python
["("]
```

The most recently added item is removed first.

---

# Why Use a Stack?

Consider:

```python
s = "([{}])"
```

Open brackets:

```text
(
[
{
```

Stack:

```text
(
[
{
```

When we encounter:

```text
}
```

We must match:

```text
{
```

which is the most recent opening bracket.

A Stack gives us exactly that.

---

# My Solution (Stack + Dictionary)

```python
class Solution(object):
    def isValid(self, s):

        stack = []

        d = {
            ")": "(",
            "}": "{",
            "]": "["
        }

        for i in s:

            if i in d.values():
                stack.append(i)

            if i in d.keys():

                if len(stack) == 0:
                    return False

                if d[i] != stack[-1]:
                    return False

                stack.pop()

        if len(stack) == 0:
            return True

        return False
```

---

# Dry Run

## Example

```python
s = "({})"
```

Start:

```python
stack = []
```

Dictionary:

```python
{
    ")": "(",
    "}": "{",
    "]": "["
}
```

---

### Character 1

```text
(
```

Opening bracket.

Push:

```python
stack = ["("]
```

---

### Character 2

```text
{
```

Opening bracket.

Push:

```python
stack = ["(", "{"]
```

---

### Character 3

```text
}
```

Dictionary says:

```python
d["}"] = "{"
```

Top of stack:

```python
stack[-1] = "{"
```

Match found.

Pop:

```python
stack = ["("]
```

---

### Character 4

```text
)
```

Dictionary says:

```python
d[")"] = "("
```

Top of stack:

```python
stack[-1] = "("
```

Match found.

Pop:

```python
stack = []
```

---

Loop finished.

Stack is empty:

```python
[]
```

Return:

```python
True
```

---

# Invalid Example

```python
s = "([)]"
```

Process:

```text
(
[
)
```

Stack:

```python
["(", "["]
```

Dictionary:

```python
d[")"] = "("
```

Top of stack:

```python
"["
```

Compare:

```python
"[" != "("
```

Mismatch found.

Return:

```python
False
```

---

# Why Check for Empty Stack?

Consider:

```python
s = ")"
```

There is no opening bracket.

Stack:

```python
[]
```

Attempting:

```python
stack[-1]
```

would cause an error.

Therefore:

```python
if len(stack) == 0:
    return False
```

is required.

---

# Why Check if Stack is Empty After the Loop?

Consider:

```python
s = "(("
```

Process:

```text
(
(
```

Stack:

```python
["(", "("]
```

No closing brackets exist.

Loop finishes.

Stack is NOT empty.

Return:

```python
False
```

Because some opening brackets were never closed.

---

# Time Complexity

Each character is processed once.

```text
O(n)
```

---

# Space Complexity

In the worst case:

```python
s = "((((((((("
```

All characters are stored in the stack.

```text
O(n)
```

---

# Alternative Approach

A brute force style approach could repeatedly remove:

```text
()
{}
[]
```

from the string until no more pairs remain.

Example:

```text
({})

→ ()
→ ""
```

Empty string means valid.

However:

* Slower
* Less efficient
* Not preferred in interviews

Complexity can become:

```text
O(n²)
```

Therefore Stack is the preferred solution.

---

# Comparison of Approaches

| Approach                    | Time  | Space |
| --------------------------- | ----- | ----- |
| Repeated String Replacement | O(n²) | O(n)  |
| Stack + Dictionary          | O(n)  | O(n)  |

---

# Concepts Learned

During this problem I learned:

* Stack
* Push
* Pop
* LIFO
* Dictionary Mapping
* Bracket Matching
* Time Complexity
* Space Complexity

---

# Results

Problem Solved:

**LeetCode #20 - Valid Parentheses**

Approaches Learned:

* String Replacement (Theory) ✅
* Stack + Dictionary ✅

Status:

* Accepted on LeetCode ✅
* First Stack Problem Completed ✅

---

# Reflection

This problem introduced me to the Stack data structure.

The biggest lesson was:

> The most recent opening bracket must be matched first.

This naturally leads to using a Stack because it follows:

```text
Last In First Out (LIFO)
```

I also learned how dictionaries can be combined with stacks to quickly match corresponding brackets.

This is one of the most common interview patterns and forms the foundation for many future Stack problems.
