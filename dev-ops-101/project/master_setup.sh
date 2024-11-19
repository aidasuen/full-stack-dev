#!/bin/bash

# Функция для проверки успешности выполнения команд
check_success() {
    if [ $? -eq 0 ]; then
        echo "$1 выполнен успешно!"
    else
        echo "Ошибка при выполнении: $1"
        exit 1
    fi
}

echo "Запуск мастер-скрипта..."

# Шаг 1: Обновление и апгрейд пакетов
echo "Шаг 1: Запуск скрипта для обновления и апгрейда пакетов linux"
bash /root/full-stack-dev/dev-ops-101/project/linux.sh
check_success "Обновление и апгрейд пакетов"

# Шаг 2: Установка Nginx
echo "Шаг 2: Запуск скрипта для установки Nginx..."
bash /root/full-stack-dev/dev-ops-101/project/nginx.sh
check_success "Установка Nginx"

# Шаг 3: Создание пользователей и групп
echo "Шаг 3: Запуск скрипта для создания пользователей и групп..."
bash /root/full-stack-dev/dev-ops-101/project/create_user.sh
check_success "Создание пользователей и групп"

# Шаг 4: Резервное копирование файлов
echo "Шаг 4: Запуск скрипта для резервного копирования файлов..."
bash /root/full-stack-dev/dev-ops-101/project/backup_configs.sh
check_success "Резервное копирование файлов"

echo "Все шаги выполнены успешно!"
