#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
УЛУЧШЕННЫЙ ГЕНЕРАТОР ФОРМ ДЛЯ BLACKRUSSIA
Вставляешь форму одним блоком → заполняешь → получаешь BB-код
"""

import json
import os
import re
import hashlib
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
        
        # Создаем папку при инициализации
        self.create_output_folder()
    
    def create_output_folder(self):
        """Создание папки для сохранения результатов"""
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            print(f"📁 Создана папка для сохранения: {self.output_folder}")
    
    def clear_screen(self):
        """Очистка экрана"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_title(self, text):
        """Красивый заголовок"""
        print("\n" + "═" * 60)
        print(f"🎮 {text}")
        print("═" * 60)
    
    def get_form_input(self):
        """Получение формы от пользователя - УЛУЧШЕННАЯ ВЕРСИЯ"""
        self.clear_screen()
        self.print_title("ВВОД ФОРМЫ")
        
        print("📝 Вставьте вашу форму целиком (копируйте из темы на форуме)")
        print("\n🔥 ВАЖНО: После вставки нажмите Enter, а затем введите слово 'ГОТОВО'")
        print("   Это защита от преждевременного завершения ввода!")
        print("-" * 60)
        
        print("\n📋 ВСТАВЬТЕ ВАШУ ФОРМУ СЕЙЧАС:")
        print("=" * 60)
        
        lines = []
        print("\n[Начинайте ввод. После завершения введите 'ГОТОВО' на отдельной строке]")
        
        # Счетчик для пустых строк подряд
        empty_lines_count = 0
        
        try:
            while True:
                try:
                    line = input()
                except EOFError:
                    print("\n⚠️  Обнаружен EOF. Завершаем ввод...")
                    break
                    
                # Проверяем команду завершения
                if line.strip().upper() == 'ГОТОВО':
                    print("✅ Ввод завершен по команде 'ГОТОВО'")
                    break
                    
                # Проверяем, не пытается ли пользователь завершить ввод
                if not line.strip():
                    empty_lines_count += 1
                    if empty_lines_count >= 2:
                        print("\n⚠️  Обнаружены две пустые строки подряд.")
                        confirm = input("Вы хотите завершить ввод? (y/n): ").lower()
                        if confirm == 'y':
                            break
                        else:
                            print("Продолжайте ввод...")
                            empty_lines_count = 0
                            continue
                else:
                    empty_lines_count = 0
                
                lines.append(line)
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Ввод прерван пользователем.")
            confirm = input("Завершить ввод? (y/n): ").lower()
            if confirm != 'y':
                return self.get_form_input()  # Начинаем заново
            return None, None
        
        if not lines:
            print("❌ Вы не ввели форму!")
            return None, None
        
        # Объединяем в одну строку
        full_text = "\n".join(lines)
        
        # Отладочная информация
        print(f"\n✅ Получено строк: {len(lines)}")
        print(f"📏 Длина текста: {len(full_text)} символов")
        
        # Показываем первые 5 строк для проверки
        print("\n📄 ПРЕДПРОСМОТР (первые 5 строк):")
        print("-" * 40)
        for i, line in enumerate(lines[:5]):
            print(f"{i+1}: {line[:60]}{'...' if len(line) > 60 else ''}")
        if len(lines) > 5:
            print(f"... и еще {len(lines) - 5} строк")
        print("-" * 40)
        
        # Проверяем, есть ли вопросы в форме
        confirm = input("\n✅ Форма введена правильно? (y/n): ").lower()
        if confirm != 'y':
            print("\n🔄 Попробуем еще раз...")
            return self.get_form_input()
        
        # Извлекаем заголовок и вопросы
        return self.parse_full_form(full_text)
    
    def clean_question_text(self, text):
        """Очистка текста вопроса"""
        # Убираем номер в начале
        cleaned = re.sub(r'^\d+[\.\)]\s*', '', text)
        # Убираем двоеточие в конце если есть
        if cleaned.endswith(':'):
            cleaned = cleaned[:-1].strip()
        return cleaned
    
    def alternative_parse(self, lines):
        """Альтернативный парсинг для сложных случаев"""
        questions = []
        
        # Паттерны для поиска вопросов
        patterns = [
            r'(\d+[\.\)]\s*.+?:)',  # Номер. текст:
            r'(\d+\.\s*.+)',       # Номер. текст
            r'^([^:]+?:)$',        # текст:
        ]
        
        for line in lines:
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    question_text = match.group(1).strip()
                    questions.append({
                        "number": len(questions) + 1,
                        "original": question_text,
                        "clean": self.clean_question_text(question_text),
                        "type": self.detect_field_type(question_text)
                    })
                    break
        
        return questions
    
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
            questions = self.alternative_parse(lines)
        
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
            # ИСПРАВЛЕНО: Правильный формат вывода вопроса
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
                    
                    if is_screenshot or answer.startswith("https://"):
                        break
                    else:
                        print("⚠️  Похоже, это не ссылка на скриншот. Убедитесь, что используете правильный сервис.")
                        confirm = input("Все равно использовать эту ссылку? (y/n): ").lower()
                        if confirm == 'y':
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
                    
                    break
            
            elif field_type == "multiline":
                print("📄 Введите развернутый ответ:")
                print("(Для завершения введите пустую строку)")
                
                lines = []
                line_num = 1
                
                while True:
                    line = input(f"  Строка {line_num}: ").strip()
                    if line == "":
                        if lines:
                            break
                        else:
                            print("  ⚠️  Ответ не может быть пустым!")
                            continue
                    lines.append(line)
                    line_num += 1
                
                answer = "\n".join(lines)
            
            else:  # Текст
                answer = input("Ответ: ").strip()
                while not answer:
                    print("⚠️  Ответ не может быть пустым!")
                    answer = input("Ответ: ").strip()
            
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
            
            # ИСПРАВЛЕНО: Единый формат вывода
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
                        q_to_edit["answer"] = new_answer
                        print("✅ Ответ обновлен")
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
            
            # ИСПРАВЛЕНО: Правильный формат вопроса в BB-коде
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
        import datetime
        
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
    
    def main_menu(self):
        """Главное меню"""
        while True:
            self.clear_screen()
            self.print_title("ГЕНЕРАТОР ФОРМ ДЛЯ BLACKRUSSIA")
            
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
            print("  4. 🚪 ВЫХОД")
            
            choice = input("\nВаш выбор (1-4): ").strip()
            
            if choice == "1":
                self.run_workflow()
            
            elif choice == "2":
                self.show_example()
            
            elif choice == "3":
                self.show_designs()
            
            elif choice == "4":
                print("\n👋 До свидания!")
                break
            
            else:
                print("❌ Неверный выбор!")
                input("\n↵ Нажмите Enter чтобы продолжить...")
    
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