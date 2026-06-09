# Word Frequency Counter

# Input:
# python is good python is easy

# Output:
# {
# 'python':2,
# 'is':2,
# 'good':1,
# 'easy':1
# }



text = input("Enter a text: ")
words = text.split()

frequency = {}

for word in words:
    if word in frequency:
        frequency[word] += 1
    else:
        frequency[word] = 1
print(frequency)
