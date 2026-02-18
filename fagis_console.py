import os
import sys
import time
import webbrowser
import requests
import re
import random
import math
import hashlib
import json
import socket
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Callable, Any
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import urllib.parse
import platform



class Config:
    VERSION = "2.0"
    VERSION_URL = "https://raw.githubusercontent.com/kubydog101/fagis-console/refs/heads/main/ver.txt"
    DOWNLOAD_URL = "https://github.com/kubydog101/fagis-console/releases/latest"
    MALICIOUS_DB_URL = "https://raw.githubusercontent.com/kubydog101/fagis-console/refs/heads/main/scam-db.txt"
    MAX_COMMAND_HISTORY = 100
    REQUEST_TIMEOUT = 10
    NOTES_FILE = "notes.json"



class Colors:
    HEADER = '\033[95m' if os.name != 'nt' else ''
    BLUE = '\033[94m' if os.name != 'nt' else ''
    CYAN = '\033[96m' if os.name != 'nt' else ''
    GREEN = '\033[92m' if os.name != 'nt' else ''
    WARNING = '\033[93m' if os.name != 'nt' else ''
    FAIL = '\033[91m' if os.name != 'nt' else ''
    ENDC = '\033[0m' if os.name != 'nt' else ''
    BOLD = '\033[1m' if os.name != 'nt' else ''
    UNDERLINE = '\033[4m' if os.name != 'nt' else ''



@dataclass
class FileInfo:
    """Информация о файле/директории"""
    name: str
    path: str
    is_dir: bool
    size: int
    modified: datetime

@dataclass
class Note:
    """Заметка"""
    id: int
    title: str
    content: str
    created: datetime
    updated: datetime

class SecurityLevel(Enum):
    """Уровни безопасности URL"""
    SAFE = "safe"
    SUSPICIOUS = "suspicious"
    MALICIOUS = "malicious"
    UNKNOWN = "unknown"



