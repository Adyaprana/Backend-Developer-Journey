# String methods: upper(), lower(), strip(), replace(), split(), len() etc

# upper() - converts all characters in a string to uppercase
# lower() - converts all characters in a string to lowercase
# strip() - removes leading and trailing whitespace from a string
# replace() - replaces a specified substring with another substring
# split() - splits a string into a list of substrings based on a specified delimiter
# len() - returns the length of a string
# index() - returns the index of the first occurrence of a specified substring in a string

# Example usage
name = "Adyaprana"
print(name.upper())  # Output: ADYAPRANA
print(name.lower())  # Output: adyaprana
print(name.capitalize())  # Output: Adyaprana
print(name.title())  # Output: Adyaprana
print(name.isalpha())  # Output: True
print(name.isdigit())  # Output: Falseprint(name.endswith("a"))  # Output: True
print(name.startswith("A"))  # Output: True
print(name.count("a"))  # Output: 2
print(name.find("p"))  # Output: 4
print(name.rfind("a"))  # Output: 8
print(name.split("a"))  # Output: ['Ady', 'pr', 'n', '']
print(name.replace("a", "o"))  # Output: Adyoprono
print(name.strip("A"))  # Output: dyaprana


print(len(name))  # Output: 9
print(name.index("p"))  # Output: 4
print(name[0])  # Output: A
print(name[1:5])  # Output: dyap
print(name[-1])  # Output: a


greeting = "   Hello, World!   "
print(greeting.strip())  # Output: Hello, World!


sentence = "I love Python programming"
print(sentence.replace("Python", "Java"))  # Output: I love Java programming

text = "Hello, how are you?"
print(text.split())  # Output: ['Hello,', 'how', 'are', 'you?']

