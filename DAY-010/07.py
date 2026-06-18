# ✅ Safe Integer Input
try:
    number = int(input("enter a number: "))
except ValueError:
    print("Invalid enter number")

print("------------------------------------")





# ✅ Safe Division Program
try:
    n = 100
    number = int(input("enter a number: "))
    print(n/number)
except ZeroDivisionError:
    print("Cannot divide by zero")
print("------------------------------------")





# ✅ Handle ValueError
try:
    number1 = int(input("Enter A: "))
    number2 = int(input("Enter B: "))
    print(f"{number1} + {number2} = {number1 + number2}")
except ValueError:
    print("Invalid enter number")
print("------------------------------------")





# ✅ Handle IndexError
try:
    names = ["ADYAPRANA", "DRAVIS","NEXON"]
    print(names[0])
    print(names[7])
except IndexError:
    print("Index did not exist")
print("------------------------------------")





# ✅ Handle KeyError
try: 
    student = {
        "Name": "Adyaprana",
        "Roll": "25MCAC57"
    }
    print(student["Name"])
    print(student["age"])
except KeyError:
    print("Key did not Exist")
print("------------------------------------")





# ✅ Login Validation
try:
    username = input("Enter username: ")
    password = input("Enter password: ")
    if len(username) < 3 or len(password) < 6:
        print("Error: Username or password is too short!")
    else:
        print("Login successful!")
except Exception as e:
    print(f"Error: {e}")

print("------------------------------------")





# ✅ Student Marks Validation
while True:
    try:
        marks = float(input("Enter student marks (0-100): "))
        if marks < 0 or marks > 100:
            raise ValueError
    except ValueError:
        print("Error: Must be a number between 0 and 100!")
    else:
        print(f"Marks saved: {marks}")
        break
    finally:
        print("--- Marks check attempt complete ---")
print("------------------------------------")





# ✅ Age Validation
while True:
    try:
        age = int(input("Enter age (0-120): "))
        if age < 0 or age > 120:
            raise ValueError
    except ValueError:
        print("Error: Must be a whole number between 0 and 120!")
    else:
        print(f"Age saved: {age}")
        break
    finally:
        print("--- Age check attempt complete ---")
print("------------------------------------")





# ✅ Salary Validation
while True:
    try:
        salary = float(input("Enter salary: "))
        if salary < 0:
            raise ValueError
    except ValueError:
        print("Error: Must be a positive number!")
    else:
        print(f"Salary saved: {salary}")
        break
    finally:
        print("--- Salary check attempt complete ---")
print("------------------------------------")





# ✅ Enhanced Calculator
try:
    num1 = float(input("Enter Number 1: "))
    num2 = float(input("Enter Number 2: "))

    operation  = input("Enter your action('+','-','*','/'): ")

    if  operation == "+":
        print(f"{num1} + {num2} = {num1+num2}")
    elif  operation == "-":
        print(f"{num1} - {num2} = {num1-num2}")
    elif  operation == "*":
        print(f"{num1} * {num2} = {num1*num2}")
    elif  operation == "/":
        print(f"{num1} / {num2} = {num1/num2}")
    else: 
        raise ValueError("Invalid Operations")
    
except ValueError as e:
    print("Error: ",e)
except ZeroDivisionError:
    print("Cannot divide by zero")
finally:
    print("Calculator Closed")
print("------------------------------------")








# ✅ Student Grade Manager With Error Handling
print("====================================")
print("     STUDENT GRADE MANAGER          ")
print("====================================")
while True:
    try:
        student_name = input("Enter student name: ").strip()
        if not student_name.isalpha():
            raise ValueError("Name must contain letters only.")
    except ValueError as e:
        print(f"Error: {e} Please try again.")
    else:
        print(f"Student logged: {student_name}")
        break
    finally:
        print("-> Name validation block executed.")
while True:
    try:
        score_input = input("Enter exam score (0-100): ")
        score = float(score_input)
        if score < 0 or score > 100:
            raise ValueError("Score must be between 0 and 100.")
    except ValueError as e:
        if "could not convert" in str(e):
            print("Error: Score must be a valid number!")
        else:
            print(f"Error: {e}")
    else:
        print(f"Valid score recorded: {score}")
        break
    finally:
        print("-> Score validation block executed.")
try:
    print(f"\n📊 Processing Results for {student_name}...")
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"
except NameError:
    print("❌ Error: Critical system fault. Missing student data.")
