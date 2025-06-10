import requests
import sys
 
API_URL = "http://127.0.0.1:8000"
  
def create_task():
    title = input("Title: ")
    description = input("Description (optional): ")
    status = input("Status (pending/completed) [pending]: ") or "pending"
    due_date = input("Due date (YYYY-MM-DD) (optional): ")
    priority = input("Priority (low/medium/high) : ") or "medium"
 
    data = {
        "title": title,
        "description": description if description else None,
        "status": status,
        "due_date": due_date if due_date else None,
        "priority": priority
    }
 
    response = requests.post(f"{API_URL}/tasks/", json=data)
    if response.status_code == 201:
        print("Task created:", response.json())
    else:
        print("Error:", response.text)
 
def view_all_tasks():
    response = requests.get(f"{API_URL}/tasks/")
    if response.status_code == 200:
        tasks = response.json()
        if not tasks:
            print("No tasks found.")
            return
        print("Tasks:")
        print(f"{'ID':<9} {'Title':<20} {'Status':<10} {'Due Date':<12} {'Priority':<8}")
        print("-" * 60)
        for t in tasks:
            print(f"{t['id']:<9} {t['title'][:20]:<20} {t['status']:<10} {str(t['due_date'] or ''):<12} {t['priority']:<8}")
    else:
        print("Error fetching tasks:", response.text)
 
def view_task_by_id():
    try:
        task_id = int(input("Enter task ID: "))
    except ValueError:
        print("Invalid input")
        return
    response = requests.get(f"{API_URL}/tasks/{task_id}")
    if response.status_code == 200:
        t = response.json()
        print(f"ID: {t['id']}\nTitle: {t['title']}\nDescription: {t.get('description')}\nStatus: {t['status']}\nDue Date: {t.get('due_date')}\nPriority: {t['priority']}")
    else:
        print("Task not found.")
 
def update_task():
    try:
        task_id = int(input("Enter task ID to update: "))
    except ValueError:
        print("Invalid input")
        return
 
    data = {}
    title = input("New title (leave blank to skip): ")
    if title:
        data["title"] = title
 
    description = input("New description (leave blank to skip): ")
    if description:
        data["description"] = description
 
    status = input("New status (pending/completed, leave blank to skip): ")
    if status:
        data["status"] = status
 
    due_date = input("New due date (YYYY-MM-DD, leave blank to skip): ")
    if due_date:
        data["due_date"] = due_date
 
    priority = input("New priority (low/medium/high, leave blank to skip): ")
    if priority:
        data["priority"] = priority
 
    if not data:
        print("Nothing to update.")
        return
 
    response = requests.put(f"{API_URL}/tasks/{task_id}", json=data)
    if response.status_code == 200:
        print("Task updated:", response.json())
    else:
        print("Error updating task:", response.text)
 
def delete_task():
    try:
        task_id = int(input("Enter task ID to delete: "))
    except ValueError:
        print("Invalid input")
        return
    response = requests.delete(f"{API_URL}/tasks/{task_id}")
    if response.status_code == 204:
        print("Task deleted.")
    else:
        print("Error deleting task:", response.text)
 
def main():
    while True:
        print("\nTO-DO LIST MENU")
        print("1. Create Task")
        print("2. View All Tasks")
        print("3. View Task by ID")
        print("4. Update Task")
        print("5. Delete Task")
        print("6. Exit")
 
        choice = input("Enter choice: ")
 
        if choice == '1':
            create_task()
        elif choice == '2':
            view_all_tasks()
        elif choice == '3':
            view_task_by_id()
        elif choice == '4':
            update_task()
        elif choice == '5':
            delete_task()
        elif choice == '6':
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.")
 
if __name__ == "__main__":
    main()
 
