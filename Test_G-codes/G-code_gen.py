UP = 'G0 Z10'
DOWN = 'G1 Z-0.5F10'

def G1To(x, y):
    return 'G1 X' + str(x) + 'Y' + str(y) + 'F10'
def G0To(x, y):
    return 'G0 X' + str(x) + 'Y' + str(y)
def fract(file, n, x, y, X, Y):
    if n == 0:
        return
    print(G0To(x + X / 3, y + Y / 3), file = file)
    print(DOWN, file = file)
    print(G1To(x + 2 * X / 3, y + Y / 3), file = file)
    print(G1To(x + 2 * X / 3, y + 2 * Y / 3), file = file)
    print(G1To(x + X / 3, y + 2 * Y / 3), file = file)
    print(G1To(x + X / 3, y + Y / 3), file = file)
    print(UP, file = file)
    for xx in range(3):
        for yy in range(3):
            if not (xx == 1 and yy == 1):
                fract(file, n - 1, x + xx * X / 3, y + yy * Y / 3, X / 3, Y / 3)

FName = input('Введите имя файла для записи --> ')
file = open(FName, 'w')
print('T1M6\nG17\nG0 Z10', file = file)
n = int(input('Введите степень фрактала --> '))
fract(file, n, 10, 10, 10, 10)
print('M30', file = file)
file.close()
