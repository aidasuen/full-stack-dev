#!/bin/bash

# Запрашиваем у пользователя полный путь к файлу для сохранения
read -p "Введите полный путь к файлу для сохранения: " file_path

# Проверяем, существует ли указанный файл
if [ ! -f "$file_path" ]; then
    echo "Ошибка: Файл '$file_path' не найден!"
    exit 1
fi

# Запрашиваем у пользователя имя для резервной копии файла
read -p "Введите имя для резервной копии файла: " backup_file_name

# Получаем текущую дату в формате YYYYMMDD
current_date=$(date +%Y%m%d)

# Указываем путь к директории backup_configs в домашнем каталоге
backup_dir="$HOME/backup_configs"

# Проверяем, существует ли директория backup_configs, если нет — создаем
if [ ! -d "$backup_dir" ]; then
    echo "Директория $backup_dir не существует. Создаю..."
    mkdir -p "$backup_dir"
fi

# Создаем имя для резервной копии с добавлением даты в имя
backup_file="$backup_dir/${backup_file_name}_$current_date"

# Копируем файл в директорию backup_configs с добавлением даты в имя файла
echo "Копирование файла '$file_path' в '$backup_file'..."
cp "$file_path" "$backup_file"

# Проверяем, успешно ли завершилась операция копирования
if [ $? -eq 0 ]; then
    echo "Резервная копия файла '$file_path' успешно сохранена как '$backup_file'."
else
    echo "Ошибка при копировании файла!"
    exit 1
fi













