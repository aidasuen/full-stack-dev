import argparse

tasks = []

# Загрузка задач из текстового файла
def load_tasks():
    global tasks
    try:
        with open("tasks.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            tasks = [{"id": idx + 1, "description": line.strip()} for idx, line in enumerate(lines)]
    except FileNotFoundError:
        tasks = []

# Сохранение задач в текстовый файл
def save_tasks():
    with open("tasks.txt", "w", encoding="utf-8") as file:
        for task in tasks:
            file.write(task["description"] + "\n")

def add_tasks(description):
    task = {"id": len(tasks) + 1, "description": description}
    tasks.append(task)
    save_tasks()  # Сохраняем задачи в файл
    print(f"Задача добавлена: {task['description']}")

def view_tasks():
    if not tasks:
        print("Нет задач.")
        return
    for task in tasks:
        print(f"ID: {task['id']} - {task['description']}")

def update_tasks(task_id, new_description):
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = new_description
            save_tasks()  # Сохраняем задачи в файл после обновления
            print(f"Задача ID {task_id} обновлена на: {new_description}")
            return
    print(f"Задача с ID {task_id} не найдена.")

def delete_tasks(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks()  # Сохраняем задачи в файл после удаления
    print(f"Задача с ID {task_id} удалена.")

def main():
    load_tasks()  # Загружаем задачи из файла при старте программы
    parser = argparse.ArgumentParser(description="Управление задачами")
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add', help='Добавить задачу')
    add_parser.add_argument('--description', type=str, required=True, help='Описание задачи')

    view_parser = subparsers.add_parser('view', help='Просмотреть все задачи')

    update_parser = subparsers.add_parser('update', help='Обновить описание задачи')
    update_parser.add_argument('--id', type=int, required=True, help='ID задачи')
    update_parser.add_argument('--description', type=str, required=True, help='Новое описание задачи')

    delete_parser = subparsers.add_parser('delete', help='Удалить задачу')
    delete_parser.add_argument('--id', type=int, required=True, help='ID задачи')

    args = parser.parse_args()

    if args.command == 'add':
        add_tasks(args.description)
    elif args.command == 'view':
        view_tasks()
    elif args.command == 'update':
        update_tasks(args.id, args.description)
    elif args.command == 'delete':
        delete_tasks(args.id)
    else:
        print("Неизвестная команда.")

    save_tasks()  # Сохраняем задачи в файл после завершения работы

if __name__ == "__main__":
    main()

