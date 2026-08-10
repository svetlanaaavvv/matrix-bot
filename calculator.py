# calculator.py
# Методика расчёта Матрицы Судьбы с сайта gadalkindom.ru
# Все формулы строго по буквенной модели

def to_archan(num):
    """
    Приводит число к диапазону 1-22
    Если число больше 22, складывает цифры до получения числа <= 22
    """
    while num > 22:
        num = sum(int(digit) for digit in str(num))
    return num if num != 0 else 22


def calculate_matrix(birth_date: str):
    """
    Рассчитывает Матрицу Судьбы по дате рождения
    Формулы взяты с сайта gadalkindom.ru
    """
    try:
        # Парсим дату рождения
        day, month, year = map(int, birth_date.split('.'))

        # === БАЗОВЫЕ ЧИСЛА (из даты рождения) ===
        A = to_archan(day)          # Характер
        B = to_archan(month)        # Карма
        C = to_archan(sum(int(d) for d in str(year)))  # Деньги
        D = to_archan(A + B + C)    # Отношения

        # === ЛИЧНЫЙ (ДИАГОНАЛЬНЫЙ) КВАДРАТ ===
        E = to_archan(A + B + C + D)  # Зона комфорта (центр личного квадрата)

        # Точки на диагоналях личного квадрата
        J = to_archan(A + E)
        K = to_archan(B + E)
        L = to_archan(C + E)
        M = to_archan(D + E)

        # Остальные точки личного квадрата
        O = to_archan(A + J)
        P = to_archan(B + K)
        Q = to_archan(C + L)
        N = to_archan(D + M)

        S = to_archan(J + E)
        T = to_archan(K + E)

        # === РОДОВОЙ (ПРЯМОЙ) КВАДРАТ ===
        # Грани родового квадрата
        F = to_archan(A + B)
        G = to_archan(B + C)
        H = to_archan(C + D)
        I = to_archan(D + A)

        # L2 — центр родового квадрата
        L2 = to_archan(F + G + H + I)

        # L1 — центр всей матрицы (ЗОНА КОМФОРТА — она же E в некоторых школах)
        L1 = to_archan(E + L2)

        # Первая группа точек родового квадрата
        F2 = to_archan(F + L2)
        G2 = to_archan(G + L2)
        H2 = to_archan(H + L2)
        I2 = to_archan(I + L2)

        # Вторая группа
        F1 = to_archan(F + F2)
        G1 = to_archan(G + G2)
        H1 = to_archan(H + H2)
        I1 = to_archan(I + I2)

        # Третья группа (для отношений и финансов)
        R = to_archan(M + L)
        R1 = to_archan(R + M)
        R2 = to_archan(R + L)

        # === ПРЕДНАЗНАЧЕНИЯ ===
        # Личное предназначение: (A+C) + (B+D)
        personal_purpose = to_archan((A + C) + (B + D))

        # Социальное предназначение: (F+H) + (G+I)
        social_purpose = to_archan((F + H) + (G + I))

        # Духовное предназначение: личное + социальное
        spiritual_purpose = to_archan(personal_purpose + social_purpose)

        # === ОТВЕТ БОТА ===
        return {
            # Основные позиции (для вывода в боте)
            "character": A,          # Характер (число дня)
            "karma": B,              # Карма (число месяца)
            "money": C,              # Денежный канал (сумма цифр года)
            "love": D,               # Отношения (A+B+C)
            "comfort": L1,           # Зона комфорта (центр матрицы)

            # Дополнительные точки (для расширенных функций)
            "E": E,
            "J": J, "K": K, "L": L, "M": M,
            "O": O, "P": P, "Q": Q, "N": N,
            "S": S, "T": T,
            "F": F, "G": G, "H": H, "I": I,
            "L2": L2,
            "F2": F2, "G2": G2, "H2": H2, "I2": I2,
            "F1": F1, "G1": G1, "H1": H1, "I1": I1,
            "R": R, "R1": R1, "R2": R2,
            "personal_purpose": personal_purpose,
            "social_purpose": social_purpose,
            "spiritual_purpose": spiritual_purpose,
        }

    except Exception as e:
        print(f"❌ Ошибка расчёта матрицы: {e}")
        return None


# === ТЕСТ ДЛЯ ПРОВЕРКИ ===
if __name__ == "__main__":
    # Тест для даты 11.01.2004
    result = calculate_matrix("11.01.2004")
    if result:
        print("🔮 МАТРИЦА СУДЬБЫ ДЛЯ 11.01.2004:")
        print(f"  🌟 Характер: {result['character']} Аркан")
        print(f"  🔮 Карма: {result['karma']} Аркан")
        print(f"  💰 Деньги: {result['money']} Аркан")
        print(f"  ❤️ Отношения: {result['love']} Аркан")
        print(f"  🛋 Зона комфорта: {result['comfort']} Аркан")

    # Тест для даты 21.05.2005
    result2 = calculate_matrix("21.05.2005")
    if result2:
        print("\n🔮 МАТРИЦА СУДЬБЫ ДЛЯ 21.05.2005:")
        print(f"  🌟 Характер: {result2['character']} Аркан")
        print(f"  🔮 Карма: {result2['karma']} Аркан")
        print(f"  💰 Деньги: {result2['money']} Аркан")
        print(f"  ❤️ Отношения: {result2['love']} Аркан")
        print(f"  🛋 Зона комфорта: {result2['comfort']} Аркан")