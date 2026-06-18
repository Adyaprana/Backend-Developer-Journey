# File Modes: 
# r  → read
# w  → write
# a  → append
# x  → create

# Check File Exists
import os
if os.path.exists("DAY-11/student.txt"):
    print("Exists")

# UTF-8 Encoding
# with open(
#     "DAY-11/skills.txt",
#     encoding="utf-8"
# )


# INTERVIEW QUESTIONS:

# Q1. What is File I/O?
# Answer: Reading and writing data from files.

# Q2. What does open() do?
# Answer: Opens a file.

# Q3. Difference between read() and readline()?
# Answer: read() --> Entire file.
#         readline() --> One line.

# Q4. Difference between w and a?
# Answer: w --> Overwrite.
#         a --> Append.

# Q5. Why close()?
# Answer: Releases resources.

# Q6. Why use with?
# Answer: Automatically closes file.

# Q7. What is CSV?
# Answer: Comma Separated Values.

# Q8. Why is CSV popular?
# Answer: Easy data exchange format.

# Q9. What is JSON?
# Answer: JavaScript Object Notation, Data exchange format used by APIs.

# Q10. Why is JSON important for backend developers?
# Answer: APIs communicate using JSON.

# Q11. What does json.dump() do?
# Answer: Python → JSON file.

# Q12. What does json.load() do?
# Answer: JSON file → Python object.

# Q13. Difference between Dictionary and JSON?
# Answer: Dictionary: Python object.
#         JSON: Text format.

# Q14. Which Python datatype is closest to JSON object?
# Answer: Dictionary.

# Q15. What file mode is safest for adding data?
# Answer: Append mode: a