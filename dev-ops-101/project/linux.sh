#!/bin/bash

# Лог-файл для записи результатов обновления
LOG_FILE="/var/log/auto_update.log"

# Дата и время начала обновления
echo "[$(date)] Начало обновления и апгрейда пакетов..." >> $LOG_FILE

# Обновление списка пакетов
echo "[$(date)] Обновление списка пакетов..." >> $LOG_FILE
DEBIAN_FRONTEND=noninteractive sudo apt-get update -y >> $LOG_FILE 2>&1
if [ $? -ne 0 ]; then
    echo "[$(date)] Ошибка при обновлении списка пакетов" >> $LOG_FILE
    exit 1
fi

# Обновление установленных пакетов
echo "[$(date)] Обновление пакетов..." >> $LOG_FILE
DEBIAN_FRONTEND=noninteractive sudo apt-get upgrade -y >> $LOG_FILE 2>&1
if [ $? -ne 0 ]; then
    echo "[$(date)] Ошибка при обновлении пакетов" >> $LOG_FILE
    exit 1
fi

# Очистка кеша пакетов
echo "[$(date)] Очистка кеша пакетов..." >> $LOG_FILE
DEBIAN_FRONTEND=noninteractive sudo apt-get clean >> $LOG_FILE 2>&1
if [ $? -ne 0 ]; then
    echo "[$(date)] Ошибка при очистке кеша пакетов" >> $LOG_FILE
    exit 1
fi

# Завершение обновления
echo "[$(date)] Обновление завершено." >> $LOG_FILE

