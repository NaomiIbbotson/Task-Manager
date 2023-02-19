#=====importing libraries===========
import datetime

# Returns True if the name and password are valid
def login(name, password):
    users = dictionary_of_users()

    # Check name and password against users dict.
    if name in users and users[name] == password:
       return True
    
# Returns a dictionary of users and passwords from user file
def dictionary_of_users():
    dict_of_user = {}
    with open("user.txt", "r")as f:
        for line in f:
            stripped_data = line.strip("\n")
            list_data = stripped_data.split(", ")
            dict_of_user[list_data[0]] = list_data[1]
    return dict_of_user


# Registers a new user when user selects "r"
def reg_user():
    # Dictionary of users from file
    users = dictionary_of_users()

    # Get username and check if it already exists in users
    while True:
        username = input("Enter the username you wish to register: ")
        if username in users:
            print("\nUsername already exists, please choose an alternative!\n")
        else:
            break
    
    # Get password and confirmation until they match
    while True:  
        password = input("Enter the password: ")
        confirmation = input("Confirm your password: ")

        # Register user if password match or display message.
        if password == confirmation:
            with open("user.txt", "a") as f:
                f.write(f"\n{username}, {password}")
            break
        else:
            print("\nPasswords do not match, try again!\n")


# Adding a task, called when user selects "a"
def add_task():
     # Get username and check if username exists
    users = dictionary_of_users()
    username = ""
    while username not in users:
        username = input("Enter the username of the person the task is to be assigned to: ")
        if username not in users:
            print("Username does not exist")

    # Get rest of the task data
    task = input("Enter the title of the task: ")
    task_description = input("Enter the task description: ")
    today = datetime.datetime.now()
    todays_date = today.strftime("%d %b %Y")

    # Getting the due date int the correct format
    while True:
        due_date = input("Enter the due date for the task DD Mon YYYY: ")
        try:
            trial_date = datetime.datetime.strptime(due_date, "%d %b %Y").date()
            break
        except:
            print("Please enter the date in the format specified")
    
    # Write data to file
    with open("tasks.txt", "a") as f:
            f.write(f"\n{username}, {task}, {task_description}, {todays_date}, {due_date}, No")


# Transforms string of individual task data into a list
def task_as_list(task):
    stripped_line = task.strip("\n")
    split_data = stripped_line.split(", ")
    return split_data

# Returns formatted task data for printing
def formatted_task(task, num):
    return(f"""
________________________________________________

Task ID:                {num}
Task :                  {task[1]}
Assigned to:            {task[0]}
Date assigned:          {task[3]}
Due date:               {task[4]}
Task complete?          {task[5]}
Task description:
    {task[2]}
________________________________________________
            """)


# View all tasks, called when user types ‘va’
def view_all():
    # Open tasks file an get data
    with open("tasks.txt", "r") as f:
        task_data = f.readlines()

    # Print each task in a readable way
    for task_num,line in enumerate(task_data, 1):
        task = task_as_list(line)
        print(formatted_task(task, task_num))


# View tasks assigned to logged in user, called when user types ‘vm’
def view_mine():
    # Open tasks file and display only the tasks for the logged in user
    with open("tasks.txt", "r") as f:
        task_data = f.readlines()

    # List of all the task numbers for the current user
    my_task_nums = []
    # List of all the tasks as list of lists
    list_of_all_tasks = []

    # Looping over task data
    # Adding all tasks to list of tasks
    # Getting current user task numbers
    # Printing only tasks for user
    for task_num,line in enumerate(task_data, 1):
        task = task_as_list(line)
        list_of_all_tasks.append(task)
        if task[0] == current_user:
            my_task_nums.append(task_num)
            print(formatted_task(task, task_num))

    # Choosing task to edit and validating choice.
    task_choice = 0

    while task_choice not in my_task_nums:
        task_choice = input("Enter a task number to edit or enter -1 to return to main menu: ")
        try:
            task_choice = int(task_choice)
        except:
            pass
  
        if task_choice == -1:
            return
        if task_choice not in my_task_nums:
            print("Please choose from the task numbers available.\n")

    task_index = task_choice - 1

    # If the task is already completed it cannot be edited - show message and return
    if list_of_all_tasks[task_index][-1] == "Yes":
            print("This task is complete and can no longer be edited")
            return

    edit_task(task_index, list_of_all_tasks)


def edit_task(index, tasks):
    # List of choices available and selection
    choices = ["c", "ed", "ep", "e"]
    selection = ""
    
    while selection not in choices:
        # Display editing menu and get selection from user
        selection = input("""Select one of the following Options below:

c - Mark task as complete
ed - Edit due date
ep - Edit person who the task is assigned to
e - Exit to main menu

: """).lower()
    
        if selection not in choices:
             print("You have made a wrong choice, Please try again\n")
             
    # Get data from user
    if selection == "c":
        tasks[index][-1] = "Yes"
    elif selection == "ed":
        # Getting date in correct format
        while True:
            tasks[index][4] = input("Enter the new date DD Mon YYYY: ")
            try:
                trial_date = datetime.datetime.strptime(tasks[index][4], "%d %b %Y").date()
                break
            except:
                print("Please enter the date in the format specified")
        
    elif selection == "ep":
        tasks[index][0] = input("Enter the person who the task is to be assigned: ")
    else:
        return

    # Transform tasks list to a string
    string_of_tasks  = ""
    for line in tasks:
        separator = ", "
        string_line = separator.join(line)
        string_line += "\n"
        string_of_tasks += string_line

    
    with open("tasks.txt", "w") as f:
        f.write(string_of_tasks)


