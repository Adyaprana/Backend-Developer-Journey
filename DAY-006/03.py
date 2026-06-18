# Nested Dictionaries --> Dictionary inside another dictionary.

# Simple Dictionary

student = {
    "name":"Adyaprana"
}

# Nested Dictionary
student = {
    "name":"Adyaprana",
    "address":{
        "city":"Bangalore",
    }
}
print(student["address"]["city"])

response = {
    "user":{
        "id":1,
        "name":"Adyaprana",
        "profile":{
            "city":"Bangalore"
        }
    }
}
print(response["user"]["profile"]["city"])


car = {
    "bmw":{
        "car_id": 101,
        "car_name": "BMW X3",
        "car_type": "SUV"
    },
    "audi":{
        "car_id": 104,
        "car_name": "AUDI Q5",
        "car_type": "SUV"
    }
}
print(car)
print(car["bmw"])
print(car["audi"]["car_name"])