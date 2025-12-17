#!/usr/bin/env python3
"""
Главный скрипт для запуска всех тестов.
"""
import subprocess
import sys
import os

def print_header(text):
    """Печатает заголовок."""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)

def run_test_suite(test_files, category_name):
    """Запускает набор тестов."""
    print_header(f"Запуск {category_name} тестов")
    
    all_passed = True
    total_tests = len(test_files)
    passed_tests = 0
    
    for test_file in test_files:
        if not os.path.exists(test_file):
            print(f"⚠️  Файл не найден: {test_file}")
            continue
        
        test_name = os.path.basename(test_file)
        print(f"\n▶  Запуск: {test_name}")
        print("-" * 40)
        
        try:
            # Запускаем pytest
            cmd = [sys.executable, "-m", "pytest", test_file, "-v", "--tb=short"]
            result = subprocess.run(cmd, text=True, capture_output=True, timeout=30)
            
            # Выводим результат
            if result.stdout:
                # Выводим только summary
                lines = result.stdout.strip().split('\n')
                for line in lines[-10:]:  # Последние 10 строк
                    if line.strip():
                        print(line)
            
            if result.stderr:
                print("Ошибки:", file=sys.stderr)
                print(result.stderr, file=sys.stderr)
            
            if result.returncode == 0:
                print(f"✅ Успешно: {test_name}")
                passed_tests += 1
            else:
                print(f"❌ Ошибки в: {test_name}")
                all_passed = False
                
        except subprocess.TimeoutExpired:
            print(f"⏰ Таймаут: {test_name}")
            all_passed = False
        except Exception as e:
            print(f"❌ Ошибка запуска: {e}")
            all_passed = False
    
    # Статистика
    print(f"\n📊 {category_name}: {passed_tests}/{total_tests} тестов пройдено")
    
    return all_passed

def run_all_tests():
    """Запускает все тесты."""
    print("🚀 Запуск тестов фитнес-приложения")
    print("Версия: 1.0.0")
    print(f"Python: {sys.version}")
    print(f"Рабочая директория: {os.getcwd()}")
    
    # Проверяем наличие pytest
    try:
        subprocess.run(
            [sys.executable, "-m", "pytest", "--version"], 
            capture_output=True, 
            check=True,
            timeout=5
        )
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        print("\n❌ Ошибка: pytest не установлен или недоступен")
        print("Установите pytest: pip install pytest")
        return 1
    
    # Определяем тестовые файлы по категориям
    test_categories = {
        "Базовые": [
            "tests/test_simple.py"
        ],
        "Клиент": [
            "tests/test_client_gui.py"
        ],
        "Сервер": [
            "tests/test_server.py"
        ],
        "Модели": [
            "tests/test_models_simple.py"
        ],
        "Интеграционные": [
            "tests/test_integration.py"
        ]
    }
    
    # Запускаем тесты по категориям
    results = {}
    
    for category, files in test_categories.items():
        # Фильтруем существующие файлы
        existing_files = [f for f in files if os.path.exists(f)]
        
        if existing_files:
            results[category] = run_test_suite(existing_files, category)
        else:
            print(f"\n⚠️  Нет тестов в категории: {category}")
    
    # Сводка
    print_header("Сводка результатов")
    
    total_categories = len(results)
    passed_categories = sum(1 for passed in results.values() if passed)
    
    print("📋 Результаты по категориям:")
    for category, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {category}")
    
    print(f"\n📊 Итог: {passed_categories}/{total_categories} категорий пройдено успешно")
    
    if passed_categories == total_categories:
        print("\n🎉 Все тесты пройдены успешно!")
        return 0
    else:
        print("\n⚠️  Некоторые тесты не пройдены.")
        print("   Проверьте вывод выше для деталей.")
        return 1

def run_quick_test():
    """Запускает быстрые тесты для проверки."""
    print("⚡ Запуск быстрых тестов для проверки")
    
    cmd = [sys.executable, "-m", "pytest", 
           "tests/test_simple.py",
           "tests/test_server.py",
           "-v", 
           "--tb=no",
           "--disable-warnings"]
    
    try:
        result = subprocess.run(cmd, text=True)
        return result.returncode
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return 1

def main():
    """Главная функция."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Запуск тестов фитнес-приложения")
    parser.add_argument("--quick", action="store_true", help="Запуск только быстрых тестов")
    parser.add_argument("--category", help="Запуск тестов определенной категории")
    
    args = parser.parse_args()
    
    if args.quick:
        return run_quick_test()
    elif args.category:
        # Запуск тестов определенной категории
        test_categories = {
            "basic": ["tests/test_simple.py"],
            "client": ["tests/test_client_gui.py"],
            "server": ["tests/test_server.py"],
            "models": ["tests/test_models_simple.py"],
            "integration": ["tests/test_integration.py"],
            "all": None  # Все тесты
        }
        
        if args.category.lower() == "all":
            return run_all_tests()
        elif args.category.lower() in test_categories:
            files = test_categories[args.category.lower()]
            if files:
                run_test_suite(files, args.category)
            return 0
        else:
            print(f"❌ Неизвестная категория: {args.category}")
            print(f"Доступные категории: {', '.join(test_categories.keys())}")
            return 1
    else:
        # Запуск всех тестов
        return run_all_tests()

if __name__ == "__main__":
    # Устанавливаем рабочую директорию
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Запускаем тесты
    exit_code = main()
    sys.exit(exit_code)