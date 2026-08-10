# calculator.py
from datetime import datetime

def calculate_matrix(birth_date: str):
    """
    Рассчитывает Матрицу Судьбы по дате рождения
    """
    try:
        day, month, year = map(int, birth_date.split('.'))
        
        # Приводим число к 1-22
        def to_archan(num):
            result = num % 22
            return 22 if result == 0 else result
        
        # Характер = число дня рождения
        character = to_archan(day)
        
        # Карма = число месяца
        karma = to_archan(month)
        
        # Деньги = сумма цифр года
        money = to_archan(sum(map(int, str(year))))
        
        # Отношения = сумма дня и месяца
        love = to_archan(day + month)
        
        # Зона комфорта = сумма всех арканов
        comfort = to_archan(character + karma + money + love)
        
        return {
            "character": character,
            "karma": karma,
            "money": money,
            "love": love,
            "comfort": comfort
        }
    except:
        return None