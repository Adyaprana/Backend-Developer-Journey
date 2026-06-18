# Grade Calculator

marks = int(input("enter marks:"))
if marks >= 90:
    print("Grade A")
elif marks >= 80:
    print("Grade B")
elif marks >= 70:
    print("Grade C")
elif marks >= 60:
    print("Grade D")
elif marks >= 50:
    print("PASS")
else:
    print("FAIL")


# Enhanced Version of Grade Calculator

marks = int(input("enter marks:"))
if marks > 100 or marks < 0:
    print("Invalid Marks")
elif marks >= 90:
    print("Grade A")
elif marks >= 80:
    print("Grade B")
elif marks >= 70:
    print("Grade C")
elif marks >= 60:
    print("Grade D")
elif marks >= 50:
    print("PASS")
else:
    print("FAIL")