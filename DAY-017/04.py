# Polymorphism: --> Same method name BUT Different behavior.

# Think: Animal Sound
# Dog: Bark
# Cat: Meow
# Bird: Chirp

# Same action but Different implementation.

# Example: 
class Dog:
    def sound(self):
        print("Bark")
class Cat:
    def sound(self):
        print("Meow")

animals = [Dog(), Cat()]

for animal in animals:
    animal.sound()

# It's Powerful --> The caller doesn't care what object it receives.
# Only knows: .sound()
# This is heavily used in frameworks.

