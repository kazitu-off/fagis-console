import os
import sys
import time
import webbrowser
import requests
import re
from datetime import datetime

class Localization:
    def __init__(self, lang='en'):
        self.lang = lang
        self.translations = self.load_translations()
        
    def load_translations(self):
        base_translations = {
            'welcome': "┌─────────────────────────────────────────────┐\n│           FAGIS Console OS v{}           │\n└─────────────────────────────────────────────┘",
            'language_choice': "Select language:\n1. English\n2. Русский\n> ",
            'invalid_choice': "Invalid choice. Defaulting to English.",
            'prompt': "{}@{}> ",
            'current_time': "Current time: {}",
            'current_date': "Today's date: {}",
            'current_user': "Current user: {}",
            'dir_content': "Contents of {}:",
            'dir_not_found': "Directory not found: {}",
            'file_created': "File created: {}",
            'dir_created': "Directory created: {}",
            'unknown_cmd': "Command not found: {}. Type 'help' for available commands.",
            'exit_msg': "Shutting down system...",
            'help_title': "Available commands:",
            'help_help': "help [command] - display help information",
            'help_exit': "exit - terminate the system",
            'help_clear': "clear - clear the screen",
            'help_time': "time - show current time",
            'help_date': "date - show current date",
            'help_whoami': "whoami - display current user",
            'help_ls': "ls - list directory contents",
            'help_cd': "cd [directory] - change directory",
            'help_mkdir': "mkdir <directory> - create new directory",
            'help_touch': "touch <filename> - create new file",
            'help_echo': "echo <text> - display text",
            'help_calc': "calc - start calculator",
            'help_game': "game - play number guessing game",
            'calc_title': "Calculator (type 'exit' to quit)",
            'calc_prompt': "Enter expression> ",
            'calc_result': "Result: {}",
            'calc_error': "Calculation error: {}",
            'game_title': "Guess the number (1-10)!",
            'game_prompt': "Attempt {}/3: ",
            'game_win': "Congratulations! You guessed correctly!",
            'game_loss': "Game over! The number was: {}",
            'game_invalid': "Please enter a valid number!",
            'no_file_name': "Error: Please specify a file name",
            'no_dir_name': "Error: Please specify a directory name",
            'no_text': "Error: Please specify text to display",
            'update_available': "UPDATE AVAILABLE!\nCurrent version: {}\nLatest version: {}",
            'update_menu': "\nOptions:\n1. Download update\n2. Skip\n> ",
            'update_downloading': "Opening download page in browser...",
            'update_skipped': "Update check skipped.",
            'update_error': "Failed to check updates: {}",
            'update_latest': "You have the latest version ({})",
            'checking_update': "Checking for updates...",
            'check_url_title': "Link Security Check",
            'safe_url': "The link appears safe: {}",
            'malicious_url': "DANGER! Malicious link detected: {}",
            'url_not_recognized': "Link not recognized: {}",
            'check_error': "Security check error: {}",
            'malicious_db_error': "Failed to load malicious URLs database: {}",
            'enter_url': "Enter URL to check> ",
            'url_detected': "Security warning: Potential malicious URL detected - {}",
            'checking_urls': "Scanning for malicious links...",
            'clean_content': "Content appears clean. No malicious links detected.",
            'internet_connected': "Internet connection: Active",
            'internet_failed': "Internet connection: Failed (Error: {})",
            'help_urlcheck': "urlcheck <url> - check URL safety",
            'help_internet': "checkinternet - test internet connection",
            'malicious_db_loaded': "Loaded {} malicious URL patterns",
            'malicious_db_empty': "Warning: Malicious URL database is empty"
        }
        
        ru_translations = base_translations.copy()
        ru_translations.update({
            'language_choice': "Выберите язык:\n1. English\n2. Русский\n> ",
            'invalid_choice': "Некорректный выбор. Используется русский.",
            'current_time': "Текущее время: {}",
            'current_date': "Сегодняшняя дата: {}",
            'current_user': "Текущий пользователь: {}",
            'dir_content': "Содержимое {}:",
            'dir_not_found': "Каталог не найден: {}",
            'file_created': "Файл создан: {}",
            'dir_created': "Каталог создан: {}",
            'unknown_cmd': "Команда не найдена: {}. Введите 'help' для списка команд.",
            'exit_msg': "Завершение работы системы...",
            'help_title': "Доступные команды:",
            'help_help': "help [команда] - показать справку",
            'help_exit': "exit - завершить работу",
            'help_clear': "clear - очистить экран",
            'help_time': "time - показать текущее время",
            'help_date': "date - показать текущую дату",
            'help_whoami': "whoami - показать текущего пользователя",
            'help_ls': "ls - список файлов в каталоге",
            'help_cd': "cd [каталог] - сменить каталог",
            'help_mkdir': "mkdir <каталог> - создать каталог",
            'help_touch': "touch <файл> - создать файл",
            'help_echo': "echo <текст> - вывести текст",
            'help_calc': "calc - запустить калькулятор",
            'help_game': "game - игра 'угадай число'",
            'calc_title': "Калькулятор (введите 'exit' для выхода)",
            'calc_prompt': "Введите выражение> ",
            'calc_result': "Результат: {}",
            'calc_error': "Ошибка вычисления: {}",
            'game_title': "Угадайте число от 1 до 10!",
            'game_prompt': "Попытка {}/3: ",
            'game_win': "Поздравляем! Вы угадали!",
            'game_loss': "Игра окончена! Загаданное число: {}",
            'game_invalid': "Пожалуйста, введите число!",
            'no_file_name': "Ошибка: Укажите имя файла",
            'no_dir_name': "Ошибка: Укажите имя каталога",
            'no_text': "Ошибка: Укажите текст для вывода",
            'update_available': "ДОСТУПНО ОБНОВЛЕНИЕ!\nТекущая версия: {}\nНовая версия: {}",
            'update_menu': "\nВарианты:\n1. Скачать обновление\n2. Пропустить\n> ",
            'update_downloading': "Открываю страницу загрузки в браузере...",
            'update_skipped': "Проверка обновлений пропущена.",
            'update_error': "Ошибка проверки обновлений: {}",
            'update_latest': "У вас последняя версия ({})",
            'checking_update': "Проверка обновлений...",
            'check_url_title': "Проверка безопасности ссылок",
            'safe_url': "Ссылка безопасна: {}",
            'malicious_url': "ОПАСНО! Обнаружена вредоносная ссылка: {}",
            'url_not_recognized': "Ссылка не распознана: {}",
            'check_error': "Ошибка проверки: {}",
            'malicious_db_error': "Ошибка загрузки базы опасных ссылок: {}",
            'enter_url': "Введите URL для проверки> ",
            'url_detected': "Предупреждение безопасности: Обнаружена потенциально опасная ссылка - {}",
            'checking_urls': "Поиск опасных ссылок...",
            'clean_content': "Вредоносные ссылки не обнаружены.",
            'internet_connected': "Интернет-соединение: Активно",
            'internet_failed': "Интернет-соединение: Недоступно (Ошибка: {})",
            'help_urlcheck': "urlcheck <url> - проверить безопасность ссылки",
            'help_internet': "checkinternet - проверить интернет-соединение",
            'malicious_db_loaded': "Загружено {} шаблонов опасных URL",
            'malicious_db_empty': "Предупреждение: База опасных URL пуста"
        })
        
        return {'en': base_translations, 'ru': ru_translations}.get(self.lang, base_translations)
        
    def get(self, key, *args):
        translation = self.translations.get(key, key)
        try:
            return translation.format(*args)
        except:
            return translation