class TranslationManager:
    """Менеджер переводов"""
    
    def __init__(self, lang: str = 'en'):
        self.lang = lang
        self.translations = self._load_translations()
    
    def _load_translations(self):
        """Загрузка переводов"""
        en = {
            'welcome': f"{Colors.GREEN}┌─────────────────────────────────────────────┐{Colors.ENDC}\n"
                      f"{Colors.GREEN}│{Colors.ENDC}           {Colors.BOLD}FAGIS Console OS v{{}}{Colors.ENDC}           {Colors.GREEN}│{Colors.ENDC}\n"
                      f"{Colors.GREEN}└─────────────────────────────────────────────┘{Colors.ENDC}",
            'language_choice': f"{Colors.CYAN}Select language:{Colors.ENDC}\n1. English\n2. Русский\n{Colors.CYAN}> {Colors.ENDC}",
            'invalid_choice': f"{Colors.WARNING}Invalid choice. Defaulting to English.{Colors.ENDC}",
            'prompt': f"{Colors.GREEN}{{}}@{{}}{Colors.ENDC}:{Colors.BLUE}{{}}{Colors.ENDC}{Colors.GREEN}$ {Colors.ENDC}",
            'current_time': f"{Colors.CYAN}Current time:{Colors.ENDC} {{}}",
            'current_date': f"{Colors.CYAN}Today's date:{Colors.ENDC} {{}}",
            'current_user': f"{Colors.CYAN}Current user:{Colors.ENDC} {{}}",
            'current_dir': f"{Colors.CYAN}Current directory:{Colors.ENDC} {{}}",
            'dir_content': f"{Colors.BOLD}Contents of {{}}:{Colors.ENDC}",
            'dir_not_found': f"{Colors.FAIL}Directory not found:{Colors.ENDC} {{}}",
            'file_created': f"{Colors.GREEN}File created:{Colors.ENDC} {{}}",
            'dir_created': f"{Colors.GREEN}Directory created:{Colors.ENDC} {{}}",
            'file_deleted': f"{Colors.GREEN}File deleted:{Colors.ENDC} {{}}",
            'dir_deleted': f"{Colors.GREEN}Directory deleted:{Colors.ENDC} {{}}",
            'unknown_cmd': f"{Colors.FAIL}Command not found:{Colors.ENDC} {{}}. {Colors.CYAN}Type 'help' for available commands.{Colors.ENDC}",
            'exit_msg': f"{Colors.WARNING}Shutting down system...{Colors.ENDC}",
            'help_title': f"{Colors.BOLD}Available commands:{Colors.ENDC}",
            'help_format': f"  {Colors.GREEN}{{:<12}}{Colors.ENDC} {{}}",
            'calc_title': f"{Colors.BOLD}Calculator (type 'exit' to quit){Colors.ENDC}",
            'calc_prompt': f"{Colors.CYAN}Enter expression>{Colors.ENDC} ",
            'calc_result': f"{Colors.GREEN}Result:{Colors.ENDC} {{}}",
            'calc_error': f"{Colors.FAIL}Calculation error:{Colors.ENDC} {{}}",
            'game_title': f"{Colors.BOLD}Guess the number (1-10)!{Colors.ENDC}",
            'game_prompt': f"{Colors.CYAN}Attempt {{}}/3:{Colors.ENDC} ",
            'game_win': f"{Colors.GREEN}Congratulations! You guessed correctly!{Colors.ENDC}",
            'game_loss': f"{Colors.FAIL}Game over! The number was:{Colors.ENDC} {{}}",
            'game_invalid': f"{Colors.WARNING}Please enter a valid number!{Colors.ENDC}",
            'no_file_name': f"{Colors.FAIL}Error:{Colors.ENDC} Please specify a file name",
            'no_dir_name': f"{Colors.FAIL}Error:{Colors.ENDC} Please specify a directory name",
            'no_text': f"{Colors.FAIL}Error:{Colors.ENDC} Please specify text to display",
            'update_available': f"{Colors.WARNING}UPDATE AVAILABLE!{Colors.ENDC}\n{Colors.CYAN}Current version:{Colors.ENDC} {{}}\n{Colors.CYAN}Latest version:{Colors.ENDC} {{}}",
            'update_menu': f"\n{Colors.CYAN}Options:{Colors.ENDC}\n1. Download update\n2. Skip\n{Colors.CYAN}> {Colors.ENDC}",
            'update_downloading': f"{Colors.GREEN}Opening download page in browser...{Colors.ENDC}",
            'update_skipped': f"{Colors.WARNING}Update check skipped.{Colors.ENDC}",
            'update_error': f"{Colors.FAIL}Failed to check updates:{Colors.ENDC} {{}}",
            'update_latest': f"{Colors.GREEN}You have the latest version ({{}}){Colors.ENDC}",
            'checking_update': f"{Colors.CYAN}Checking for updates...{Colors.ENDC}",
            'safe_url': f"{Colors.GREEN}✓ Safe:{Colors.ENDC} {{}}",
            'malicious_url': f"{Colors.FAIL}✗ MALICIOUS:{Colors.ENDC} {{}}",
            'suspicious_url': f"{Colors.WARNING}⚠ Suspicious:{Colors.ENDC} {{}}",
            'url_not_recognized': f"{Colors.WARNING}? Not recognized:{Colors.ENDC} {{}}",
            'check_error': f"{Colors.FAIL}Security check error:{Colors.ENDC} {{}}",
            'malicious_db_error': f"{Colors.FAIL}Failed to load malicious URLs database:{Colors.ENDC} {{}}",
            'enter_url': f"{Colors.CYAN}Enter URL to check>{Colors.ENDC} ",
            'checking_urls': f"{Colors.CYAN}Scanning for malicious links...{Colors.ENDC}",
            'clean_content': f"{Colors.GREEN}✓ Content appears clean. No malicious links detected.{Colors.ENDC}",
            'internet_connected': f"{Colors.GREEN}✓ Internet connection:{Colors.ENDC} Active",
            'internet_failed': f"{Colors.FAIL}✗ Internet connection:{Colors.ENDC} Failed ({{}})",
            'malicious_db_loaded': f"{Colors.GREEN}Loaded {{}} malicious URL patterns{Colors.ENDC}",
            'malicious_db_empty': f"{Colors.WARNING}Warning: Malicious URL database is empty{Colors.ENDC}",
            'command_history': f"{Colors.BOLD}Command history:{Colors.ENDC}",
            'no_history': "No commands in history",
            'file_not_found': f"{Colors.FAIL}File not found:{Colors.ENDC} {{}}",
            'permission_denied': f"{Colors.FAIL}Permission denied:{Colors.ENDC} {{}}",
            'system_info': f"{Colors.BOLD}System Information:{Colors.ENDC}\n"
                          f"  OS: {{}}\n"
                          f"  Python: {{}}\n"
                          f"  Current time: {{}}\n"
                          f"  Working directory: {{}}",
            
            
            'hash_title': f"{Colors.BOLD}Hash Calculator:{Colors.ENDC}",
            'hash_prompt': f"{Colors.CYAN}Enter text to hash:{Colors.ENDC} ",
            'hash_result': "MD5: {}\nSHA1: {}\nSHA256: {}",
            'hash_file_prompt': f"{Colors.CYAN}Enter file path:{Colors.ENDC} ",
            'hash_file_result': "File {}:\nMD5: {}\nSHA256: {}",
            'hash_file_not_found': f"{Colors.FAIL}File not found:{Colors.ENDC} {{}}",
            'timer_title': f"{Colors.BOLD}Timer:{Colors.ENDC}",
            'timer_prompt': f"{Colors.CYAN}Enter seconds (or mm:ss):{Colors.ENDC} ",
            'timer_started': "Timer started for {}",
            'timer_done': f"{Colors.GREEN}Time's up!{Colors.ENDC}",
            'timer_cancelled': "Timer cancelled",
            'stopwatch_title': f"{Colors.BOLD}Stopwatch:{Colors.ENDC}",
            'stopwatch_controls': "Controls: [s]tart, p/a[u]se, [r]eset, [q]uit",
            'stopwatch_time': "Elapsed: {}",
            'notes_title': f"{Colors.BOLD}Notes Manager:{Colors.ENDC}",
            'notes_commands': "Commands: list, add <title>, view <id>, edit <id>, delete <id>, search <text>",
            'notes_list': "Notes:",
            'notes_empty': "No notes",
            'notes_added': f"{Colors.GREEN}Note added with ID {{}}{Colors.ENDC}",
            'notes_deleted': f"{Colors.GREEN}Note deleted{Colors.ENDC}",
            'notes_not_found': f"{Colors.FAIL}Note not found{Colors.ENDC}",
            'notes_content': f"{Colors.BOLD}Title:{{}} {{}}{Colors.ENDC}\nCreated: {{}}\nUpdated: {{}}\n\n{{}}",
            'notes_search_results': "Search results for '{}':",
            'notes_edit_instructions': "Enter new content (Ctrl+D to save, Ctrl+C to cancel):",
            'port_scan_title': f"{Colors.BOLD}Port Scanner:{Colors.ENDC}",
            'port_scan_prompt': f"{Colors.CYAN}Enter host:{Colors.ENDC} ",
            'port_scan_range': f"{Colors.CYAN}Enter port range (e.g., 1-1024):{Colors.ENDC} ",
            'port_scanning': "Scanning {} for open ports...",
            'port_open': f"{Colors.GREEN}Port {{}} is open{Colors.ENDC}",
            'port_closed': "Port {} is closed",
            'port_error': f"{Colors.FAIL}Error scanning port {{}}:{{}} {{}}{Colors.ENDC}",
            'port_scan_done': f"{Colors.GREEN}Scan complete. Found {{}} open ports.{Colors.ENDC}",
            'password_title': f"{Colors.BOLD}Password Generator:{Colors.ENDC}",
            'password_prompt': f"{Colors.CYAN}Enter password length (8-64):{Colors.ENDC} ",
            'password_options': "Include:\n1. Lowercase\n2. Uppercase\n3. Numbers\n4. Special chars\n5. All\n> ",
            'password_result': "Generated password: {}",
            'password_strength': "Strength: {}",
            'translate_title': f"{Colors.BOLD}Simple Translator (using mymemory API):{Colors.ENDC}",
            'translate_prompt': f"{Colors.CYAN}Enter text to translate:{Colors.ENDC} ",
            'translate_from': f"{Colors.CYAN}From language (en/ru/fr/de/es):{Colors.ENDC} ",
            'translate_to': f"{Colors.CYAN}To language (en/ru/fr/de/es):{Colors.ENDC} ",
            'translate_result': "Translation: {}",
            'translate_error': f"{Colors.FAIL}Translation failed:{Colors.ENDC} {{}}",
            'qr_title': f"{Colors.BOLD}QR Code Generator (uses qrencode):{Colors.ENDC}",
            'qr_prompt': f"{Colors.CYAN}Enter text for QR code:{Colors.ENDC} ",
            'qr_error': f"{Colors.FAIL}QR generation failed:{Colors.ENDC} {{}}",
            'qr_not_installed': f"{Colors.WARNING}qrencode not installed. Install with: sudo apt install qrencode{Colors.ENDC}",
            'qr_saved': f"{Colors.GREEN}QR code saved as {{}}{Colors.ENDC}",
            'reminder_title': f"{Colors.BOLD}Reminder:{Colors.ENDC}",
            'reminder_prompt': f"{Colors.CYAN}Enter reminder message:{Colors.ENDC} ",
            'reminder_time': f"{Colors.CYAN}Enter seconds until reminder:{Colors.ENDC} ",
            'reminder_set': f"{Colors.GREEN}Reminder set for {{}} seconds{Colors.ENDC}",
            'reminder_alert': f"{Colors.WARNING}REMINDER:{{}} {{}}{Colors.ENDC}",
            'unit_converter_title': f"{Colors.BOLD}Unit Converter:{Colors.ENDC}",
            'unit_converter_menu': "1. Length (m, km, mile, ft)\n2. Weight (kg, g, lb, oz)\n3. Temperature (C, F, K)\n4. Speed (km/h, mph, m/s)\n> ",
            'unit_converter_from': f"{Colors.CYAN}From:{Colors.ENDC} ",
            'unit_converter_to': f"{Colors.CYAN}To:{Colors.ENDC} ",
            'unit_converter_value': f"{Colors.CYAN}Value:{Colors.ENDC} ",
            'unit_converter_result': "{} {} = {} {}",
            'unit_converter_error': f"{Colors.FAIL}Invalid conversion{Colors.ENDC}",
        }
        
        ru = {
            'welcome': f"{Colors.GREEN}┌─────────────────────────────────────────────┐{Colors.ENDC}\n"
                      f"{Colors.GREEN}│{Colors.ENDC}           {Colors.BOLD}FAGIS Console OS v{{}}{Colors.ENDC}           {Colors.GREEN}│{Colors.ENDC}\n"
                      f"{Colors.GREEN}└─────────────────────────────────────────────┘{Colors.ENDC}",
            'language_choice': f"{Colors.CYAN}Выберите язык:{Colors.ENDC}\n1. English\n2. Русский\n{Colors.CYAN}> {Colors.ENDC}",
            'invalid_choice': f"{Colors.WARNING}Некорректный выбор. Используется русский.{Colors.ENDC}",
            'prompt': f"{Colors.GREEN}{{}}@{{}}{Colors.ENDC}:{Colors.BLUE}{{}}{Colors.ENDC}{Colors.GREEN}$ {Colors.ENDC}",
            'current_time': f"{Colors.CYAN}Текущее время:{Colors.ENDC} {{}}",
            'current_date': f"{Colors.CYAN}Сегодняшняя дата:{Colors.ENDC} {{}}",
            'current_user': f"{Colors.CYAN}Текущий пользователь:{Colors.ENDC} {{}}",
            'current_dir': f"{Colors.CYAN}Текущая директория:{Colors.ENDC} {{}}",
            'dir_content': f"{Colors.BOLD}Содержимое {{}}:{Colors.ENDC}",
            'dir_not_found': f"{Colors.FAIL}Директория не найдена:{Colors.ENDC} {{}}",
            'file_created': f"{Colors.GREEN}Файл создан:{Colors.ENDC} {{}}",
            'dir_created': f"{Colors.GREEN}Директория создана:{Colors.ENDC} {{}}",
            'file_deleted': f"{Colors.GREEN}Файл удален:{Colors.ENDC} {{}}",
            'dir_deleted': f"{Colors.GREEN}Директория удалена:{Colors.ENDC} {{}}",
            'unknown_cmd': f"{Colors.FAIL}Команда не найдена:{Colors.ENDC} {{}}. {Colors.CYAN}Введите 'help' для справки.{Colors.ENDC}",
            'exit_msg': f"{Colors.WARNING}Завершение работы системы...{Colors.ENDC}",
            'help_title': f"{Colors.BOLD}Доступные команды:{Colors.ENDC}",
            'help_format': f"  {Colors.GREEN}{{:<12}}{Colors.ENDC} {{}}",
            'calc_title': f"{Colors.BOLD}Калькулятор (введите 'exit' для выхода){Colors.ENDC}",
            'calc_prompt': f"{Colors.CYAN}Введите выражение>{Colors.ENDC} ",
            'calc_result': f"{Colors.GREEN}Результат:{Colors.ENDC} {{}}",
            'calc_error': f"{Colors.FAIL}Ошибка вычисления:{Colors.ENDC} {{}}",
            'game_title': f"{Colors.BOLD}Угадайте число от 1 до 10!{Colors.ENDC}",
            'game_prompt': f"{Colors.CYAN}Попытка {{}}/3:{Colors.ENDC} ",
            'game_win': f"{Colors.GREEN}Поздравляем! Вы угадали!{Colors.ENDC}",
            'game_loss': f"{Colors.FAIL}Игра окончена! Загаданное число:{Colors.ENDC} {{}}",
            'game_invalid': f"{Colors.WARNING}Пожалуйста, введите число!{Colors.ENDC}",
            'no_file_name': f"{Colors.FAIL}Ошибка:{Colors.ENDC} Укажите имя файла",
            'no_dir_name': f"{Colors.FAIL}Ошибка:{Colors.ENDC} Укажите имя директории",
            'no_text': f"{Colors.FAIL}Ошибка:{Colors.ENDC} Укажите текст для вывода",
            'update_available': f"{Colors.WARNING}ДОСТУПНО ОБНОВЛЕНИЕ!{Colors.ENDC}\n{Colors.CYAN}Текущая версия:{Colors.ENDC} {{}}\n{Colors.CYAN}Новая версия:{Colors.ENDC} {{}}",
            'update_menu': f"\n{Colors.CYAN}Варианты:{Colors.ENDC}\n1. Скачать обновление\n2. Пропустить\n{Colors.CYAN}> {Colors.ENDC}",
            'update_downloading': f"{Colors.GREEN}Открываю страницу загрузки в браузере...{Colors.ENDC}",
            'update_skipped': f"{Colors.WARNING}Проверка обновлений пропущена.{Colors.ENDC}",
            'update_error': f"{Colors.FAIL}Ошибка проверки обновлений:{Colors.ENDC} {{}}",
            'update_latest': f"{Colors.GREEN}У вас последняя версия ({{}}){Colors.ENDC}",
            'checking_update': f"{Colors.CYAN}Проверка обновлений...{Colors.ENDC}",
            'safe_url': f"{Colors.GREEN}✓ Безопасно:{Colors.ENDC} {{}}",
            'malicious_url': f"{Colors.FAIL}✗ ОПАСНО:{Colors.ENDC} {{}}",
            'suspicious_url': f"{Colors.WARNING}⚠ Подозрительно:{Colors.ENDC} {{}}",
            'url_not_recognized': f"{Colors.WARNING}? Не распознано:{Colors.ENDC} {{}}",
            'check_error': f"{Colors.FAIL}Ошибка проверки:{Colors.ENDC} {{}}",
            'malicious_db_error': f"{Colors.FAIL}Ошибка загрузки базы опасных ссылок:{Colors.ENDC} {{}}",
            'enter_url': f"{Colors.CYAN}Введите URL для проверки>{Colors.ENDC} ",
            'checking_urls': f"{Colors.CYAN}Поиск опасных ссылок...{Colors.ENDC}",
            'clean_content': f"{Colors.GREEN}✓ Вредоносные ссылки не обнаружены.{Colors.ENDC}",
            'internet_connected': f"{Colors.GREEN}✓ Интернет-соединение:{Colors.ENDC} Активно",
            'internet_failed': f"{Colors.FAIL}✗ Интернет-соединение:{Colors.ENDC} Недоступно ({{}})",
            'malicious_db_loaded': f"{Colors.GREEN}Загружено {{}} шаблонов опасных URL{Colors.ENDC}",
            'malicious_db_empty': f"{Colors.WARNING}Предупреждение: База опасных URL пуста{Colors.ENDC}",
            'command_history': f"{Colors.BOLD}История команд:{Colors.ENDC}",
            'no_history': "Нет команд в истории",
            'file_not_found': f"{Colors.FAIL}Файл не найден:{Colors.ENDC} {{}}",
            'permission_denied': f"{Colors.FAIL}Отказано в доступе:{Colors.ENDC} {{}}",
            'system_info': f"{Colors.BOLD}Информация о системе:{Colors.ENDC}\n"
                          f"  ОС: {{}}\n"
                          f"  Python: {{}}\n"
                          f"  Текущее время: {{}}\n"
                          f"  Рабочая директория: {{}}",
            
            
            'hash_title': f"{Colors.BOLD}Калькулятор хешей:{Colors.ENDC}",
            'hash_prompt': f"{Colors.CYAN}Введите текст для хеширования:{Colors.ENDC} ",
            'hash_result': "MD5: {}\nSHA1: {}\nSHA256: {}",
            'hash_file_prompt': f"{Colors.CYAN}Введите путь к файлу:{Colors.ENDC} ",
            'hash_file_result': "Файл {}:\nMD5: {}\nSHA256: {}",
            'hash_file_not_found': f"{Colors.FAIL}Файл не найден:{Colors.ENDC} {{}}",
            'timer_title': f"{Colors.BOLD}Таймер:{Colors.ENDC}",
            'timer_prompt': f"{Colors.CYAN}Введите секунды (или мм:сс):{Colors.ENDC} ",
            'timer_started': "Таймер запущен на {}",
            'timer_done': f"{Colors.GREEN}Время вышло!{Colors.ENDC}",
            'timer_cancelled': "Таймер отменен",
            'stopwatch_title': f"{Colors.BOLD}Секундомер:{Colors.ENDC}",
            'stopwatch_controls': "Управление: [s]тарт, [p]ауза, [r]есет, [q]выход",
            'stopwatch_time': "Прошло: {}",
            'notes_title': f"{Colors.BOLD}Менеджер заметок:{Colors.ENDC}",
            'notes_commands': "Команды: list, add <название>, view <id>, edit <id>, delete <id>, search <текст>",
            'notes_list': "Заметки:",
            'notes_empty': "Нет заметок",
            'notes_added': f"{Colors.GREEN}Заметка добавлена с ID {{}}{Colors.ENDC}",
            'notes_deleted': f"{Colors.GREEN}Заметка удалена{Colors.ENDC}",
            'notes_not_found': f"{Colors.FAIL}Заметка не найдена{Colors.ENDC}",
            'notes_content': f"{Colors.BOLD}Название:{{}} {{}}{Colors.ENDC}\nСоздано: {{}}\nОбновлено: {{}}\n\n{{}}",
            'notes_search_results': "Результаты поиска по '{}':",
            'notes_edit_instructions': "Введите новый текст (Ctrl+D для сохранения, Ctrl+C для отмены):",
            'port_scan_title': f"{Colors.BOLD}Сканер портов:{Colors.ENDC}",
            'port_scan_prompt': f"{Colors.CYAN}Введите хост:{Colors.ENDC} ",
            'port_scan_range': f"{Colors.CYAN}Введите диапазон портов (например, 1-1024):{Colors.ENDC} ",
            'port_scanning': "Сканирование {} на открытые порты...",
            'port_open': f"{Colors.GREEN}Порт {{}} открыт{Colors.ENDC}",
            'port_closed': "Порт {} закрыт",
            'port_error': f"{Colors.FAIL}Ошибка сканирования порта {{}}:{{}} {{}}{Colors.ENDC}",
            'port_scan_done': f"{Colors.GREEN}Сканирование завершено. Найдено {{}} открытых портов.{Colors.ENDC}",
            'password_title': f"{Colors.BOLD}Генератор паролей:{Colors.ENDC}",
            'password_prompt': f"{Colors.CYAN}Введите длину пароля (8-64):{Colors.ENDC} ",
            'password_options': "Включить:\n1. Строчные буквы\n2. Заглавные буквы\n3. Цифры\n4. Спецсимволы\n5. Все\n> ",
            'password_result': "Сгенерированный пароль: {}",
            'password_strength': "Сложность: {}",
            'translate_title': f"{Colors.BOLD}Простой переводчик (использует mymemory API):{Colors.ENDC}",
            'translate_prompt': f"{Colors.CYAN}Введите текст для перевода:{Colors.ENDC} ",
            'translate_from': f"{Colors.CYAN}С какого языка (en/ru/fr/de/es):{Colors.ENDC} ",
            'translate_to': f"{Colors.CYAN}На какой язык (en/ru/fr/de/es):{Colors.ENDC} ",
            'translate_result': "Перевод: {}",
            'translate_error': f"{Colors.FAIL}Ошибка перевода:{Colors.ENDC} {{}}",
            'qr_title': f"{Colors.BOLD}Генератор QR-кода (требуется qrencode):{Colors.ENDC}",
            'qr_prompt': f"{Colors.CYAN}Введите текст для QR-кода:{Colors.ENDC} ",
            'qr_error': f"{Colors.FAIL}Ошибка генерации QR:{Colors.ENDC} {{}}",
            'qr_not_installed': f"{Colors.WARNING}qrencode не установлен. Установите: sudo apt install qrencode{Colors.ENDC}",
            'qr_saved': f"{Colors.GREEN}QR-код сохранен как {{}}{Colors.ENDC}",
            'reminder_title': f"{Colors.BOLD}Напоминание:{Colors.ENDC}",
            'reminder_prompt': f"{Colors.CYAN}Введите текст напоминания:{Colors.ENDC} ",
            'reminder_time': f"{Colors.CYAN}Введите секунды до напоминания:{Colors.ENDC} ",
            'reminder_set': f"{Colors.GREEN}Напоминание установлено на {{}} секунд{Colors.ENDC}",
            'reminder_alert': f"{Colors.WARNING}НАПОМИНАНИЕ:{{}} {{}}{Colors.ENDC}",
            'unit_converter_title': f"{Colors.BOLD}Конвертер единиц:{Colors.ENDC}",
            'unit_converter_menu': "1. Длина (м, км, миля, фут)\n2. Вес (кг, г, фунт, унция)\n3. Температура (C, F, K)\n4. Скорость (км/ч, миль/ч, м/с)\n> ",
            'unit_converter_from': f"{Colors.CYAN}Из:{Colors.ENDC} ",
            'unit_converter_to': f"{Colors.CYAN}В:{Colors.ENDC} ",
            'unit_converter_value': f"{Colors.CYAN}Значение:{Colors.ENDC} ",
            'unit_converter_result': "{} {} = {} {}",
            'unit_converter_error': f"{Colors.FAIL}Неверная конвертация{Colors.ENDC}",
        }
        
        return {'en': en, 'ru': ru}
    
    def get(self, key: str, *args) -> str:
        """Получить переведенную строку"""
        text = self.translations.get(self.lang, self.translations['en']).get(key, key)
        try:
            return text.format(*args)
        except:
            return text



