def R_to_A(roman):
    R = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    res = 0
    for i in range(len(roman)):
        if i < len(roman) - 1 and R[roman[i]] < R[roman[i + 1]]:
            res -= R[roman[i]]
        else:
            res += R[roman[i]]
    return res


def A_to_R(num):
    A = ((1, 'I'), (4,'IV'), (5, 'V'), (9, 'IX'), (10, 'X'), (40, 'XL'), (50, 'L'),
         (90, 'XC'), (100, 'C'), (400, 'CD'), (500, 'D'), (900,'CM'), (1000, 'M'))
    res = ''
    for arab, roman in A[::-1]:
        while num >= arab:
            res += roman
            num -= arab
    return res


def correct_R(num):
    R = ('I', 'V', 'X', 'L', 'C', 'D', 'M')
    for i in num:
        if i not in R:
            return False
    return True


def calc():
    while True:
        user_input = input('Введите выражение (для выхода введите STOP) : ')
        if user_input == 'STOP':
            print('Калькулятор выключен')
            break
        parts = user_input.split()
        if len(parts) != 3:
            print('Некорректный ввод. Ввод должен удовлетворять формату "ЧИСЛО ОПЕРАЦИЯ ЧИСЛО"', 'Пример: VI - II', sep = '\n')
            continue
        a,oper,b = parts
        if oper not in '+-/*' or not(correct_R(a)) or not(correct_R(b)) :
            if oper not in '+-/*':
                print('Доступны только операции +, -, /, *')
                continue
            if not (correct_R(a)) or not(correct_R(b)):
                print('Введены некорректные римские числа', 'Пример: VI - II', sep = '\n')
                continue
        a, b = R_to_A(a), R_to_A(b)
        res = 0
        if oper == '+':
            res = a + b
        elif oper == '-':
            if a - b < 0:
                print('Результат вычитания не должен быть отрицательным')
                continue
            else:
                res = a - b
        elif oper == '/' :
            res = a // b
        else:
            res = a * b
        print('Результат:', A_to_R(res))
calc()