else:
    print("\n====================================")
    print(f"🎓 REPORT CARD FOR {student_name.upper()}")
    print(f"📝 Final Score: {score}%")
    print(f"🏅 Letter Grade: {grade}")
    print("====================================")
finally:
    print("\n🏁 Grade Management System Session Closed.")

print("------------------------------------")





# ✅ Multiple Exception Handling
# List of standard student scores to practice with
sample_scores = [95, 82, "Absent", 74, 0, 88]

print("====================================")
print("    MULTIPLE EXCEPTION HANDLING     ")
print("====================================")

for item in sample_scores:
    try:
        print(f"\nProcessing entry: {item}")
        # This will fail with TypeError if 'item' is a string ("Absent")
        score = float(item) 
        # This will fail with ZeroDivisionError if score is 0
        scaling_factor = 100 / score 
        adjusted_score = score + 5
    except ValueError:
        # Catches explicitly failed manual conversions
        print("Error: Could not convert data to a number.")
        
    except TypeError:
        # Catches mixing incompatible types (e.g., trying to float() a word)
        print("Error: Incompatible data type found.")
        
    except ZeroDivisionError:
        # Catches dividing by zero math errors
        print("Error: Cannot calculate scaling factor because score is 0.")
        
    except Exception as general_error:
        # Parent exception: Catches any other unexpected error
        print(f"Unexpected System Error: {general_error}")
        
    else:
        # Runs ONLY if no errors happened above
        print(f"Success! Adjusted Score: {adjusted_score}")
        print(f"Scaling Metric: {scaling_factor:.2f}")
        
    finally:
        # Runs every single loop iteration
        print("-> Finished processing item pipeline.")
print("------------------------------------")



# ✅ Custom Exception Program
# Define custom exceptions by inheriting from the base Exception class
class InsufficientFundsError(Exception):
    """Raised when a withdrawal amount exceeds the account balance."""
    pass

class InvalidAmountError(Exception):
    """Raised when the input amount is negative or zero."""
    pass

# Mock account balance
account_balance = 500.0

print("=== BANKING SYSTEM (CUSTOM EXCEPTIONS) ===")
while True:
    try:
        withdraw_input = input(f"Current Balance: ${account_balance} | Enter amount to withdraw: ")
        amount = float(withdraw_input)
        
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be greater than zero.")
        if amount > account_balance:
            raise InsufficientFundsError(f"You cannot withdraw ${amount}. You only have ${account_balance}.")
            
    except ValueError:
        print("Error: Please enter a valid numerical amount.")
    except InvalidAmountError as e:
        print(f"Transaction Denied: {e}")
    except InsufficientFundsError as e:
        print(f"Transaction Denied: {e}")
    else:
        account_balance -= amount
        print(f"Success! You withdrew ${amount:.2f}.")
        print(f"New Balance: ${account_balance:.2f}")
        break
    finally:
        print("-> ATM transaction attempt finished.")

print("------------------------------------")


# =====================================================================
# ✅ Menu Driven Calculator
# =====================================================================
print("\n=== MENU DRIVEN CALCULATOR ===")

while True:
    print("\n1. Add (+)")
    print("2. Subtract (-)")
    print("3. Multiply (*)")
    print("4. Divide (/)")
    print("5. Exit")
    
    try:
        choice = input("Choose an option (1-5): ").strip()
        
        if choice == '5':
            print("👋 Exiting calculator. Goodbye!")
            break
            
        if choice not in ['1', '2', '3', '4']:
            raise ValueError("Invalid menu option selected.")
            
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        
        if choice == '1':
            result = num1 + num2
            op = "+"
        elif choice == '2':
            result = num1 - num2
            op = "-"
        elif choice == '3':
            result = num1 * num2
            op = "*"
        elif choice == '4':
            if num2 == 0:
                raise ZeroDivisionError("Math error: Cannot divide by zero.")
            result = num1 / num2
            op = "/"

    except ValueError as e:
        if "Invalid menu option" in str(e):
            print("Error: Please select a valid option from 1 to 5.")
        else:
            print("Error: Invalid numeric input. Please enter numbers only.")
    except ZeroDivisionError as e:
        print(f"Error: {e}")
    else:
        print(f"Result: {num1} {op} {num2} = {result}")
    finally:
        print("-> Calculation operation loop completed.")

print("------------------------------------")