class SecurityScanner:
    """Сканер безопасности для URL"""
    
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.malicious_patterns: List[str] = []
        self.suspicious_patterns = [
            r'bit\.ly',
            r'tinyurl\.com',
            r'goo\.gl',
            r'free-',
            r'bonus',
            r'prize',
            r'winner',
            r'confirm',
            r'secure-',
            r'login\.',
            r'signin\.',
            r'account\.',
            r'update\.',
            r'verify\.'
        ]
        
    def load_database(self) -> Tuple[bool, str]:
        """Загрузка базы опасных URL"""
        try:
            response = requests.get(self.db_url, timeout=Config.REQUEST_TIMEOUT)
            response.raise_for_status()
            self.malicious_patterns = [
                line.strip().lower() 
                for line in response.text.splitlines() 
                if line.strip() and not line.startswith('#')
            ]
            return True, f"Loaded {len(self.malicious_patterns)} patterns"
        except Exception as e:
            return False, str(e)
    
    def check_url(self, url: str) -> Tuple[SecurityLevel, str]:
        """Проверка URL на безопасность"""
        try:
            
            if not re.match(r'^https?://', url.lower()):
                url = 'http://' + url
                
            parsed = urllib.parse.urlparse(url)
            domain = parsed.netloc.lower()
            full_url = url.lower()
            
            
            for pattern in self.malicious_patterns:
                if pattern in domain or pattern in full_url:
                    return SecurityLevel.MALICIOUS, pattern
            
            
            for pattern in self.suspicious_patterns:
                if re.search(pattern, domain, re.IGNORECASE):
                    return SecurityLevel.SUSPICIOUS, pattern
            
            
            if re.match(r'^\d+\.\d+\.\d+\.\d+$', domain):
                return SecurityLevel.SUSPICIOUS, "IP address instead of domain"
            
            return SecurityLevel.SAFE, ""
            
        except Exception as e:
            return SecurityLevel.UNKNOWN, str(e)



