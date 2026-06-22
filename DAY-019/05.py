# INTERVIEW QUESTIONS: 


# Q1. What is an iterable?
# Answer: An object that can be looped over.
# Examples: list, tuple, string, dictionary, set.

# Q2. What is an iterator?
# Answer: An object that returns values one-by-one.

# Q3. Which function creates iterator?
# Answer: iter()

# Q4. Which function gets next value?
# Answer: next()

# Q5. What happens when iterator finishes?
# Answer: Raises: StopIteration

# Q6. What is iter()?
# Answer: Special method returning iterator object.

# Q7. What is next()?
# Answer: Returns next item from iterator.

# Q8. What is a generator?
# Answer: A function that uses: yield
#                   instead of: return

# Q9. Difference between return and yield?
# Answer: return: Ends function immediately.
#         yield:  Pauses function and remembers state.

# Q10. Why are generators memory efficient?
# Answer: Because values are generated only when needed.

# Q11. What is Generator Expression?
# Answer: Compact syntax for generators.
# Example: (x*x for x in range(5))

# Q12. Where are generators used?
# Answer:   fastAPI
#           Data Pipelines
#           File Processing
#           Streaming Data
#           AI/ML

# Q13. What is lazy evaluation?
# Answer: Compute value only when needed, Generators use lazy evaluation.

# Q14. Can generators be iterated multiple times?
# Answer: No, After exhaustion, create new generator.

# Q15. Why should backend developers learn generators?
# Answer: Because backend systems often process huge amounts of data and generators save memory.