# map vs List Comprehension

# Map:
numbers = []
list(map(lambda x:x*x,numbers))

# List Comprehension:
[x*x for x in numbers]


# filter vs List Comprehension

# Filter:
list(filter(lambda x:x>10,numbers))

# List Comprehension:
[x for x in numbers if x>10]


# INTERVIEW QUESTIONS

# Q1. What is Lambda Function?
# Answer: An anonymous function defined using lambda keyword.

# Q2. Why use Lambda?
# Answer: For short one-line functions.

# Q3. Syntax of Lambda?
# Answer: lambda arguments: expression

# Q4. What is map()?
# Answer: Applies a function to every element.

# Q5. What does map return?
# Answer: A map object. Usually converted using: list(map(...))

# Q6. What is filter()?
# Answer: Returns elements matching a condition.

# Q7. Difference Between map and filter?
# Answer: map transforms. filter selects.

# Q8. What is zip()?
# Answer: Combines multiple iterables element-by-element.

# Q9. What happens if zip lists have different lengths?
# Answer: Stops at shortest list.
# Example:
zip([1,2],[10])
# Output:
[(1,10)]

# Q10. What is sorted()?
# Answer: Returns new sorted list.

# Q11. Difference between sorted() and sort()?
# Answer: 1. sorted() Returns new list.
#         2. sort() Modifies original list.

# Q12. What does key argument do?
# Answer: Controls sorting logic.

# Q13. Can Lambda Have Multiple Arguments?
# Answer: Yes. lambda x,y:x+y

# Q14. Which is more Pythonic: map or comprehension?
# Answer: Usually list comprehension.

# Q15. Where are Lambda, map, filter used in backend?
# Answer: Used for: 1. API data transformation
#                   2. Filtering records
#                   3. Sorting users
#                   4. Data processing pipelines

