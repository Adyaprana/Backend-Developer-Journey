# Reverse String (Reverse a string using loop)
# Method 1 (Loop)
text = str(input("enter a text: "))
reverse = ""
for ch in text:
    reverse = ch + reverse
    print(reverse)

# Method 2

text = input("Enter Text: ")
print(text[::-1])