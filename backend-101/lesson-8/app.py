import argparse
import json
import os

tasks = []

# Загрузка задач из текстового файла
def load_tasks():
    global tasks
    try:
        if not os.path.exists("tasks.json"):  # Проверка на наличие файла
            print("Файл данных не найден, создается новый.")
            tasks = []  # Если файл отсутствует, создается пустой список задач
        else:
            with open("tasks.json", "r", encoding="utf-8") as file:
                tasks = json.load(file)  # Загружаем задачи из JSON
    except json.JSONDecodeError:
        print("Ошибка при чтении JSON из файла. Файл поврежден или имеет неверный формат.")
        tasks = []  # Возвращаем пустой список задач, если ошибка в формате JSON
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        tasks = []  # Если произошла другая ошибка, создаем пустой список задач

# Сохранение задач в JSON-файл
def save_tasks():
    try:
        with open("tasks.json", "w", encoding="utf-8") as file:
            json.dump(tasks, file, ensure_ascii=False, indent=4)  # Сериализация в JSON
    except Exception as e:
        print(f"Ошибка при сохранении данных в файл: {e}")

def add_tasks(description):
    task = {"id": len(tasks) + 1, "description": description}
    tasks.append(task)
    save_tasks()  # Сохраняем задачи в файл после добавления
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

if __name__ == "__main__":
    main()
