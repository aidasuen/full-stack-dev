import os

def print_directory_structure(directory, indent=0):
    try:
        items = os.listdir(directory)
        for item in items:
            item_path = os.path.join(directory, item)
            print(' ' * indent + item)
            if os.path.isdir(item_path):
                print_directory_structure(item_path, indent + 2)
    except PermissionError:
        print(' ' * indent + '[Доступ запрещен]')
    except FileNotFoundError:
        print(' ' * indent + '[Папка не найдена]')

def search_file(directory, filename):
    try:
        items = os.listdir(directory)
        for item in items:
            item_path = os.path.join(directory, item)
            if item == filename:
                return item_path
            if os.path.isdir(item_path):
                result = search_file(item_path, filename)
                if result:
                    return result
    except PermissionError:
        return None
    except FileNotFoundError:
        return None
    return None

def calculate_total_size(directory):
    total_size = 0
    try:
        items = os.listdir(directory)
        for item in items:
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                total_size += os.path.getsize(item_path)
            elif os.path.isdir(item_path):
                total_size += calculate_total_size(item_path)
    except PermissionError:
        pass
    except FileNotFoundError:
        pass
    return total_size

if __name__ == "__main__":
    directory = 'front-end-101/final_project_plan'


    print("Структура директорий и файлов:")
    print_directory_structure(directory)

    filename_to_search = 'final_project_plan.md'
    result = search_file(directory, filename_to_search)
    if result:
        print(f"Файл найден: {result}")
    else:
        print(f"Файл '{filename_to_search}' не найден.")

    total_size = calculate_total_size(directory)
    print(f"Общий размер файлов в директории: {total_size} байт")
