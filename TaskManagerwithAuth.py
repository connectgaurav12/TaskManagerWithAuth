# Importing Packages
import pandas as pd
import hashlib  ##required to encrypt the password
import os

# Files to store user credentials and tasks for users
users_file = "users.csv"
tasks_file = "tasks.csv"

# Create file if don't exist
if not os.path.exists("users.csv"):
    pd.DataFrame(columns=['username', 'password']).to_csv("users.csv")

if not os.path.exists("tasks.csv"):
    pd.DataFrame(columns=['username', 'taskId', 'description', 'status']).to_csv("tasks.csv")


# function to hash encrypt the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# function to register the user
def register_user():
    username = input("Please enter the Username:")
    password = input("Please enter the Password")

    user_df = pd.read_csv(users_file)

    if username in user_df['username'].values:
        print("Username Already exist. Please try using different user name")
        return False

    hashed_pswd = hash_password(password)

    new_user = pd.DataFrame([[username, hashed_pswd]], columns=['username', 'password'])
    user_df = pd.concat([user_df, new_user], ignore_index=True)

    user_df.to_csv(users_file,index=False)

    print("Registration for ", username, "is successful")
    return True


# Function for login/Authentication
def login():
    username = input("Please enter the Username:")
    password = input("Please enter the Password")
    user_df = pd.read_csv(users_file)

    if username not in user_df['username'].values:
        print("You have entered invalid username or password")
        return ""

    hashed_pswd = hash_password(password)

    if hashed_pswd != user_df[user_df['username'] == username]['password'].values[0]:
        print("You have entered invalid username or password")
        return ""

    print("Login Successful for username :", username)
    return username


# Function to add the task
def add_task(username):
    task_desc = input("Enter the task description :")
    task_df = pd.read_csv(tasks_file)
    task_id = len(task_df) + 1
    new_task = pd.DataFrame([[username, task_id, task_desc, 'Pending']],
                            columns=['username', 'taskId', 'description', 'status'])
    task_df = pd.concat([task_df, new_task], ignore_index=True)
    task_df.to_csv(tasks_file, index=False)

    print("Task for", username, "Added Successfully!. Task_id:", task_id)


# Function to View the tasks for a user
def view_task(username):
    task_df = pd.read_csv(tasks_file)
    user_tasks = task_df[task_df['username'] == username]

    if user_tasks.empty:
        print("No task found for user :", username)
        return

    for _, task in user_tasks.iterrows():
        print("Task ID :", task['taskId'], "Description :", task['description'], "Status :", task['status'])


# Function to update Task as completed
def update_task_completed(username):
    task_id = int(input("Please enter the task ID to be marked as completed :"))

    task_df = pd.read_csv(tasks_file)
    print(task_df[task_df['username'] == username]['taskId'].values)
    if task_id not in task_df[task_df['username'] == username]['taskId'].values:
        print("Invalid Task ID")
        return

    task_df.loc[(task_df['username'] == username) & (task_df['taskId'] == task_id), 'status'] = 'Completed'
    task_df.to_csv(tasks_file,index=False)
    print("Task Id", task_id, " Updated to Completed for username ", username, " !!")


# Function to delete the tasks
def delete_task(username):
    task_id = int(input("Please enter the task ID you want to delete :"))

    task_df = pd.read_csv(tasks_file)

    if task_id not in task_df[task_df['username'] == username]['taskId'].values:
        print("Invalid task Id for the user")
        return
    # Removing the row from dataframe where username and task_id matches
    # ~ negates the selection
    task_df=task_df[~((task_df['username'] == username) & (task_df['taskId'] == task_id))]
    task_df.to_csv(tasks_file, index=False)
    print("Task id ", task_id, " Deleted Successfully for username ", username)


# Interactive menu
def menu(username):
    while True:
        print("\nMenu")
        print("1. Add a Task")
        print("2. View Tasks")
        print("3. Mark a Task as Completed")
        print("4. Delete a Task")
        print("5. Logout")

        choice = input("Please enter your choice ")

        if choice == '1':
            add_task(username)
        elif choice == '2':
            view_task(username)
        elif choice == '3':
            update_task_completed(username)
        elif choice == '4':
            delete_task(username)
        elif choice == '5':
            print("Logging out")
            break
        else:
            print("Invalid Choice, Please try again")


# Main Function to initiate the call
def main():
    while True:
        print("Welcome to the task Manager")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Please enter your choice :")

        if choice == '1':
            register_user()
        elif choice == '2':
            username = login()
            if username:
                menu(username)
        elif choice == '3':
            break
        else:
            print("Invalid Choice, Please try again")


if __name__ == "__main__":
    main()