class ConsoleOS:
    def __init__(self):
        self.current_user = os.getenv('USER', os.getenv('USERNAME', 'guest'))
        self.current_dir = Path.cwd()
        self.running = True
        self.command_history: List[str] = []
        self.commands: Dict[str, Callable] = {}
        self.notes: List[Note] = []
        self.next_note_id = 1
        
        
        self.locale = self._select_language()
        self.security = SecurityScanner(Config.MALICIOUS_DB_URL)
        
        
        self._register_commands()
        
        
        self._initialize_database()
        
        
        self._load_notes()

    def _select_language(self) -> TranslationManager:
        """Выбор языка при запуске"""
        self._clear_screen()
        print(TranslationManager('en').get('welcome', Config.VERSION))
        print()
        
        try:
            choice = input(TranslationManager('en').get('language_choice')).strip()
            if choice == '2':
                lang = 'ru'
            else:
                lang = 'en'
        except:
            lang = 'en'
            
        return TranslationManager(lang)

    def _initialize_database(self):
        """Инициализация базы данных"""
        success, message = self.security.load_database()
        if success:
            print(self.locale.get('malicious_db_loaded', len(self.security.malicious_patterns)))
        else:
            print(self.locale.get('malicious_db_error', message))
        time.sleep(1)

    def _clear_screen(self):
        """Очистка экрана"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def _load_notes(self):
        """Загрузка заметок из файла"""
        notes_file = Path(Config.NOTES_FILE)
        if notes_file.exists():
            try:
                with open(notes_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for note_data in data:
                        note = Note(
                            id=note_data['id'],
                            title=note_data['title'],
                            content=note_data['content'],
                            created=datetime.fromisoformat(note_data['created']),
                            updated=datetime.fromisoformat(note_data['updated'])
                        )
                        self.notes.append(note)
                        if note.id >= self.next_note_id:
                            self.next_note_id = note.id + 1
            except:
                pass
                
    def _save_notes(self):
        """Сохранение заметок в файл"""
        try:
            data = []
            for note in self.notes:
                data.append({
                    'id': note.id,
                    'title': note.title,
                    'content': note.content,
                    'created': note.created.isoformat(),
                    'updated': note.updated.isoformat()
                })
            with open(Config.NOTES_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except:
            pass

    def _register_commands(self):
        """Регистрация всех команд"""
        
        def help_cmd(*args):
            """Показать справку"""
            if args and args[0] in self.commands:
                cmd = args[0]
                print(f"{cmd}: {self.commands[cmd].__doc__ or 'No description'}")
            else:
                print(self.locale.get('help_title'))
                
                all_commands = sorted(set([k for k in self.commands.keys() if k not in ['?', 'quit', 'cls', 'dir', 'del', 'checkurl']]))
                for cmd in all_commands:
                    doc = self.commands[cmd].__doc__ or 'No description'
                    print(self.locale.get('help_format', cmd, doc))

        
        
        def exit_cmd(*args):
            """Выход из системы"""
            print(self.locale.get('exit_msg'))
            time.sleep(1)
            self.running = False

        def clear_cmd(*args):
            """Очистить экран"""
            self._clear_screen()

        def time_cmd(*args):
            """Показать текущее время"""
            print(self.locale.get('current_time', datetime.now().strftime("%H:%M:%S")))

        def date_cmd(*args):
            """Показать текущую дату"""
            print(self.locale.get('current_date', datetime.now().strftime("%d.%m.%Y")))

        def whoami_cmd(*args):
            """Показать текущего пользователя"""
            print(self.locale.get('current_user', self.current_user))

        def pwd_cmd(*args):
            """Показать текущую директорию"""
            print(self.locale.get('current_dir', str(self.current_dir)))

        def ls_cmd(*args):
            """Список файлов в директории"""
            try:
                path = self.current_dir
                if args and args[0]:
                    path = Path(args[0])
                    if not path.is_absolute():
                        path = self.current_dir / path
                
                if not path.exists():
                    print(self.locale.get('dir_not_found', str(path)))
                    return
                
                if not path.is_dir():
                    print(f"{str(path)} is not a directory")
                    return
                
                items = []
                for item in path.iterdir():
                    items.append({
                        'name': item.name,
                        'is_dir': item.is_dir(),
                        'size': item.stat().st_size if item.is_file() else 0
                    })
                
                
                items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
                
                print(self.locale.get('dir_content', str(path)))
                for item in items:
                    if item['is_dir']:
                        print(f"  {Colors.BLUE}{item['name']}/{Colors.ENDC}")
                    else:
                        size = item['size']
                        if size < 1024:
                            size_str = f" ({size} B)"
                        elif size < 1024*1024:
                            size_str = f" ({size/1024:.1f} KB)"
                        else:
                            size_str = f" ({size/1024/1024:.1f} MB)"
                        print(f"  {Colors.GREEN}{item['name']}{Colors.ENDC}{size_str}")
                        
            except PermissionError:
                print(self.locale.get('permission_denied', str(path)))
            except Exception as e:
                print(f"Error: {e}")

        def cd_cmd(*args):
            """Сменить директорию"""
            if not args:
                
                target = Path.home()
            else:
                target = Path(args[0])
                if not target.is_absolute():
                    target = self.current_dir / target
                
            try:
                target = target.resolve()
                if target.exists() and target.is_dir():
                    self.current_dir = target
                else:
                    print(self.locale.get('dir_not_found', str(target)))
            except Exception as e:
                print(f"Error: {e}")

        def mkdir_cmd(*args):
            """Создать директорию"""
            if not args:
                print(self.locale.get('no_dir_name'))
                return
                
            new_dir = self.current_dir / args[0]
            try:
                new_dir.mkdir(parents=True, exist_ok=True)
                print(self.locale.get('dir_created', str(new_dir)))
            except Exception as e:
                print(f"Error: {e}")

        def touch_cmd(*args):
            """Создать файл"""
            if not args:
                print(self.locale.get('no_file_name'))
                return
                
            new_file = self.current_dir / args[0]
            try:
                new_file.touch(exist_ok=True)
                print(self.locale.get('file_created', str(new_file)))
            except Exception as e:
                print(f"Error: {e}")

        def rm_cmd(*args):
            """Удалить файл или директорию (используйте -r для директорий)"""
            if not args:
                print("Usage: rm <file/directory> [-r]")
                return
                
            target = self.current_dir / args[0]
            recursive = '-r' in args or '--recursive' in args
            
            try:
                if target.is_file():
                    target.unlink()
                    print(self.locale.get('file_deleted', str(target)))
                elif target.is_dir() and recursive:
                    import shutil
                    shutil.rmtree(target)
                    print(self.locale.get('dir_deleted', str(target)))
                elif target.is_dir():
                    print("Use -r to remove directories")
                else:
                    print(self.locale.get('file_not_found', str(target)))
            except Exception as e:
                print(f"Error: {e}")

        def echo_cmd(*args):
            """Вывести текст"""
            if args:
                print(' '.join(args))
            else:
                print()

        def cat_cmd(*args):
            """Показать содержимое файла"""
            if not args:
                print("Usage: cat <file>")
                return
                
            target = self.current_dir / args[0]
            try:
                if target.exists() and target.is_file():
                    with open(target, 'r', encoding='utf-8') as f:
                        print(f.read())
                else:
                    print(self.locale.get('file_not_found', str(target)))
            except UnicodeDecodeError:
                print("Binary file")
            except Exception as e:
                print(f"Error: {e}")

        def calc_cmd(*args):
            """Запустить калькулятор"""
            print(self.locale.get('calc_title'))
            while True:
                try:
                    expr = input(self.locale.get('calc_prompt'))
                    if expr.lower() in ['exit', 'quit', 'q']:
                        break
                    
                    
                    allowed = {'abs': abs, 'round': round, 'min': min, 'max': max}
                    allowed.update({k: v for k, v in math.__dict__.items() if not k.startswith('_')})
                    
                    result = eval(expr, {"__builtins__": {}}, allowed)
                    print(self.locale.get('calc_result', result))
                except Exception as e:
                    print(self.locale.get('calc_error', str(e)))

        def game_cmd(*args):
            """Игра 'угадай число'"""
            number = random.randint(1, 10)
            attempts = 3
            
            print(self.locale.get('game_title'))
            for attempt in range(1, attempts + 1):
                try:
                    guess = input(self.locale.get('game_prompt', attempt))
                    guess = int(guess)
                    
                    if guess == number:
                        print(self.locale.get('game_win'))
                        return
                    print("Too small!" if guess < number else "Too big!")
                except ValueError:
                    print(self.locale.get('game_invalid'))
                    
            print(self.locale.get('game_loss', number))

        def history_cmd(*args):
            """Показать историю команд"""
            if not self.command_history:
                print(self.locale.get('no_history'))
                return
                
            print(self.locale.get('command_history'))
            for i, cmd in enumerate(self.command_history[-20:], 1):
                print(f"  {i:3d}  {cmd}")

        def sysinfo_cmd(*args):
            """Показать информацию о системе"""
            print(self.locale.get('system_info',
                platform.system(),
                platform.python_version(),
                datetime.now().strftime("%H:%M:%S"),
                str(self.current_dir)
            ))

        def checkinternet_cmd(*args):
            """Проверить интернет-соединение"""
            test_urls = [
                "https://www.google.com",
                "https://www.cloudflare.com",
                "https://1.1.1.1"
            ]
            
            for url in test_urls:
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        print(self.locale.get('internet_connected'))
                        return True
                except:
                    continue
                    
            print(self.locale.get('internet_failed', "All tests failed"))
            return False

        def urlcheck_cmd(*args):
            """Проверить безопасность URL"""
            if not self.security.malicious_patterns:
                print("Database not loaded. Run 'update_db' to reload")
                return
                
            url = args[0].strip() if args else input(self.locale.get('enter_url')).strip()
            if not url:
                return
                
            level, reason = self.security.check_url(url)
            
            if level == SecurityLevel.SAFE:
                print(self.locale.get('safe_url', url))
            elif level == SecurityLevel.SUSPICIOUS:
                print(self.locale.get('suspicious_url', f"{url} ({reason})"))
            elif level == SecurityLevel.MALICIOUS:
                print(self.locale.get('malicious_url', f"{url} (matched: {reason})"))
            else:
                print(self.locale.get('url_not_recognized', url))

        def update_cmd(*args):
            """Проверить обновления"""
            print("\n" + self.locale.get('checking_update'))
            
            try:
                response = requests.get(Config.VERSION_URL, timeout=5)
                response.raise_for_status()
                latest_version = response.text.strip()
                
                if latest_version != Config.VERSION:
                    print("\n" + "─" * 40)
                    print(self.locale.get('update_available', Config.VERSION, latest_version))
                    choice = input(self.locale.get('update_menu')).strip()
                    
                    if choice == '1':
                        print("\n" + self.locale.get('update_downloading'))
                        webbrowser.open(Config.DOWNLOAD_URL)
                        time.sleep(2)
                    else:
                        print("\n" + self.locale.get('update_skipped'))
                        time.sleep(1)
                else:
                    print("\n" + self.locale.get('update_latest', Config.VERSION))
                    time.sleep(1)
                    
            except Exception as e:
                print("\n" + self.locale.get('update_error', str(e)))
                time.sleep(2)

        def update_db_cmd(*args):
            """Обновить базу опасных URL"""
            print("Updating malicious URL database...")
            success, message = self.security.load_database()
            if success:
                print(self.locale.get('malicious_db_loaded', len(self.security.malicious_patterns)))
            else:
                print(self.locale.get('malicious_db_error', message))

        

        def hash_cmd(*args):
            """Вычислить хеш текста или файла"""
            print(self.locale.get('hash_title'))
            
            if args and args[0] == '-f':
                
                file_path = input(self.locale.get('hash_file_prompt')).strip()
                if not file_path:
                    return
                    
                path = Path(file_path)
                if not path.exists():
                    print(self.locale.get('hash_file_not_found', file_path))
                    return
                    
                try:
                    with open(path, 'rb') as f:
                        data = f.read()
                        md5 = hashlib.md5(data).hexdigest()
                        sha256 = hashlib.sha256(data).hexdigest()
                        print(self.locale.get('hash_file_result', file_path, md5, sha256))
                except Exception as e:
                    print(f"Error: {e}")
            else:
                
                text = input(self.locale.get('hash_prompt')).strip()
                if text:
                    data = text.encode()
                    md5 = hashlib.md5(data).hexdigest()
                    sha1 = hashlib.sha1(data).hexdigest()
                    sha256 = hashlib.sha256(data).hexdigest()
                    print(self.locale.get('hash_result', md5, sha1, sha256))

        def timer_cmd(*args):
            """Таймер обратного отсчета"""
            print(self.locale.get('timer_title'))
            
            time_str = input(self.locale.get('timer_prompt')).strip()
            if not time_str:
                return
                
            
            seconds = 0
            if ':' in time_str:
                parts = time_str.split(':')
                if len(parts) == 2:
                    minutes, secs = map(int, parts)
                    seconds = minutes * 60 + secs
            else:
                try:
                    seconds = int(time_str)
                except:
                    print("Invalid time format")
                    return
                    
            if seconds <= 0:
                print("Invalid time")
                return
                
            print(self.locale.get('timer_started', self._format_time(seconds)))
            
            try:
                for i in range(seconds, 0, -1):
                    print(f"\r{self._format_time(i)} ", end='', flush=True)
                    time.sleep(1)
                print()
                print(self.locale.get('timer_done'))
            except KeyboardInterrupt:
                print()
                print(self.locale.get('timer_cancelled'))

        def stopwatch_cmd(*args):
            """Секундомер"""
            print(self.locale.get('stopwatch_title'))
            print(self.locale.get('stopwatch_controls'))
            
            running = False
            start_time = None
            elapsed = 0
            
            while True:
                cmd = input("> ").strip().lower()
                
                if cmd == 's':  
                    if not running:
                        start_time = time.time() - elapsed
                        running = True
                        print("Started")
                elif cmd == 'p' or cmd == 'u':  
                    if running:
                        elapsed = time.time() - start_time
                        running = False
                        print(f"Paused: {self._format_time(elapsed)}")
                elif cmd == 'r':  
                    elapsed = 0
                    if running:
                        start_time = time.time()
                    print("Reset")
                elif cmd == 'q':  
                    break
                elif cmd:  
                    current = time.time() - start_time if running else elapsed
                    print(self.locale.get('stopwatch_time', self._format_time(current)))

        def notes_cmd(*args):
            """Менеджер заметок"""
            print(self.locale.get('notes_title'))
            print(self.locale.get('notes_commands'))
            
            if not args:
                return
                
            subcmd = args[0].lower()
            
            if subcmd == 'list':
                if not self.notes:
                    print(self.locale.get('notes_empty'))
                else:
                    print(self.locale.get('notes_list'))
                    for note in sorted(self.notes, key=lambda x: x.updated, reverse=True):
                        preview = note.content[:50] + '...' if len(note.content) > 50 else note.content
                        print(f"  [{note.id}] {note.title} - {preview}")
                        
            elif subcmd == 'add' and len(args) > 1:
                title = ' '.join(args[1:])
                print(self.locale.get('notes_edit_instructions'))
                try:
                    lines = []
                    while True:
                        try:
                            line = input()
                            lines.append(line)
                        except EOFError:
                            break
                    content = '\n'.join(lines)
                    
                    note = Note(
                        id=self.next_note_id,
                        title=title,
                        content=content,
                        created=datetime.now(),
                        updated=datetime.now()
                    )
                    self.notes.append(note)
                    self.next_note_id += 1
                    self._save_notes()
                    print(self.locale.get('notes_added', note.id))
                except KeyboardInterrupt:
                    print("\nCancelled")
                    
            elif subcmd == 'view' and len(args) > 1:
                try:
                    note_id = int(args[1])
                    note = next((n for n in self.notes if n.id == note_id), None)
                    if note:
                        print(self.locale.get('notes_content',
                            '', note.title,
                            note.created.strftime("%Y-%m-%d %H:%M"),
                            note.updated.strftime("%Y-%m-%d %H:%M"),
                            note.content))
                    else:
                        print(self.locale.get('notes_not_found'))
                except ValueError:
                    print("Invalid ID")
                    
            elif subcmd == 'edit' and len(args) > 1:
                try:
                    note_id = int(args[1])
                    note = next((n for n in self.notes if n.id == note_id), None)
                    if note:
                        print(self.locale.get('notes_edit_instructions'))
                        print(f"Current content:\n{note.content}\n")
                        try:
                            lines = []
                            while True:
                                try:
                                    line = input()
                                    lines.append(line)
                                except EOFError:
                                    break
                            note.content = '\n'.join(lines)
                            note.updated = datetime.now()
                            self._save_notes()
                            print(self.locale.get('notes_added', note.id))
                        except KeyboardInterrupt:
                            print("\nCancelled")
                    else:
                        print(self.locale.get('notes_not_found'))
                except ValueError:
                    print("Invalid ID")
                    
            elif subcmd == 'delete' and len(args) > 1:
                try:
                    note_id = int(args[1])
                    note = next((n for n in self.notes if n.id == note_id), None)
                    if note:
                        self.notes.remove(note)
                        self._save_notes()
                        print(self.locale.get('notes_deleted'))
                    else:
                        print(self.locale.get('notes_not_found'))
                except ValueError:
                    print("Invalid ID")
                    
            elif subcmd == 'search' and len(args) > 1:
                query = ' '.join(args[1:]).lower()
                print(self.locale.get('notes_search_results', query))
                found = False
                for note in self.notes:
                    if query in note.title.lower() or query in note.content.lower():
                        preview = note.content[:50] + '...' if len(note.content) > 50 else note.content
                        print(f"  [{note.id}] {note.title} - {preview}")
                        found = True
                if not found:
                    print("No matches found")

        def portscan_cmd(*args):
            """Сканирование открытых портов"""
            print(self.locale.get('port_scan_title'))
            
            host = input(self.locale.get('port_scan_prompt')).strip()
            if not host:
                host = 'localhost'
                
            range_str = input(self.locale.get('port_scan_range')).strip()
            if not range_str:
                range_str = '1-1024'
                
            try:
                if '-' in range_str:
                    start, end = map(int, range_str.split('-'))
                else:
                    start = end = int(range_str)
                    
                if start < 1 or end > 65535 or start > end:
                    print("Invalid port range")
                    return
                    
                print(self.locale.get('port_scanning', host))
                open_ports = []
                
                for port in range(start, end + 1):
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((host, port))
                    if result == 0:
                        print(self.locale.get('port_open', port))
                        open_ports.append(port)
                    sock.close()
                    
                print(self.locale.get('port_scan_done', len(open_ports)))
                
            except Exception as e:
                print(self.locale.get('port_error', host, range_str, str(e)))

        def password_cmd(*args):
            """Генератор паролей"""
            print(self.locale.get('password_title'))
            
            try:
                length = int(input(self.locale.get('password_prompt')).strip() or '12')
                if length < 8 or length > 64:
                    print("Length must be between 8 and 64")
                    return
                    
                print(self.locale.get('password_options'))
                choice = input().strip()
                
                chars = ''
                if choice == '1' or choice == '5':
                    chars += 'abcdefghijklmnopqrstuvwxyz'
                if choice == '2' or choice == '5':
                    chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                if choice == '3' or choice == '5':
                    chars += '0123456789'
                if choice == '4' or choice == '5':
                    chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
                    
                if not chars:
                    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                    
                password = ''.join(random.choice(chars) for _ in range(length))
                
                
                strength = 0
                if re.search(r'[a-z]', password):
                    strength += 1
                if re.search(r'[A-Z]', password):
                    strength += 1
                if re.search(r'[0-9]', password):
                    strength += 1
                if re.search(r'[^a-zA-Z0-9]', password):
                    strength += 1
                    
                strength_levels = ['Very Weak', 'Weak', 'Medium', 'Strong', 'Very Strong']
                
                print(self.locale.get('password_result', password))
                print(self.locale.get('password_strength', strength_levels[strength]))
                
            except Exception as e:
                print(f"Error: {e}")

        def translate_cmd(*args):
            """Простой переводчик (использует mymemory API)"""
            print(self.locale.get('translate_title'))
            
            text = input(self.locale.get('translate_prompt')).strip()
            if not text:
                return
                
            from_lang = input(self.locale.get('translate_from')).strip() or 'en'
            to_lang = input(self.locale.get('translate_to')).strip() or 'ru'
            
            try:
                url = f"https://api.mymemory.translated.net/get"
                params = {
                    'q': text,
                    'langpair': f"{from_lang}|{to_lang}"
                }
                
                response = requests.get(url, params=params, timeout=10)
                data = response.json()
                
                if response.status_code == 200 and 'responseData' in data:
                    translation = data['responseData']['translatedText']
                    print(self.locale.get('translate_result', translation))
                else:
                    print(self.locale.get('translate_error', "API error"))
                    
            except Exception as e:
                print(self.locale.get('translate_error', str(e)))

        def qr_cmd(*args):
            """Генерация QR-кода (требуется qrencode)"""
            print(self.locale.get('qr_title'))
            
            text = input(self.locale.get('qr_prompt')).strip()
            if not text:
                return
                
            filename = f"qr_{int(time.time())}.png"
            
            try:
                
                result = subprocess.run(['which', 'qrencode'], capture_output=True)
                if result.returncode != 0:
                    print(self.locale.get('qr_not_installed'))
                    return
                    
                
                cmd = ['qrencode', '-o', filename, text]
                result = subprocess.run(cmd, capture_output=True)
                
                if result.returncode == 0:
                    print(self.locale.get('qr_saved', filename))
                else:
                    print(self.locale.get('qr_error', result.stderr.decode()))
                    
            except Exception as e:
                print(self.locale.get('qr_error', str(e)))

        def reminder_cmd(*args):
            """Установить напоминание"""
            print(self.locale.get('reminder_title'))
            
            message = input(self.locale.get('reminder_prompt')).strip()
            if not message:
                return
                
            try:
                seconds = int(input(self.locale.get('reminder_time')).strip())
                if seconds <= 0:
                    print("Invalid time")
                    return
                    
                print(self.locale.get('reminder_set', seconds))
                
                
                def reminder_thread():
                    time.sleep(seconds)
                    print(f"\n{self.locale.get('reminder_alert', '', message)}")
                    
                import threading
                thread = threading.Thread(target=reminder_thread, daemon=True)
                thread.start()
                
            except ValueError:
                print("Invalid time")
            except Exception as e:
                print(f"Error: {e}")

        def convert_cmd(*args):
            """Конвертер единиц измерения"""
            print(self.locale.get('unit_converter_title'))
            
            print(self.locale.get('unit_converter_menu'))
            choice = input().strip()
            
            
            units = {
                '1': {  
                    'm': 1,
                    'km': 0.001,
                    'mile': 0.000621371,
                    'ft': 3.28084
                },
                '2': {  
                    'kg': 1,
                    'g': 1000,
                    'lb': 2.20462,
                    'oz': 35.274
                },
                '3': {  
                    'c': 'celsius',
                    'f': 'fahrenheit',
                    'k': 'kelvin'
                },
                '4': {  
                    'km/h': 1,
                    'mph': 0.621371,
                    'm/s': 0.277778
                }
            }
            
            if choice not in units:
                print(self.locale.get('unit_converter_error'))
                return
                
            unit_set = units[choice]
            
            from_unit = input(self.locale.get('unit_converter_from')).strip().lower()
            to_unit = input(self.locale.get('unit_converter_to')).strip().lower()
            
            if from_unit not in unit_set or to_unit not in unit_set:
                print(self.locale.get('unit_converter_error'))
                return
                
            try:
                value = float(input(self.locale.get('unit_converter_value')).strip())
                
                if choice == '3':  
                    
                    if from_unit == 'c':
                        if to_unit == 'f':
                            result = value * 9/5 + 32
                        elif to_unit == 'k':
                            result = value + 273.15
                        else:
                            result = value
                    elif from_unit == 'f':
                        if to_unit == 'c':
                            result = (value - 32) * 5/9
                        elif to_unit == 'k':
                            result = (value - 32) * 5/9 + 273.15
                        else:
                            result = value
                    elif from_unit == 'k':
                        if to_unit == 'c':
                            result = value - 273.15
                        elif to_unit == 'f':
                            result = (value - 273.15) * 9/5 + 32
                        else:
                            result = value
                else:
                    
                    result = value / unit_set[from_unit] * unit_set[to_unit]
                    
                print(self.locale.get('unit_converter_result', value, from_unit, result, to_unit))
                
            except ValueError:
                print(self.locale.get('unit_converter_error'))

        
        self.commands = {
            
            'help': help_cmd,
            '?': help_cmd,
            'exit': exit_cmd,
            'quit': exit_cmd,
            'clear': clear_cmd,
            'cls': clear_cmd,
            'time': time_cmd,
            'date': date_cmd,
            'whoami': whoami_cmd,
            'pwd': pwd_cmd,
            'ls': ls_cmd,
            'dir': ls_cmd,
            'cd': cd_cmd,
            'mkdir': mkdir_cmd,
            'touch': touch_cmd,
            'rm': rm_cmd,
            'del': rm_cmd,
            'echo': echo_cmd,
            'cat': cat_cmd,
            'calc': calc_cmd,
            'game': game_cmd,
            'history': history_cmd,
            'sysinfo': sysinfo_cmd,
            'checkinternet': checkinternet_cmd,
            'urlcheck': urlcheck_cmd,
            'checkurl': urlcheck_cmd,
            'update': update_cmd,
            'update_db': update_db_cmd,
            
            
            'hash': hash_cmd,
            'timer': timer_cmd,
            'stopwatch': stopwatch_cmd,
            'notes': notes_cmd,
            'portscan': portscan_cmd,
            'password': password_cmd,
            'translate': translate_cmd,
            'qr': qr_cmd,
            'reminder': reminder_cmd,
            'convert': convert_cmd
        }
        
    def _format_time(self, seconds: int) -> str:
        """Форматирование времени"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"

    def show_banner(self):
        """Показать приветственный баннер"""
        print(self.locale.get('welcome', Config.VERSION))
        print(self.locale.get('current_user', self.current_user))
        print(self.locale.get('current_dir', str(self.current_dir)))
        print()
        print("Type 'help' for available commands")

    def run(self):
        """Основной цикл системы"""
        self._clear_screen()
        
        
        if 'update' in self.commands:
            self.commands['update']()
            self._clear_screen()
        
        self.show_banner()
        
        while self.running:
            try:
                
                hostname = os.uname().nodename if hasattr(os, 'uname') else 'localhost'
                dir_name = self.current_dir.name if self.current_dir.name else '/'
                
                prompt = f"{Colors.GREEN}{self.current_user}@{hostname}{Colors.ENDC}:{Colors.BLUE}{dir_name}{Colors.ENDC}{Colors.GREEN}$ {Colors.ENDC}"
                
                
                command_line = input(prompt).strip()
                
                if not command_line:
                    continue
                    
                
                self.command_history.append(command_line)
                if len(self.command_history) > Config.MAX_COMMAND_HISTORY:
                    self.command_history.pop(0)
                
                
                parts = command_line.split()
                cmd_name = parts[0].lower()
                cmd_args = parts[1:]
                
                
                if cmd_name in self.commands:
                    try:
                        self.commands[cmd_name](*cmd_args)
                    except Exception as e:
                        print(f"Command execution error: {e}")
                else:
                    print(self.locale.get('unknown_cmd', cmd_name))
                    
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except EOFError:
                print("\n" + self.locale.get('exit_msg'))
                self.running = False
            except Exception as e:
                print(f"System error: {e}")



if __name__ == "__main__":
    try:
        os_system = ConsoleOS()
        os_system.run()
    except KeyboardInterrupt:
        print("\nSystem terminated by user")
    except Exception as e:
        print(f"Fatal system error: {str(e)}")
        sys.exit(1)
