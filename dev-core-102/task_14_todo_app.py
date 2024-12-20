import os
import json
from datetime import datetime, date  

def load_tasks(filename="dev-core-102/tasks.json"):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    print("Файл пуст.")
                    return []  
                return json.loads(content)
        except json.JSONDecodeError:
            print("Ошибка: файл поврежден или содержит некорректный JSON.")
            return []  
    return []

def save_tasks(tasks, filename="dev-core-102/tasks.json"):
    for task in tasks:
        if "deadline" in task:
            if isinstance(task["deadline"], date): 
                task["deadline"] = task["deadline"].strftime("%d-%m-%Y")  
            elif isinstance(task["deadline"], str):
                try:
                    task["deadline"] = datetime.strptime(task["deadline"], "%d-%m-%Y").strftime("%d-%m-%Y")
                except ValueError:
                    print(f"Ошибка: Неверный формат даты для задачи: {task['description']}")
                    task["deadline"] = "" 
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)

def add_task(tasks, description, deadline=None):
    task = {"description": description, "completed": False}
    if deadline:
        try:
            task["deadline"] = datetime.strptime(deadline, "%d-%m-%Y").date()  
        except ValueError:
            print("Некорректный формат даты. Используйте формат dd-mm-yyyy.")
            return
    tasks.append(task)

def remove_task(tasks, index):
    try:
        tasks.pop(index)
    except IndexError:
        print("Ошибка: задачи с таким номером не существует.")

def view_tasks(tasks):
    if not tasks:
        print("Нет задач для отображения.")
        return
    for idx, task in enumerate(tasks, 1):
        status = "Выполнена" if task["completed"] else "Не выполнена"
        deadline = f" Срок: {task['deadline']}" if "deadline" in task and task["deadline"] else ""
        print(f"{idx}. {task['description']}{deadline} - {status}")

def mark_task_completed(tasks, index):
    try:
        tasks[index]["completed"] = True
    except IndexError:
        print("Ошибка: задачи с таким номером не существует.")

def main():
    tasks = load_tasks()
    
    while True:
        print("\nКоманды:")
        print("add - добавить задачу")
        print("remove - удалить задачу")
        print("view - показать все задачи")
        print("complete - пометить задачу как выполненную")
        print("exit - завершить программу")

        command = input("Введите команду: ").strip().lower()

        if command == "add":
            description = input("Введите описание задачи: ").strip()
            deadline = input("Введите срок выполнения задачи (формат dd-mm-yyyy, необязательно): ").strip()
            add_task(tasks, description, deadline)
            save_tasks(tasks)
        
        elif command == "remove":
            try:
                index = int(input("Введите номер задачи для удаления: ")) - 1
                remove_task(tasks, index)
                save_tasks(tasks)
            except ValueError:
                print("Ошибка: введите корректный номер задачи.")
        
        elif command == "view":
            view_tasks(tasks)
        
        elif command == "complete":
            try:
                index = int(input("Введите номер задачи, которую нужно отметить как выполненную: ")) - 1
                mark_task_completed(tasks, index)
                save_tasks(tasks)
            except ValueError:
                print("Ошибка: введите корректный номер задачи.")
        
        elif command == "exit":
            print("Выход из программы.")
            break
        
        else:
            print("Неизвестная команда. Пожалуйста, выберите одну из предложенных команд.")

if __name__ == "__main__":
    main()
