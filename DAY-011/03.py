# CSV FILES: 
# CSV: Comma Separated Values
# CSV MODULE --> import csv

# Example:
# name,age,city
# Adyaprana,23,Bangalore
# Rahul,22,Delhi

# Used everywhere:
# Excel
# Data Analysis
# Reports
# Business Data

# Write CSV: 
import csv
with open("DAY-11/students.csv","w",newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Name","Age"])
    writer.writerow(["Adyaprana",23])
    writer.writerow(["Rahul",22])
    writer.writerow(["david",34])
    writer.writerow(["sam",27])
    writer.writerow(["vikram",29])
    writer.writerow(["sourav",24])

# Read CSV
import csv
with open("DAY-11/students.csv") as file:
    read = csv.reader(file)
    for row in read:
        print(row)