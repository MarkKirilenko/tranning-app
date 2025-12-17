# client_validation.py
import re
from datetime import datetime

class Validator:
    """Класс для выполнения валидации пользовательского ввода."""
    
    @staticmethod
    def is_valid_phone_by(phone):
        """
        Проверяет номер телефона на соответствие форматам Беларуси (+375 или 80)
        и общему формату (9 цифр после кода).
        """
        # Очищаем строку от всего, кроме цифр и знака '+'
        clean_phone = re.sub(r'[^\d\+]', '', phone)
        
        # Шаблон: начинается с +375 и 9 цифр, ИЛИ начинается с 80 и 9 цифр (для звонков по РБ)
        pattern = re.compile(r'^(?:\+375|80)\d{9}$')
        
        if pattern.match(clean_phone):
            return True
        return False

    @staticmethod
    def is_valid_date(date_str):
        """Проверяет формат даты ГГГГ-ММ-ДД и ее разумность."""
        try:
            # Проверка формата
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            now_date = datetime.now().date()
            
            # Дата не должна быть в будущем
            if date_obj.date() > now_date:
                return False, "Дата рождения не может быть в будущем."
                
            # Дополнительная проверка: возраст должен быть >= 5 лет (разумное ограничение для регистрации)
            if (now_date - date_obj.date()).days < (365 * 5):
                return False, "Минимальный возраст для регистрации — 5 лет."
                
            return True, ""
        except ValueError:
            return False, "Неверный формат даты. Используйте ГГГГ-ММ-ДД."