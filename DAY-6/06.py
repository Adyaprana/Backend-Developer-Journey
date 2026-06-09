# Student grade book using dictionary

student_grade_book = {
    "stu-1": {
        "name": "Adyaprana",
        "roll": "25mcac57",
        "course": "MCA",
        "grade": {"PYTHON": 89, "OS": 98, "DBMS": 90, "OOP": 97, "DEVOPS": 95}
    },
    "stu-2": {
        "name": "PRAVEEN",
        "roll": "25mcac50",
        "course": "MCA",
        "grade": {"PYTHON": 79, "OS": 69, "DBMS": 75, "OOP": 84, "DEVOPS": 88}
    },
    "stu-3": {
        "name": "VIKAS",
        "roll": "25mcac55",
        "course": "MCA",
        "grade": {"PYTHON": 81, "OS": 93, "DBMS": 60, "OOP": 87, "DEVOPS": 75}
    }
}

print("--- STUDENT REPORT CARD ---")
for stu_id, info in student_grade_book.items():
    grades = info["grade"].values()
    
    total_marks = sum(grades)
    num_subjects = len(grades)
    percentage = total_marks / num_subjects
    
    # Determine pass/fail (e.g., passing mark is 40 for all subjects)
    status = "PASS" if all(g >= 40 for g in grades) else "FAIL"
    
    print(f"\nName: {info['name']} ({info['roll']})")
    print(f"Total Marks: {total_marks} / {num_subjects * 100}")
    print(f"Percentage: {percentage:.2f}%")
    print(f"Status: {status}")
