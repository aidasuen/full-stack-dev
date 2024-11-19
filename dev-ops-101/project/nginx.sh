#!/bin/bash

# Лог-файл для записи результатов установки
LOG_FILE="/var/log/nginx.log"

# Дата и время начала установки
echo "[$(date)] Начало установки Nginx..." >> $LOG_FILE

# Установка Nginx
echo "[$(date)] Установка Nginx..." >> $LOG_FILE
sudo apt-get install -y nginx >> $LOG_FILE 2>&1

# Запуск Nginx
echo "[$(date)] Запуск Nginx..." >> $LOG_FILE
sudo systemctl start nginx >> $LOG_FILE 2>&1

# Включение Nginx в автозагрузку
echo "[$(date)] Включение Nginx в автозагрузку..." >> $LOG_FILE
sudo systemctl enable nginx >> $LOG_FILE 2>&1

# Проверка статуса службы Nginx
echo "[$(date)] Проверка статуса службы Nginx..." >> $LOG_FILE
STATUS=$(sudo systemctl is-active nginx)

if [ "$STATUS" == "active" ]; then
    echo "[$(date)] Nginx работает и активен." >> $LOG_FILE
else
    echo "[$(date)] Nginx не запущен! Статус: $STATUS" >> $LOG_FILE
    sudo systemctl status nginx >> $LOG_FILE 2>&1
    exit 1  # Завершаем скрипт с ошибкой, если Nginx не работает
fi

# Завершение установки
echo "[$(date)] Установка Nginx завершена." >> $LOG_FILE
