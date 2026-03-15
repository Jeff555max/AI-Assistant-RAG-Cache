"""
Главный скрипт запуска RAG-ассистента.

Позволяет выбрать режим работы:
1. Консольная версия (main.py)
2. Telegram бот (bot_main.py)
"""

import os
import sys
import subprocess
from dotenv import load_dotenv


def clear_screen():
    """Очищает экран консоли."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Выводит заголовок программы."""
    print("=" * 70)
    print("🤖 RAG-АССИСТЕНТ С CHROMADB И КЕШИРОВАНИЕМ")
    print("=" * 70)
    print()


def print_menu():
    """Выводит меню выбора режима."""
    print("Выберите режим работы:")
    print()
    print("  1. 💻 Консольная версия")
    print("     - Интерактивный режим в терминале")
    print("     - Демонстрационный режим")
    print("     - Команды: stats, cache, clear_cache")
    print()
    print("  2. 📱 Telegram бот")
    print("     - Работа через Telegram")
    print("     - Команды: /start, /help, /stats, /logs")
    print("     - Требуется токен бота")
    print()
    print("  3. ❌ Выход")
    print()


def check_telegram_token():
    """Проверяет наличие токена Telegram бота."""
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token or token == "your_telegram_bot_token_here":
        print("\n⚠️  ВНИМАНИЕ: Не найден TELEGRAM_BOT_TOKEN!")
        print()
        print("Для работы Telegram бота необходимо:")
        print("1. Получить токен у @BotFather в Telegram")
        print("2. Добавить токен в файл .env:")
        print("   TELEGRAM_BOT_TOKEN=ваш_токен")
        print()
        return False
    return True


def check_openai_key():
    """Проверяет наличие OpenAI API ключа."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key or api_key == "your_openai_api_key_here":
        print("\n⚠️  ВНИМАНИЕ: Не найден OPENAI_API_KEY!")
        print()
        print("Для работы системы необходимо:")
        print("1. Получить API ключ на https://platform.openai.com/api-keys")
        print("2. Добавить ключ в файл .env:")
        print("   OPENAI_API_KEY=ваш_ключ")
        print()
        return False
    return True


def run_console_mode():
    """Запускает консольную версию."""
    clear_screen()
    print_header()
    print("🚀 Запуск консольной версии...")
    print()
    
    if not check_openai_key():
        input("\nНажмите Enter для возврата в меню...")
        return
    
    try:
        # Запускаем main.py
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Программа остановлена пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка при запуске: {str(e)}")
        input("\nНажмите Enter для возврата в меню...")


def run_telegram_bot():
    """Запускает Telegram бота."""
    clear_screen()
    print_header()
    print("🚀 Запуск Telegram бота...")
    print()
    
    if not check_openai_key():
        input("\nНажмите Enter для возврата в меню...")
        return
    
    if not check_telegram_token():
        input("\nНажмите Enter для возврата в меню...")
        return
    
    try:
        # Запускаем bot_main.py
        subprocess.run([sys.executable, "bot_main.py"], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Бот остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка при запуске: {str(e)}")
        input("\nНажмите Enter для возврата в меню...")


def main():
    """Главная функция с меню выбора."""
    # Устанавливаем UTF-8 для вывода в консоль Windows
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        try:
            choice = input("Введите номер (1-3): ").strip()
            
            if choice == "1":
                run_console_mode()
            elif choice == "2":
                run_telegram_bot()
            elif choice == "3":
                clear_screen()
                print("👋 До свидания!")
                break
            else:
                print("\n❌ Неверный выбор. Попробуйте снова.")
                input("\nНажмите Enter для продолжения...")
        
        except KeyboardInterrupt:
            clear_screen()
            print("\n👋 До свидания!")
            break
        except Exception as e:
            print(f"\n❌ Ошибка: {str(e)}")
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()