def generate_reports():

    # Open tasks file an get data
    with open("tasks.txt", "r") as f:
        task_data = f.readlines()

    with open("user.txt", "r") as f:
        user_data = f.readlines()


    # variables for task counts
    completed_task_count = 0
    uncompleted_task_count = 0
    task_count = 0
    overdue_task_count = 0
    today = datetime.date.today()
    

    # Counting the tasks line by line
    for line in task_data:
        task = task_as_list(line)
        task_count += 1
        if task[5] == "Yes":
            completed_task_count += 1
        else:
            uncompleted_task_count += 1
            due_date = datetime.datetime.strptime(task[4], "%d %b %Y").date()
            if due_date < today:
                overdue_task_count +=1

    percent_incomplete = percentage_calculator(uncompleted_task_count, task_count)
    percent_ovedue = percentage_calculator(overdue_task_count, task_count)
    
    # Writing data to file task_overview
    with open("task_overview.txt", "w") as f:
        f.write(f"""Total number of tasks:          {task_count}
Total completed tasks:          {completed_task_count}
Total uncompleted tasks:        {uncompleted_task_count}
Total overdue tasks:            {overdue_task_count}
Percentage uncompleted tasks:   {percent_incomplete}%
Percentage of overdue tasks:    {percent_ovedue}%""")

    # user_overview.txt
    user_overview_data = []

    # Open user file and get data
    with open("user.txt", "r") as f:
        user_data = f.readlines()

    # Creating list of users
    users_list = []
    for line in user_data:
        stripped_data = line.strip("\n")
        list_user_data = stripped_data.split(", ")
        users_list.append(list_user_data[0])

    user_overview_data = []

    for name in users_list:
        user_stats = {
            "User" : name,
            "Number of tasks" : 0,
        }
        completed = 0
        uncompleted = 0
        overdue =0

        # Adding the data to user_stats
        for line in task_data:
            task = task_as_list(line)
            if task[0] == user_stats["User"]:
                user_stats["Number of tasks"] +=1
                if task[5] == "Yes":
                    completed +=1
                else:
                    uncompleted +=1
                    due_date = datetime.datetime.strptime(task[4], "%d %b %Y").date()
                    if today > due_date:
                        overdue += 1

        # The percentage of the total number of tasks that have been assigned to that user
        user_stats["Percent of tasks"] = percentage_calculator(user_stats["Number of tasks"], task_count)

        # The percentage of the tasks assigned to that user that have been completed
        user_stats["Percent completed"] = percentage_calculator(completed, user_stats["Number of tasks"])

        # The percentage of the tasks assigned to that user that have not been completed
        user_stats["Percent uncompleted"] = percentage_calculator(uncompleted, user_stats["Number of tasks"])

        # The percentage of the tasks assigned to that user that are overdue
        user_stats["Percent overdue"] = percentage_calculator(overdue, user_stats["Number of tasks"])

        user_overview_data.append(user_stats)
    
    num_of_users = len(users_list)

    with open("user_overview.txt", "w") as f:
        f.write(f"""Total number of users: {num_of_users}
Total number of tasks: {task_count}""")

        for user in user_overview_data:
            f.write(f"""
-----------------------------------------------------------
User:                                   {user["User"]}
Total number of tasks:                  {user["Number of tasks"]}
Percentage of tasks assigned to user:   {user["Percent of tasks"]}%
Percentage of user's completed tasks:   {user["Percent completed"]}%
Percentage of user's uncompleted tasks: {user["Percent uncompleted"]}%
Percentage of user's overdue tasks:     {user["Percent overdue"]}%
-----------------------------------------------------------
            """)


def percentage_calculator(num1, num2):
    if num1 == 0 or num2 == 0:
        return 0
    else:
        return round((num1 / num2) * 100)


def view_statistics():
    generate_reports()

    print("\nTasks Overview\n")

    with open("task_overview.txt", "r") as f:
        for line in f:
            stripped_line = line.strip("\n")
            print(stripped_line)

    print("\nUsers Overview\n")

    with open("user_overview.txt", "r") as f:
        for line in f:
            stripped_line = line.strip("\n")
            print(stripped_line)


#====Login Section====
# Ask for username and password until correct username and password entered.
logged_in = False
while not logged_in:
    current_user = input("Enter your username: ")
    user_password = input("Enter your password: ")
    logged_in = login(current_user, user_password)
    if not logged_in:
        print("\nYou have entered an incorrect username or password\n")


while True:
    #presenting the admin menu or user menu to the user and 
    # making sure that the input is converted to lower case.
    if current_user == "admin":
        menu = input("""Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
gr - generate reports
vs - view statistics
e - Exit
: """).lower()
    else:
        menu = input("""Select one of the following Options below:
a - Adding a task
va - View all tasks
vm - view my task
e - Exit
: """).lower()

    # Registering a user (admin only)
    if menu == 'r' and current_user == "admin":
        reg_user()
    
    # Adding a task
    elif menu == 'a':
        add_task()
        
    # View all tasks
    elif menu == 'va':
        view_all()
       
    # View tasks for logged in user
    elif menu == 'vm':
        view_mine()

    # Generate reports
    elif menu == "gr" and current_user == "admin":
        generate_reports()

    # View Statistics (admin only)
    elif menu == "vs" and current_user == "admin":
        view_statistics()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")