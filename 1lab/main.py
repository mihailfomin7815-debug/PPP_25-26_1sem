import random


def shuf(n, mas):
    for i in range(n):
        j = random.randint(i, n-1)
        mas[j], mas[i] = mas[i], mas[j]
    return mas


def test (n, iter):
    res = {i + 1: [0] * n for i in range(n)}
    mas = [x for x in range(1, n + 1)]
    for _ in range(iter):
        shuf_mas = shuf(n, mas)
        for pos, num in enumerate(shuf_mas):
            res[num][pos] += 1
    return res


iter = 1000
n = random.randint(5, 15)
res = test (n, iter)
print(f'Массив из {n} чисел:')
for pos in range(0, n):
    print(f'Позиция {pos}:')
    for num, count in enumerate(res[pos + 1]):
        print(f'Число {num + 1}: {count / 1000:.2%}')
