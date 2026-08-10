# calculator.py
# Методика расчёта Матрицы Судьбы
# Из книги Елены Прибыловой «Матрица судьбы. Скрытые таланты»

def to_archan(num):
    """
    Приводит число к диапазону 1-22
    По методике Прибыловой: 1-22 не складываем, 23+ складываем
    """
    if num <= 22:
        return num
    while num > 22:
        num = sum(int(digit) for digit in str(num))
    return num


def calculate_matrix(birth_date: str):
    """
    Рассчитывает Матрицу Судьбы по дате рождения
    По методике Елены Прибыловой
    """
    try:
        day, month, year = map(int, birth_date.split('.'))

        # === БАЗОВЫЕ ЧИСЛА ===
        A = to_archan(day)          # Характер
        B = to_archan(month)        # Карма
        C = to_archan(sum(int(d) for d in str(year)))  # Деньги
        D = to_archan(A + B + C)    # Отношения (начало кармического хвоста)
        E = to_archan(A + B + C + D)  # ЗОНА КОМФОРТА

        # === ДИАГОНАЛЬНЫЙ КВАДРАТ ===
        J = to_archan(A + E)
        K = to_archan(B + E)
        L = to_archan(C + E)
        M = to_archan(D + E)
        O = to_archan(A + J)
        P = to_archan(B + K)
        Q = to_archan(C + L)
        N = to_archan(D + M)

        # === РОДОВОЙ КВАДРАТ ===
        F = to_archan(A + B)
        G = to_archan(B + C)
        H = to_archan(C + D)
        I = to_archan(D + A)

        # === КАРМИЧЕСКИЙ ХВОСТ ===
        R = to_archan(M + N)
        S = to_archan(D + R)

        # === ПРЕДНАЗНАЧЕНИЯ ===
        personal_purpose = to_archan((B + D) + (A + C))
        social_purpose = to_archan((F + H) + (G + I))
        spiritual_purpose = to_archan(personal_purpose + social_purpose)

        # === ОТВЕТ ===
        return {
            "character": A,
            "karma": B,
            "money": C,
            "love": D,
            "comfort": E,  # ЗОНА КОМФОРТА

            "A": A, "B": B, "C": C, "D": D, "E": E,
            "J": J, "K": K, "L": L, "M": M,
            "O": O, "P": P, "Q": Q, "N": N,
            "F": F, "G": G, "H": H, "I": I,
            "karmic_tail": [D, R, S],
            "personal_purpose": personal_purpose,
            "social_purpose": social_purpose,
            "spiritual_purpose": spiritual_purpose,
        }

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None


# === ТЕСТ ===
if __name__ == "__main__":
    for date in ["11.01.2004", "21.05.2005"]:
        result = calculate_matrix(date)
        if result:
            print(f"🔮 {date}:")
            print(f"  Характер: {result['character']}")
            print(f"  Карма: {result['karma']}")
            print(f"  Деньги: {result['money']}")
            print(f"  Отношения: {result['love']}")
            print(f"  ЗОНА КОМФОРТА: {result['comfort']}")
            print()