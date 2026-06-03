# calculate the area of a retangle
length = float(input("Enter the length of the rectangle: "))
breadth = float(input("Enter the breadth of the rectangle: "))

area = length * breadth
print(f"The area of the rectangle is: {area}")


# calculate the area of a circle
radius = float(input("Enter the radius of the circle: "))  
pi = 3.14159
area_circle = pi * radius ** 2
print(f"The area of the circle is: {area_circle}")

# calculate the area of a triangle
base = float(input("Enter the base of the triangle: ")) 
height = float(input("Enter the height of the triangle: "))
area_triangle = 0.5 * base * height 
print(f"The area of the triangle is: {area_triangle}")

# calculate the area of a square
side = float(input("Enter the side length of the square: "))
area_square = side ** 2
print(f"The area of the square is: {area_square}")
