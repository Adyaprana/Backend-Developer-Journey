# TODO LIST APPLICATION


tasks = []
while True:
    print("\n")
    print("1.Add")
    print("2.Display")
    print("3.Remove")
    print("4.Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        task = input("Enter your task: ")
        tasks.append(task)
    elif choice == "2":
        print(tasks)
    elif choice == "3":
        task = input("Enter what you need to removes: ")
        if task in tasks:
            tasks.remove(task)
    elif choice =="4":
        break





































