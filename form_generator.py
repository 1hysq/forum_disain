#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
УЛУЧШЕННЫЙ ГЕНЕРАТОР ФОРМ ДЛЯ BLACKRUSSIA
Вставляешь форму одним блоком → заполняешь → получаешь BB-код
Версия: 1.2.0
"""

import json
import os
import re
import hashlib
import urllib.request
import urllib.error
import datetime
import webbrowser
import tempfile
import sys
from pathlib import Path

class ImprovedFormGenerator:
    def __init__(self):
        # УЛУЧШЕННЫЕ ЦВЕТА для лучшей читаемости
        self.designs = {
            "1": {"name": "🔴 Классический красный", 
                  "header": "#CC0000", 
                  "question": "#FF3333",  # Более яркий красный для вопросов
                  "answer": "#FFFFFF",    # Белый для ответов
                  "link": "#FF6666"},     # Светло-красный для ссылок
            
            "2": {"name": "🔵 Профессиональный синий", 
                  "header": "#1E3A5F", 
                  "question": "#3498DB",  # Яркий синий для вопросов
                  "answer": "#ECF0F1",    # Светло-серый для ответов
                  "link": "#2980B9"},     # Синий для ссылок
            
            "3": {"name": "⚫ Тёмный минимализм", 
                  "header": "#222222", 
                  "question": "#E74C3C",  # Ярко-красный для вопросов
                  "answer": "#F0F0F0",    # Почти белый для ответов
                  "link": "#3498DB"},     # Голубой для ссылок
            
            "4": {"name": "🟢 Зелёный спокойный", 
                  "header": "#2D5016", 
                  "question": "#2ECC71",  # Ярко-зеленый для вопросов
                  "answer": "#EAFAF1",    # Светло-зеленый для ответов
                  "link": "#27AE60"},     # Зеленый для ссылок
        }
        
        self.output_folder = "form_blackrussia"
        
        # Информация о версии и обновлениях
        self.current_version = "1.2.0"
        self.update_check_url = "https://raw.githubusercontent.com/1hysq/forum_disain/main/version.txt"
        self.github_page_url = "https://github.com/1hysq/forum_disain"
        
        # Создаем папку при инициализации
        self.create_output_folder()
        
        # Проверяем обновления при запуске
        self.check_for_updates_on_start()
    
    def create_output_folder(self):
        """Создание папки для сохранения результатов"""
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
    
    def clear_screen(self):
        """Очистка экрана"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_title(self, text):
        """Красивый заголовок"""
        print("\n" + "═" * 60)
        print(f"🎮 {text}")
        print("═" * 60)
    
    def check_for_updates_on_start(self):
        """Проверка обновлений при запуске программы"""
        try:
            # Проверяем, когда последний раз проверяли обновления
            last_check_file = "last_update_check.txt"
            should_check = True
            
            if os.path.exists(last_check_file):
                with open(last_check_file, 'r') as f:
                    try:
                        last_check = datetime.datetime.fromisoformat(f.read().strip())
                        now = datetime.datetime.now()
                        # Проверяем раз в день
                        if (now - last_check).days < 1:
                            should_check = False
                    except:
                        pass
            
            if should_check:
                self.check_for_updates(silent=True)
                # Сохраняем время проверки
                with open(last_check_file, 'w') as f:
                    f.write(datetime.datetime.now().isoformat())
                    
        except Exception as e:
            # Молча игнорируем ошибки при проверке обновлений
            pass
    
    def check_for_updates(self, silent=False):
        """Проверка наличия обновлений"""
        try:
            if not silent:
                print("\n🔍 Проверяем наличие обновлений...")
            
            headers = {'User-Agent': 'Mozilla/5.0'}
            req = urllib.request.Request(self.update_check_url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=5) as response:
                content = response.read().decode('utf-8').strip()
                
                # Убираем все лишние символы, оставляем только версию
                # Ищем версию в формате X.X.X или X.X.X.X
                version_match = re.search(r'(\d+\.\d+(?:\.\d+)*)', content)
                if version_match:
                    latest_version = version_match.group(1)
                    
                    # Сравниваем версии
                    comparison = self.compare_versions(self.current_version, latest_version)
                    
                    if comparison < 0:
                        if not silent:
                            print(f"\n🎉 Доступно обновление!")
                            print(f"   Текущая версия: {self.current_version}")
                            print(f"   Новая версия: {latest_version}")
                            print(f"\n📥 Скачать обновление можно по ссылке:")
                            print(f"   {self.github_page_url}")
                            
                            choice = input("\nХотите открыть страницу загрузки? (y/n): ").lower()
                            if choice == 'y':
                                webbrowser.open(self.github_page_url)
                        return True
                    else:
                        if not silent:
                            print("✅ У вас установлена последняя версия!")
                        return False
                else:
                    if not silent:
                        print(f"❌ Не удалось найти версию в файле. Содержимое: '{content}'")
                    return False
                
        except urllib.error.URLError:
            if not silent:
                print("❌ Не удалось проверить обновления. Проверьте подключение к интернету.")
        except Exception as e:
            if not silent:
                print(f"❌ Ошибка при проверке обновлений: {e}")
        return False
    
    def compare_versions(self, v1, v2):
        """Сравнение версий"""
        def parse_version(v):
            # Убираем все нецифровые символы кроме точек
            v = re.sub(r'[^\d\.]', '', v)
            # Разбиваем на части
            parts = []
            for part in v.split('.'):
                try:
                    parts.append(int(part))
                except ValueError:
                    parts.append(0)
            # Дополняем до 3 частей
            while len(parts) < 3:
                parts.append(0)
            return parts
        
        v1_parts = parse_version(v1)
        v2_parts = parse_version(v2)
        
        # Сравниваем по частям
        for i in range(max(len(v1_parts), len(v2_parts))):
            v1_part = v1_parts[i] if i < len(v1_parts) else 0
            v2_part = v2_parts[i] if i < len(v2_parts) else 0
            
            if v1_part < v2_part:
                return -1
            elif v1_part > v2_part:
                return 1
        
        return 0
    
    def get_form_input(self):
        """Получение формы от пользователя - УЛУЧШЕННАЯ ВЕРСИЯ"""
        self.clear_screen()
        self.print_title("ВВОД ФОРМЫ")
        
        print("📝 Вставьте вашу форму целиком (копируйте из темы на форуме)")
        print("\n📌 ВАЖНО: После вставки просто дважды нажмите Enter для завершения")
        print("   Это быстро и защищает от случайного ввода!")
        print("-" * 60)
        
        print("\n📋 ВСТАВЬТЕ ВАШУ ФОРМУ СЕЙЧАС:")
        print("=" * 60)
        
        lines = []
        print("\n[Начинайте ввод. Для завершения введите две пустые строки подряд]\n")
        
        empty_line_count = 0
        
        while True:
            try:
                line = input().rstrip('\n')
                
                # Проверяем на пустую строку
                if line == "":
                    empty_line_count += 1
                    if empty_line_count >= 2:
                        print("\n✅ Ввод завершен (две пустые строки)")
                        break
                    continue
                else:
                    empty_line_count = 0
                
                lines.append(line)
                    
            except KeyboardInterrupt:
                print("\n\n⚠️  Ввод прерван пользователем.")
                confirm = input("Завершить ввод? (y/n): ").lower()
                if confirm == 'y':
                    break
                else:
                    print("Продолжайте ввод...")
                    empty_line_count = 0
                    continue
            except EOFError:
                print("\n\n📥 Обнаружен конец ввода. Завершаем...")
                break
            except Exception as e:
                print(f"\n⚠️  Произошла ошибка: {e}")
                return None, None
        
        if not lines:
            print("❌ Вы не ввели форму!")
            return None, None
        
        # Объединяем в одну строку
        full_text = "\n".join(lines)
        
        # Быстрая проверка
        print(f"\n✅ Получено строк: {len(lines)}")
        print(f"📏 Длина текста: {len(full_text)} символов")
        
        # Показываем первые 3 строки для проверки
        print("\n📄 ПРЕДПРОСМОТР (первые 3 строки):")
        print("-" * 40)
        for i, line in enumerate(lines[:3]):
            print(f"{i+1}: {line[:80]}{'...' if len(line) > 80 else ''}")
        if len(lines) > 3:
            print(f"... и еще {len(lines) - 3} строк")
        print("-" * 40)
        
        # Быстрое подтверждение
        confirm = input("\n✅ Форма введена правильно? (y/n): ").lower()
        if confirm != 'y':
            print("\n🔄 Попробуем еще раз...")
            return self.get_form_input()
        
        # Извлекаем заголовок и вопросы
        return self.parse_full_form(full_text)
    
    def remove_questions(self, questions):
        """Удаление ненужных вопросов из формы"""
        self.clear_screen()
        self.print_title("УДАЛЕНИЕ ВОПРОСОВ")
        
        print("📝 Укажите номера вопросов, которые нужно удалить (через запятую или диапазон)")
        print("Пример: 1,3,5-7,10")
        print("Пример 2: все - удалить все вопросы")
        print("-" * 60)
        
        # Показываем все вопросы с номерами
        for i, q in enumerate(questions):
            preview = q['original'][:60] + "..." if len(q['original']) > 60 else q['original']
            print(f"{i+1:3d}. {preview}")
        
        print("-" * 60)
        
        while True:
            try:
                delete_input = input("\nВведите номера для удаления (или Enter чтобы пропустить): ").strip().lower()
                
                if not delete_input:
                    print("✅ Удаление отменено.")
                    return
                
                # Проверка на удаление всех
                if delete_input == "все":
                    confirm = input("⚠️  Удалить ВСЕ вопросы? (y/n): ").lower()
                    if confirm == 'y':
                        questions.clear()
                        print("✅ Все вопросы удалены.")
                        return
                    else:
                        print("✅ Удаление отменено.")
                        continue
                
                # Парсим ввод
                indices_to_delete = set()
                parts = delete_input.split(',')
                
                for part in parts:
                    part = part.strip()
                    if '-' in part:
                        start, end = part.split('-')
                        start_idx = int(start.strip()) - 1
                        end_idx = int(end.strip()) - 1
                        for idx in range(min(start_idx, end_idx), max(start_idx, end_idx) + 1):
                            if 0 <= idx < len(questions):
                                indices_to_delete.add(idx)
                    else:
                        idx = int(part) - 1
                        if 0 <= idx < len(questions):
                            indices_to_delete.add(idx)
                
                if not indices_to_delete:
                    print("⚠️  Не указаны корректные номера вопросов.")
                    continue
                
                # Быстрое подтверждение
                print(f"\n⚠️  Будут удалены {len(indices_to_delete)} вопросов: {sorted([i+1 for i in indices_to_delete])}")
                confirm = input("Подтвердить удаление? (y/n): ").lower()
                
                if confirm == 'y':
                    # Удаляем в обратном порядке
                    for idx in sorted(indices_to_delete, reverse=True):
                        questions.pop(idx)
                    
                    print(f"✅ Удалено {len(indices_to_delete)} вопросов.")
                    print(f"📋 Осталось вопросов: {len(questions)}")
                    
                    # Пересчитываем номера
                    for i, q in enumerate(questions):
                        q['number'] = i + 1
                    
                    break
                else:
                    print("✅ Удаление отменено.")
                    break
                    
            except ValueError:
                print("❌ Неверный формат. Используйте числа, запятые и тире или 'все'.")
            except Exception as e:
                print(f"❌ Ошибка: {e}")
    
    def clean_question_text(self, text):
        """Очистка текста вопроса"""
        # Убираем номер в начале
        cleaned = re.sub(r'^\d+[\.\)]\s*', '', text)
        # Убираем двоеточие в конце если есть
        if cleaned.endswith(':'):
            cleaned = cleaned[:-1].strip()
        return cleaned
    
    def parse_full_form(self, text):
        """Парсинг полной формы - УЛУЧШЕННАЯ ВЕРСИЯ"""
        lines = [line.rstrip() for line in text.split('\n') if line.strip() != '']
        
        if not lines:
            return "ФОРМА ЗАЯВЛЕНИЯ", []
        
        # Ищем заголовок
        title = "ФОРМА ЗАЯВЛЕНИЯ"
        for i, line in enumerate(lines):
            if any(word in line.lower() for word in ["форма", "заявление", "анкета", "заявка"]):
                title = line
                break
        
        # Ищем вопросы - улучшенная логика
        questions = []
        current_question = []
        in_question = False
        
        for line in lines:
            # Проверяем, начинается ли строка с номера вопроса
            if re.match(r'^\d+[\.\)]\s*', line):
                # Сохраняем предыдущий вопрос, если он есть
                if current_question and in_question:
                    question_text = ' '.join(current_question).strip()
                    if question_text:
                        questions.append({
                            "number": len(questions) + 1,
                            "original": question_text,
                            "clean": self.clean_question_text(question_text),
                            "type": self.detect_field_type(question_text)
                        })
                    current_question = []
                
                in_question = True
                current_question.append(line)
            elif in_question:
                # Продолжение вопроса (многострочные вопросы)
                current_question.append(line)
        
        # Добавляем последний вопрос
        if current_question and in_question:
            question_text = ' '.join(current_question).strip()
            if question_text:
                questions.append({
                    "number": len(questions) + 1,
                    "original": question_text,
                    "clean": self.clean_question_text(question_text),
                    "type": self.detect_field_type(question_text)
                })
        
        # Если не нашли вопросы стандартным способом, пытаемся другим
        if not questions:
            return self.alternative_parse(lines)
        
        return title, questions
    
    def alternative_parse(self, lines):
        """Альтернативный парсинг для сложных случаев"""
        title = "ФОРМА ЗАЯВЛЕНИЯ"
        questions = []
        
        for i, line in enumerate(lines):
            if any(word in line.lower() for word in ["форма", "заявление", "анкета"]):
                title = line
            elif re.match(r'^\d+[\.\)]\s*', line):
                questions.append({
                    "number": len(questions) + 1,
                    "original": line,
                    "clean": self.clean_question_text(line),
                    "type": self.detect_field_type(line)
                })
        
        return title, questions
    
    def detect_field_type(self, question):
        """Определение типа поля по вопросу"""
        question_lower = question.lower()
        
        # Скриншоты
        if any(word in question_lower for word in ["скриншот", "screenshot", "/time", "статистик", "статистики"]):
            return "screenshot"
        
        # Ссылки
        if any(word in question_lower for word in ["ссылка", "url", "сайт", "профиль", "биографи", "биография", "vk", "вк", "дискорд"]):
            return "link"
        
        # Длинные вопросы
        if len(question) > 50 or any(word in question_lower for word in ["почему", "расскажите", "обоснование", "считаете"]):
            return "multiline"
        
        # По умолчанию - текст
        return "text"
    
    def validate_input(self, question_text, answer, field_type):
        """Проверка введенных данных на валидность"""
        question_lower = question_text.lower()
        
        # Проверка возраста
        if any(word in question_lower for word in ["возраст", "лет", "годиков", "года", "годков", "age", "сколько лет"]):
            try:
                age = int(answer)
                if age < 14 or age > 100:
                    return False, "⚠️  Возраст должен быть в диапазоне от 14 до 100 лет."
                if age < 18:
                    return True, "⚠️  Внимание: вам меньше 18 лет. Убедитесь, что это правильно."
            except ValueError:
                return False, "⚠️  Возраст должен быть целым числом."
        
        # Проверка никнейма (не пустой и не слишком длинный)
        if any(word in question_lower for word in ["никнейм", "ник", "логин", "nickname", "nick"]):
            if not answer.strip():
                return False, "⚠️  Никнейм не может быть пустым."
            if len(answer) > 25:
                return False, "⚠️  Никнейм слишком длинный (максимум 25 символов)."
            if len(answer) < 3:
                return False, "⚠️  Никнейм слишком короткий (минимум 3 символа)."
        
        # Проверка уровня
        if any(word in question_lower for word in ["уровень", "level", "lvl"]):
            try:
                level = int(answer)
                if level < 1 or level > 100:
                    return False, "⚠️  Уровень должен быть в диапазоне от 1 до 100."
            except ValueError:
                return False, "⚠️  Уровень должен быть целым числом."
        
        # Проверка часового пояса
        if any(word in question_lower for word in ["часовой пояс", "таймзона", "timezone", "часовой"]):
            if not any(word in answer.lower() for word in ["gmt", "utc", "msk", "+", "-"]):
                return True, "⚠️  Убедитесь, что правильно указали часовой пояс (например, GMT+3, UTC+5, MSK)."
        
        # Проверка ссылок
        if field_type == "link" or field_type == "screenshot":
            if not answer.startswith(("http://", "https://")):
                return False, "⚠️  Ссылка должна начинаться с http:// или https://"
        
        # Общая проверка на слишком короткий ответ
        if len(answer.strip()) < 2 and field_type == "text":
            return True, "⚠️  Ответ очень короткий. Убедитесь, что это правильно."
        
        return True, "✅ Ответ принят"
    
    def fill_form(self, title, questions):
        """Заполнение формы"""
        self.clear_screen()
        self.print_title("ЗАПОЛНЕНИЕ ФОРМЫ")
        
        print(f"📝 Форма: {title}")
        print(f"📋 Вопросов: {len(questions)}")
        print("\n" + "=" * 60)
        print("🖊️  Теперь заполните форму. Вводите ответы для каждого вопроса.")
        print("=" * 60)
        
        filled_questions = []
        
        for q in questions:
            print(f"\n{'─' * 50}")
            print(f"❓ ВОПРОС {q['number']}. {q['clean']}:")
            
            field_type = q["type"]
            
            # Подсказки в зависимости от типа
            if field_type == "screenshot":
                print("📸 Вставьте ссылку на скриншот:")
                print("💡 Рекомендуемые сервисы: imgur.com, prnt.sc")
                print("   Пример: https://imgur.com/a/abc123")
                
                while True:
                    answer = input("Ссылка: ").strip()
                    
                    if not answer:
                        print("⚠️  Это поле обязательно для заполнения!")
                        continue
                    
                    # Добавляем https:// если нужно
                    if not answer.startswith(("http://", "https://")):
                        answer = f"https://{answer}"
                    
                    # Проверяем на сервисы скриншотов
                    screenshot_services = ["imgur.com", "prnt.sc", "prntscr.com", "gyazo.com"]
                    is_screenshot = any(service in answer.lower() for service in screenshot_services)
                    
                    # Проверка валидности
                    is_valid, message = self.validate_input(q['clean'], answer, field_type)
                    print(message)
                    
                    if is_screenshot or answer.startswith("https://"):
                        if is_valid:
                            break
                    else:
                        print("⚠️  Похоже, это не ссылка на скриншот.")
                        confirm = input("Использовать эту ссылку? (y/n): ").lower()
                        if confirm == 'y':
                            if is_valid:
                                break
            
            elif field_type == "link":
                print("🔗 Вставьте ссылку:")
                
                while True:
                    answer = input("Ссылка: ").strip()
                    
                    if not answer:
                        print("⚠️  Это поле обязательно для заполнения!")
                        continue
                    
                    if not answer.startswith(("http://", "https://")):
                        answer = f"https://{answer}"
                    
                    # Проверка валидности
                    is_valid, message = self.validate_input(q['clean'], answer, field_type)
                    print(message)
                    
                    if is_valid:
                        break
            
            elif field_type == "multiline":
                print("📄 Введите развернутый ответ:")
                print("(Нажмите Enter на пустой строке для завершения)")
                
                lines = []
                
                while True:
                    line = input(f"  Строка {len(lines)+1}: ").rstrip()
                    
                    if line == "":
                        if lines:
                            break
                        else:
                            print("  ⚠️  Ответ не может быть пустым!")
                            continue
                    else:
                        lines.append(line)
                
                answer = "\n".join(lines)
                
                # Проверка валидности
                is_valid, message = self.validate_input(q['clean'], answer, field_type)
                print(message)
            
            else:  # Текст
                while True:
                    answer = input("Ответ: ").strip()
                    
                    if not answer:
                        print("⚠️  Ответ не может быть пустым!")
                        continue
                    
                    # Проверка валидности
                    is_valid, message = self.validate_input(q['clean'], answer, field_type)
                    print(message)
                    
                    if is_valid:
                        break
            
            # Сохраняем заполненный вопрос
            filled_questions.append({
                "number": q["number"],
                "question": q["clean"],
                "original": q["original"],
                "answer": answer,
                "type": field_type
            })
        
        return filled_questions
    
    def preview_form(self, title, filled_questions):
        """Предпросмотр заполненной формы"""
        self.clear_screen()
        self.print_title("ПРЕДПРОСМОТР")
        
        print(f"📋 Форма: {title}")
        print("\nВаши ответы:")
        print("-" * 60)
        
        for q in filled_questions:
            answer_preview = q["answer"]
            if len(answer_preview) > 50:
                answer_preview = answer_preview[:47] + "..."
            
            type_icon = {
                "text": "📝",
                "link": "🔗", 
                "screenshot": "📸",
                "multiline": "📄"
            }.get(q["type"], "❓")
            
            print(f"{type_icon} ВОПРОС {q['number']}. {q['question']}:")
            print(f"   Ответ: {answer_preview}")
            print()
        
        print("-" * 60)
        
        # Даем возможность редактировать
        while True:
            print("\nОпции:")
            print("  1. ✅ Все верно, продолжить")
            print("  2. ✏️  Редактировать ответы")
            print("  3. 🔄 Начать заново")
            
            choice = input("Ваш выбор (1-3): ").strip()
            
            if choice == "1":
                return filled_questions
            elif choice == "2":
                return self.edit_answers(title, filled_questions)
            elif choice == "3":
                return None
            else:
                print("❌ Неверный выбор")
    
    def edit_answers(self, title, filled_questions):
        """Редактирование ответов"""
        self.clear_screen()
        self.print_title("РЕДАКТИРОВАНИЕ ОТВЕТОВ")
        
        print(f"📋 Форма: {title}")
        print("\nВыберите вопрос для редактирования:")
        
        for q in filled_questions:
            answer_preview = q["answer"]
            if len(answer_preview) > 30:
                answer_preview = answer_preview[:27] + "..."
            print(f"  [{q['number']}] ВОПРОС {q['number']}. {q['question'][:40]}... → {answer_preview}")
        
        print("\n  [0] ✅ Завершить редактирование")
        
        while True:
            try:
                choice = int(input("\nНомер вопроса: ").strip())
                
                if choice == 0:
                    return filled_questions
                
                # Находим вопрос
                q_to_edit = next((q for q in filled_questions if q["number"] == choice), None)
                if q_to_edit:
                    print(f"\n✏️  Редактирование вопроса {choice}:")
                    print(f"Вопрос: ВОПРОС {q_to_edit['number']}. {q_to_edit['question']}:")
                    print(f"Текущий ответ: {q_to_edit['answer']}")
                    
                    new_answer = input("Новый ответ: ").strip()
                    if new_answer:
                        # Проверка валидности нового ответа
                        is_valid, message = self.validate_input(q_to_edit['question'], new_answer, q_to_edit['type'])
                        print(message)
                        
                        if is_valid:
                            q_to_edit["answer"] = new_answer
                            print("✅ Ответ обновлен")
                        else:
                            confirm = input("Все равно использовать этот ответ? (y/n): ").lower()
                            if confirm == 'y':
                                q_to_edit["answer"] = new_answer
                                print("✅ Ответ обновлен")
                            else:
                                print("⚠️  Ответ не изменен")
                    else:
                        print("⚠️  Ответ не изменен")
                else:
                    print("❌ Вопрос с таким номером не найден")
            
            except ValueError:
                print("❌ Введите номер вопроса")
    
    def select_design(self):
        """Выбор оформления"""
        self.clear_screen()
        self.print_title("ВЫБОР ОФОРМЛЕНИЯ")
        
        print("🎨 Выберите стиль оформления:")
        for key, design in self.designs.items():
            print(f"  [{key}] {design['name']}")
        
        print("\n  [5] ⚙️  Настроить свои цвета")
        
        while True:
            choice = input("\nВаш выбор (1-5): ").strip()
            
            if choice == "5":
                return self.custom_design()
            
            if choice in self.designs:
                return self.designs[choice]
            
            print("❌ Неверный выбор")
    
    def custom_design(self):
        """Ручная настройка дизайна"""
        self.clear_screen()
        self.print_title("НАСТРОЙКА ЦВЕТОВ")
        
        print("🎨 Введите цвета в формате HEX (#RRGGBB)")
        print("\n💡 Рекомендации:")
        print("  • Цвет вопросов: яркий, заметный (#FF3333, #3498DB)")
        print("  • Цвет ответов: светлый, хорошо читаемый (#FFFFFF, #ECF0F1)")
        print("  • Цвет ссылок: контрастный (#FF6666, #2980B9)")
        print()
        
        colors = {}
        colors["header"] = input("Цвет заголовка [#CC0000]: ").strip() or "#CC0000"
        colors["question"] = input("Цвет вопросов [#FF3333]: ").strip() or "#FF3333"
        colors["answer"] = input("Цвет ответов [#FFFFFF]: ").strip() or "#FFFFFF"
        colors["link"] = input("Цвет ссылок [#0066CC]: ").strip() or "#0066CC"
        
        return {
            "name": "⚙️  Пользовательский дизайн",
            "header": colors["header"],
            "question": colors["question"],
            "answer": colors["answer"],
            "link": colors["link"]
        }
    
    def generate_bbcode(self, title, filled_questions, design):
        """Генерация BB-кода"""
        
        # Создаем строки таблицы
        rows = []
        
        for q in filled_questions:
            # Форматируем вопрос (убираем лишние пробелы, добавляем двоеточие)
            question_text = q["question"]
            if not question_text.endswith(":"):
                question_text = f"{question_text}:"
            
            question_display = f"ВОПРОС {q['number']}. {question_text}"
            answer = q["answer"]
            field_type = q["type"]
            
            # Обработка разных типов ответов
            if field_type == "screenshot":
                if answer:
                    answer_bb = f'[color={design["link"]}][url={answer}]Скриншот[/url][/color]'
                else:
                    answer_bb = f'[color={design["answer"]}](скриншот не загружен)[/color]'
            
            elif field_type == "link":
                if answer:
                    # Определяем текст для ссылки
                    q_lower = q["question"].lower()
                    if "vk" in q_lower or "вк" in q_lower:
                        display_text = "Профиль ВК"
                    elif "discord" in q_lower or "дискорд" in q_lower:
                        display_text = "Discord"
                    elif "биограф" in q_lower:
                        display_text = "Биография"
                    else:
                        display_text = "Ссылка"
                    
                    answer_bb = f'[color={design["link"]}][url={answer}]{display_text}[/url][/color]'
                else:
                    answer_bb = f'[color={design["answer"]}](ссылка не указана)[/color]'
            
            elif field_type == "multiline":
                if answer:
                    lines = answer.split('\n')
                    formatted_lines = []
                    for line in lines:
                        if line.strip():
                            formatted_lines.append(f'[color={design["answer"]}]{line.strip()}[/color]')
                    answer_bb = '\n'.join(formatted_lines)
                else:
                    answer_bb = f'[color={design["answer"]}](не заполнено)[/color]'
            
            else:  # Обычный текст
                answer_bb = f'[color={design["answer"]}]{answer}[/color]'
            
            # Создаем строку таблицы
            row = f'[tr][td][color={design["question"]}][b]{question_display}[/b][/color][/td][td]{answer_bb}[/td][/tr]'
            rows.append(row)
        
        # Собираем полный BB-код
        bbcode = f"""[center][font=Courier New]
[size=11][b][color={design["header"]}]┌────────────────────┐[/color]
{title.upper()}
[color={design["header"]}]└────────────────────┘[/color][/b][/size]

[size=9]
[table]
{"\n".join(rows)}
[/table]
[/size]
[/font][/center]"""
        
        return bbcode
    
    def get_bbcode_hash(self, bbcode):
        """Получение хэша BB-кода для сравнения"""
        return hashlib.md5(bbcode.encode('utf-8')).hexdigest()
    
    def save_results(self, title, filled_questions, bbcode, design, bbcode_hash):
        """Сохранение результатов"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = title.replace(" ", "_").replace(":", "").lower()[:20]
        
        # Гарантируем, что папка существует
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        
        # Проверяем, был ли уже сохранен такой же BB-код
        existing_files = os.listdir(self.output_folder)
        for file_name in existing_files:
            if file_name.endswith('.json'):
                try:
                    with open(os.path.join(self.output_folder, file_name), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'bbcode_hash' in data and data['bbcode_hash'] == bbcode_hash:
                            print("\n⚠️  Этот BB-код уже был сохранен ранее!")
                            print("Файл:", file_name)
                            print("Возвращаемся в главное меню...")
                            return False, None
                except:
                    continue
        
        # Сохраняем BB-код
        bbcode_file = os.path.join(self.output_folder, f"{safe_title}_{timestamp}.txt")
        with open(bbcode_file, 'w', encoding='utf-8') as f:
            f.write(bbcode)
        
        # Сохраняем данные
        data_file = os.path.join(self.output_folder, f"{safe_title}_{timestamp}.json")
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump({
                "title": title,
                "questions": filled_questions,
                "design": design,
                "bbcode": bbcode,
                "bbcode_hash": bbcode_hash,  # Сохраняем хэш для проверки
                "generated": timestamp
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 РЕЗУЛЬТАТЫ СОХРАНЕНЫ:")
        print(f"  📄 BB-код: {bbcode_file}")
        print(f"  📊 Данные: {data_file}")
        print(f"\n📁 Файлы сохранены в папку: {os.path.abspath(self.output_folder)}")
        
        # Копирование в буфер обмена (если доступно)
        try:
            import pyperclip
            pyperclip.copy(bbcode)
            print("📋 BB-код скопирован в буфер обмена!")
        except:
            print("📋 Скопируйте BB-код выше вручную")
        
        return True, bbcode_hash
    
    def show_results_menu(self, title, original_questions, filled_questions, design, last_bbcode_hash=None):
        """Меню управления после генерации BB-кода"""
        current_filled_questions = filled_questions.copy()
        current_design = design.copy()
        current_bbcode = self.generate_bbcode(title, current_filled_questions, current_design)
        current_bbcode_hash = self.get_bbcode_hash(current_bbcode)
        
        # Проверяем, не пытаемся ли сохранить тот же самый BB-код
        if last_bbcode_hash == current_bbcode_hash:
            print("\n⚠️  Этот BB-код уже был сгенерирован ранее!")
            print("Возвращаемся в главное меню...")
            return
        
        while True:
            self.clear_screen()
            self.print_title("ГОТОВЫЙ BB-КОД")
            print(current_bbcode)
            
            print("\n" + "=" * 60)
            print("МЕНЮ УПРАВЛЕНИЯ:")
            print("  1. 💾 СОХРАНИТЬ РЕЗУЛЬТАТ")
            print("  2. ❌ НЕ СОХРАНЯТЬ РЕЗУЛЬТАТ")
            print("  3. 🎨 ВЫБРАТЬ ДРУГОЙ СТИЛЬ")
            print("  4. 🔄 ЗАПОЛНИТЬ ЭТУ ФОРМУ СНОВА")
            print("  5. ✏️  РЕДАКТИРОВАТЬ ЭТУ ФОРМУ")
            print("  6. 🚀 ЗАПОЛНИТЬ НОВУЮ ФОРМУ")
            print("=" * 60)
            
            choice = input("\nВаш выбор (1-6): ").strip()
            
            if choice == "1":
                # СОХРАНИТЬ РЕЗУЛЬТАТ
                saved, new_hash = self.save_results(title, current_filled_questions, current_bbcode, current_design, current_bbcode_hash)
                if saved:
                    input("\n↵ Нажмите Enter чтобы вернуться в меню...")
                else:
                    # Если BB-код уже был сохранен, возвращаемся в главное меню
                    input("\n↵ Нажмите Enter чтобы продолжить...")
                    return
            
            elif choice == "2":
                # НЕ СОХРАНЯТЬ РЕЗУЛЬТАТ
                confirm = input("Вы уверены, что не хотите сохранить результат? (y/n): ").lower()
                if confirm == 'y':
                    print("✅ Возвращаемся в главное меню...")
                    return
            
            elif choice == "3":
                # ВЫБРАТЬ ДРУГОЙ СТИЛЬ
                new_design = self.select_design()
                current_design = new_design
                current_bbcode = self.generate_bbcode(title, current_filled_questions, current_design)
                current_bbcode_hash = self.get_bbcode_hash(current_bbcode)
                print("✅ Стиль изменен!")
                input("\n↵ Нажмите Enter чтобы продолжить...")
            
            elif choice == "4":
                # ЗАПОЛНИТЬ ЭТУ ФОРМУ СНОВА
                print("\n🔄 Начинаем заполнение формы заново...")
                confirm = input("Текущие ответы будут удалены. Продолжить? (y/n): ").lower()
                if confirm == 'y':
                    new_filled_questions = self.fill_form(title, original_questions)
                    if new_filled_questions:
                        # Предпросмотр после заполнения
                        new_filled_questions = self.preview_form(title, new_filled_questions)
                        if new_filled_questions:
                            current_filled_questions = new_filled_questions
                            current_bbcode = self.generate_bbcode(title, current_filled_questions, current_design)
                            current_bbcode_hash = self.get_bbcode_hash(current_bbcode)
                            print("✅ Форма заполнена заново!")
                        else:
                            print("❌ Заполнение отменено!")
                    else:
                        print("❌ Форма не заполнена!")
                else:
                    print("✅ Отменено.")
                input("\n↵ Нажмите Enter чтобы продолжить...")
            
            elif choice == "5":
                # РЕДАКТИРОВАТЬ ЭТУ ФОРМУ
                edited_questions = self.edit_answers(title, current_filled_questions)
                if edited_questions:
                    current_filled_questions = edited_questions
                    current_bbcode = self.generate_bbcode(title, current_filled_questions, current_design)
                    current_bbcode_hash = self.get_bbcode_hash(current_bbcode)
                    print("✅ Форма обновлена!")
                else:
                    print("❌ Редактирование отменено!")
                input("\n↵ Нажмите Enter чтобы продолжить...")
            
            elif choice == "6":
                # ЗАПОЛНИТЬ НОВУЮ ФОРМУ
                confirm = input("Вы уверены, что хотите заполнить новую форму? (y/n): ").lower()
                if confirm == 'y':
                    print("🚀 Начинаем новую форму...")
                    # Рекурсивно запускаем новый процесс
                    self.run_workflow()
                    return
                else:
                    print("✅ Отменено.")
                    input("\n↵ Нажмите Enter чтобы продолжить...")
            
            else:
                print("❌ Неверный выбор!")
                input("\n↵ Нажмите Enter чтобы продолжить...")
    
    def run_workflow(self):
        """Основной рабочий процесс"""
        # Шаг 1: Ввод формы
        result = self.get_form_input()
        if not result:
            print("❌ Ошибка ввода формы!")
            return
        
        title, questions = result
        
        if not questions:
            print("❌ Не удалось извлечь вопросы из формы!")
            return
        
        print(f"\n✅ Извлечено {len(questions)} вопросов")
        
        # Даем возможность удалить вопросы
        while True:
            print("\n🎯 ОПЦИИ ФОРМЫ:")
            print("  1. ✅ Все верно, продолжить заполнение")
            print("  2. ❌ Удалить ненужные вопросы")
            print("  3. 🔄 Ввести форму заново")
            
            choice = input("\nВаш выбор (1-3): ").strip()
            
            if choice == "1":
                break
            elif choice == "2":
                self.remove_questions(questions)
                if not questions:
                    print("❌ Все вопросы удалены. Начнем заново.")
                    return self.run_workflow()
                break
            elif choice == "3":
                return self.run_workflow()
            else:
                print("❌ Неверный выбор")
        
        input("\n↵ Нажмите Enter чтобы начать заполнение...")
        
        # Шаг 2: Заполнение формы
        filled_questions = self.fill_form(title, questions)
        if not filled_questions:
            print("❌ Форма не заполнена!")
            return
        
        # Шаг 3: Предпросмотр
        filled_questions = self.preview_form(title, filled_questions)
        if not filled_questions:
            print("❌ Редактирование отменено!")
            return
        
        # Шаг 4: Выбор оформления
        design = self.select_design()
        
        # Шаг 5: Генерация BB-кода и меню управления
        self.show_results_menu(title, questions, filled_questions, design)
    
    def show_example(self):
        """Показать пример формы"""
        self.clear_screen()
        self.print_title("ПРИМЕР ФОРМЫ")
        
        print("📋 Вот как должна выглядеть форма для вставки:")
        print()
        print("=" * 60)
        print("Форма подачи:")
        print()
        print("1. Ваш игровой Никнейм:")
        print("2. Ваш игровой уровень:")
        print("3. Скриншот статистики аккаунта(/time):")
        print("4. Были ли баны/варны(если да, то за что):")
        print("5. Как вы считаете, почему именно вы должны занять пост старшего состава:")
        print("6. Были ли ранее на руководящей должности:")
        print("7. Ссылка на одобренную РП биографию (обязательна для занятия должности заместителя организации):")
        print("8. Ваш часовой пояс:")
        print("9. Ссылка на страницу ВК:")
        print("10. Логин Discord:")
        print("11. Ваше реальное имя:")
        print("12. Ваш реальный возраст:")
        print("=" * 60)
        print()
        print("💡 Просто скопируйте ЭТОТ ТЕКСТ целиком и вставьте в программу!")
        
        input("\n↵ Нажмите Enter чтобы вернуться...")
    
    def show_designs(self):
        """Показать доступные стили"""
        self.clear_screen()
        self.print_title("ДОСТУПНЫЕ СТИЛИ")
        
        print("🎨 Выберите один из стилей:")
        print("\n💡 Все цвета были улучшены для лучшей читаемости!")
        print()
        
        for key, design in self.designs.items():
            print(f"{design['name']}:")
            print(f"  Заголовок: [color={design['header']}]████[/color] ({design['header']})")
            print(f"  Вопросы:   [color={design['question']}]████[/color] ({design['question']})")
            print(f"  Ответы:    [color={design['answer']}]████[/color] ({design['answer']})")
            print(f"  Ссылки:    [color={design['link']}]████[/color] ({design['link']})")
            print()
        
        input("\n↵ Нажмите Enter чтобы вернуться...")
    
    def main_menu(self):
        """Главное меню"""
        while True:
            self.clear_screen()
            self.print_title("ГЕНЕРАТОР ФОРМ ДЛЯ BLACKRUSSIA")
            print(f"📦 Версия: {self.current_version}")
            
            print("🚀 ПРОСТОЙ ПОРЯДОК:")
            print("  1. Вставить готовую форму (копируешь из темы на форуме)")
            print("  2. Заполнить ответы")
            print("  3. Выбрать оформление")
            print("  4. Получить BB-код")
            
            print("\n" + "═" * 40)
            print("ГЛАВНОЕ МЕНЮ:")
            print("  1. 🚀 НАЧАТЬ СОЗДАНИЕ ФОРМЫ")
            print("  2. 📖 ПОКАЗАТЬ ПРИМЕР ФОРМЫ")
            print("  3. 🎨 ПОСМОТРЕТЬ СТИЛИ")
            print("  4. 🔄 ПРОВЕРИТЬ ОБНОВЛЕНИЯ")
            print("  5. 🚪 ВЫХОД")
            
            choice = input("\nВаш выбор (1-5): ").strip()
            
            if choice == "1":
                self.run_workflow()
            
            elif choice == "2":
                self.show_example()
            
            elif choice == "3":
                self.show_designs()
            
            elif choice == "4":
                self.check_for_updates(silent=False)
                input("\n↵ Нажмите Enter чтобы продолжить...")
            
            elif choice == "5":
                print("\n👋 До свидания!")
                break
            
            else:
                print("❌ Неверный выбор!")
                input("\n↵ Нажмите Enter чтобы продолжить...")

def main():
    """Запуск программы"""
    try:
        generator = ImprovedFormGenerator()
        generator.main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Программа прервана")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        input("\n↵ Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()