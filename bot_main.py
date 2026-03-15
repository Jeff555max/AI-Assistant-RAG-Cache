"""
Главный файл для запуска Telegram бота с RAG-ассистентом.

Инициализирует все компоненты и запускает бота.
"""

import os
from dotenv import load_dotenv
from embeddings import EmbeddingStore, get_sample_documents
from rag import RAGAssistant
from cache import ResponseCache
from db_logger import DatabaseLogger
from telegram_bot import TelegramRAGBot


def main():
    """
    Главная функция для запуска Telegram бота.
    """
    print("=" * 70)
    print("🤖 ИНИЦИАЛИЗАЦИЯ TELEGRAM RAG-БОТА")
    print("=" * 70)
    
    # Загружаем переменные окружения
    load_dotenv()
    
    # Проверяем наличие необходимых ключей
    api_key = os.getenv("OPENAI_API_KEY")
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not api_key:
        print("❌ ОШИБКА: Не найден OPENAI_API_KEY в .env файле!")
        print("   Добавьте: OPENAI_API_KEY=your_key_here")
        return
    
    if not telegram_token:
        print("❌ ОШИБКА: Не найден TELEGRAM_BOT_TOKEN в .env файле!")
        print("   Получите токен у @BotFather и добавьте: TELEGRAM_BOT_TOKEN=your_token_here")
        return
    
    try:
        # 1. Инициализируем логгер
        print("\n[1/4] Инициализация логгера базы данных...")
        logger = DatabaseLogger(db_path="logs.db")
        
        # 2. Инициализируем кеш
        print("\n[2/4] Инициализация кеша...")
        cache = ResponseCache(cache_file="cache.json")
        
        # 3. Инициализируем векторное хранилище
        print("\n[3/4] Инициализация векторного хранилища...")
        embedding_store = EmbeddingStore(
            collection_name="rag_documents",
            persist_directory="./chroma_db",
            embedding_model="text-embedding-3-small",
            api_key=api_key
        )
        
        # Проверяем, нужно ли добавить примеры документов
        if embedding_store.collection.count() == 0:
            print("\n📝 База данных пуста. Добавляем примеры документов...")
            sample_docs = get_sample_documents()
            embedding_store.add_documents(sample_docs)
        else:
            print(f"✓ В базе уже есть {embedding_store.collection.count()} документов")
        
        # 4. Инициализируем RAG-ассистента
        print("\n[4/4] Инициализация RAG-ассистента...")
        rag_assistant = RAGAssistant(
            embedding_store=embedding_store,
            model="gpt-4o-mini",
            temperature=0.7
        )
        
        print("\n" + "=" * 70)
        print("✅ ВСЕ КОМПОНЕНТЫ ИНИЦИАЛИЗИРОВАНЫ")
        print("=" * 70)
        
        # Создаем и запускаем Telegram бота
        print("\n🚀 Запуск Telegram бота...")
        bot = TelegramRAGBot(
            token=telegram_token,
            rag_assistant=rag_assistant,
            cache=cache,
            logger=logger
        )
        
        print("\n" + "=" * 70)
        print("✅ БОТ ЗАПУЩЕН И ГОТОВ К РАБОТЕ")
        print("=" * 70)
        print("\nБот ожидает сообщений в Telegram...")
        print("Для остановки нажмите Ctrl+C\n")
        
        # Запускаем бота
        bot.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 Бот остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