class ConsoleOS:
    def __init__(self):
        self.current_user = "guest"
        self.current_dir = os.getcwd()
        self.running = True
        self.version = "1.1"
        self.version_url = "https://raw.githubusercontent.com/kubydog101/fagis-console/refs/heads/main/ver.txt"
        self.download_url = "https://github.com/kubydog101/fagis-console/releases/latest"
        self.malicious_urls = []
        
        # Ссылка на ваш TXT-файл с опасными URL
        self.malicious_db_url = "https://raw.githubusercontent.com/kubydog101/fagis-console/refs/heads/main/scam-db.txt"  # ЗАМЕНИТЕ НА ВАШУ ССЫЛКУ
        
        # Инициализация локализации
        try:
            self.locale = self.select_language()
        except Exception as e:
            print(f"Language error: {str(e)}. Using English.")
            self.locale = Localization('en')

        # Загрузка базы опасных URL
        self.load_malicious_urls()

    def load_malicious_urls(self):
        """Загрузка базы опасных URL из удаленного TXT-файла"""
        try:
            response = requests.get(self.malicious_db_url, timeout=10)
            response.raise_for_status()
            self.malicious_urls = [line.strip().lower() for line in response.text.splitlines() if line.strip()]
            
            if self.malicious_urls:
                print(self.locale.get('malicious_db_loaded', len(self.malicious_urls)))
            else:
                print(self.locale.get('malicious_db_empty'))
        except Exception as e:
            print(self.locale.get('malicious_db_error', str(e)))
            self.malicious_urls = []

    def select_language(self):
        self.clear_screen()
        print("┌─────────────────────────────────────────────┐")
        print("│            FAGIS Console OS v1.1            │")
        print("└─────────────────────────────────────────────┘")
        print("             Select language / Выберите язык\n")
        
        lang = 'en'
        try:
            choice = input("1. English\n2. Русский\n\n> ").strip()
            if choice == '2':
                lang = 'ru'
            elif choice != '1':
                print("\n" + Localization().get('invalid_choice'))
                time.sleep(1)
        except Exception as e:
            print(f"Input error: {str(e)}. Defaulting to English.")
        
        return Localization(lang)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def check_internet(self):
        """Проверка интернет-соединения"""
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
            except Exception as e:
                last_error = str(e)
        
        print(self.locale.get('internet_failed', last_error))
        return False

    def check_url_safety(self, *args):
        """Проверка безопасности URL"""
        if not self.malicious_urls:
            print("Database not loaded. Run 'update_db' to reload")
            return
            
        if not args:
            url = input(self.locale.get('enter_url')).strip()
        else:
            url = args[0].strip()
        
        if not url:
            return
            
        try:
            # Нормализация URL
            clean_url = url.lower()
            if not re.match(r'^https?://', clean_url):
                clean_url = 'http://' + clean_url
            
            # Извлечение домена
            domain_match = re.search(r'https?://([^/:]+)', clean_url)
            if not domain_match:
                print(self.locale.get('url_not_recognized', url))
                return
                
            domain = domain_match.group(1)
            
            # Проверка в базе опасных URL
            for malicious_pattern in self.malicious_urls:
                if malicious_pattern in domain:
                    print(self.locale.get('malicious_url', url))
                    return
                    
            print(self.locale.get('safe_url', url))
        except Exception as e:
            print(self.locale.get('check_error', str(e)))

    def check_updates(self):
        try:
            print("\n" + self.locale.get('checking_update'))
            timestamp = int(time.time())
            url = f"{self.version_url}?t={timestamp}"
            
            try:
                if not self.check_internet():
                    print("\n" + self.locale.get('update_error', "No internet connection"))
                    time.sleep(2)
                    return
                    
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                latest_version = response.text.strip()
                
                if latest_version != self.version:
                    print("\n" + "─" * 40)
                    print(self.locale.get('update_available', self.version, latest_version))
                    choice = input(self.locale.get('update_menu')).strip()
                    
                    if choice == '1':
                        print("\n" + self.locale.get('update_downloading'))
                        webbrowser.open(self.download_url)
                        time.sleep(2)
                    else:
                        print("\n" + self.locale.get('update_skipped'))
                        time.sleep(1)
                else:
                    print("\n" + self.locale.get('update_latest', self.version))
                    time.sleep(1)
                    
            except requests.exceptions.RequestException as e:
                print("\n" + self.locale.get('update_error', f"Connection error: {str(e)}"))
                time.sleep(2)
            except Exception as e:
                print("\n" + self.locale.get('update_error', str(e)))
                time.sleep(2)
                
        except Exception as e:
            print("\n" + f"Critical update error: {str(e)}")
            time.sleep(2)
        finally:
            self.clear_screen()

    def show_banner(self):
        print(self.locale.get('welcome', self.version))
        print(self.locale.get('current_user', self.current_user))
        print(f"Current directory: {self.current_dir}\n")
        print(self.locale.get('help_help'))

    def exit_system(self):
        print(self.locale.get('exit_msg'))
        time.sleep(1)
        self.running = False
        
    def show_time(self):
        print(self.locale.get('current_time', datetime.now().strftime("%H:%M:%S")))
        
    def show_date(self):
        print(self.locale.get('current_date', datetime.now().strftime("%d.%m.%Y")))
        
    def show_user(self):
        print(self.locale.get('current_user', self.current_user))
        
    def list_files(self):
        try:
            files = os.listdir(self.current_dir)
            print(self.locale.get('dir_content', self.current_dir))
            for item in files:
                prefix = "[DIR] " if os.path.isdir(os.path.join(self.current_dir, item)) else ""
                print(f"  {prefix}{item}")
        except Exception as e:
            print(f"Error: {str(e)}")
            
    def change_dir(self, *args):
        if not args:
            print(self.locale.get('help_cd'))
            return
            
        target = args[0]
        new_path = os.path.abspath(os.path.join(self.current_dir, target))
        
        if os.path.isdir(new_path):
            self.current_dir = new_path
        else:
            print(self.locale.get('dir_not_found', target))
    
    def make_dir(self, *args):
        if not args:
            print(self.locale.get('no_dir_name'))
            print(self.locale.get('help_mkdir'))
            return
            
        new_dir = os.path.join(self.current_dir, args[0])
        try:
            os.makedirs(new_dir, exist_ok=True)
            print(self.locale.get('dir_created', new_dir))
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def create_file(self, *args):
        if not args:
            print(self.locale.get('no_file_name'))
            print(self.locale.get('help_touch'))
            return
            
        new_file = os.path.join(self.current_dir, args[0])
        try:
            with open(new_file, 'w') as f:
                pass
            print(self.locale.get('file_created', new_file))
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def echo_text(self, *args):
        if not args:
            print(self.locale.get('no_text'))
            print(self.locale.get('help_echo'))
            return
            
        print(" ".join(args))
    
    def calculator(self):
        print(self.locale.get('calc_title'))
        while True:
            try:
                expr = input(self.locale.get('calc_prompt'))
                if expr.lower() == 'exit':
                    return
                result = eval(expr)
                print(self.locale.get('calc_result', result))
            except Exception as e:
                print(self.locale.get('calc_error', str(e)))
    
    def mini_game(self):
        import random
        number = random.randint(1, 10)
        attempts = 3
        
        print(self.locale.get('game_title'))
        while attempts > 0:
            try:
                guess = input(self.locale.get('game_prompt', 4 - attempts))
                guess = int(guess)
                if guess == number:
                    print(self.locale.get('game_win'))
                    return
                print("Too big!" if guess > number else "Too small!")
                attempts -= 1
            except ValueError:
                print(self.locale.get('game_invalid'))
        
        print(self.locale.get('game_loss', number))
    
    def update_database(self):
        """Обновление базы опасных URL"""
        print("Updating malicious URL database...")
        self.load_malicious_urls()

    def show_help(self, *args):
        help_texts = {
            'help': self.locale.get('help_help'),
            'exit': self.locale.get('help_exit'),
            'clear': self.locale.get('help_clear'),
            'time': self.locale.get('help_time'),
            'date': self.locale.get('help_date'),
            'whoami': self.locale.get('help_whoami'),
            'ls': self.locale.get('help_ls'),
            'cd': self.locale.get('help_cd'),
            'mkdir': self.locale.get('help_mkdir'),
            'touch': self.locale.get('help_touch'),
            'echo': self.locale.get('help_echo'),
            'calc': self.locale.get('help_calc'),
            'game': self.locale.get('help_game'),
            'checkinternet': self.locale.get('help_internet'),
            'urlcheck': self.locale.get('help_urlcheck'),
            'update_db': "update_db - reload malicious URLs database"
        }
        
        if args and args[0] in help_texts:
            cmd = args[0]
            print(f"{cmd}: {help_texts[cmd]}")
        else:
            print(self.locale.get('help_title'))
            for cmd in sorted(help_texts.keys()):
                print(f"  {cmd.ljust(12)} {help_texts[cmd]}")

    def run(self):
        self.clear_screen()
        try:
            self.check_updates()
        except Exception as e:
            print(f"Update initialization error: {str(e)}")
            time.sleep(2)
            
        self.show_banner()
        
        commands = {
            'help': self.show_help,
            'exit': self.exit_system,
            'clear': self.clear_screen,
            'time': self.show_time,
            'date': self.show_date,
            'whoami': self.show_user,
            'ls': self.list_files,
            'cd': self.change_dir,
            'mkdir': self.make_dir,
            'touch': self.create_file,
            'echo': self.echo_text,
            'calc': self.calculator,
            'game': self.mini_game,
            'checkinternet': self.check_internet,
            'urlcheck': self.check_url_safety,
            'update_db': self.update_database
        }
        
        while self.running:
            try:
                prompt = self.locale.get('prompt', self.current_user, os.path.basename(self.current_dir))
                command = input(prompt).strip().split()
                if not command:
                    continue
                    
                cmd = command[0].lower()
                args = command[1:]
                
                if cmd in commands:
                    commands[cmd](*args)
                else:
                    print(self.locale.get('unknown_cmd', cmd))
                    
            except KeyboardInterrupt:
                print("\n" + self.locale.get('help_exit'))
                self.exit_system()
            except Exception as e:
                print(f"System error: {str(e)}")

if __name__ == "__main__":
    try:
        os_system = ConsoleOS()
        os_system.run()
    except Exception as e:
        print(f"Fatal system error: {str(e)}")
        sys.exit(1)
