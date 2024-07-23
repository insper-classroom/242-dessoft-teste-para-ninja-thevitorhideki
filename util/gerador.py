from random import randint, shuffle


def gera_numeros():
    target = randint(4, 20)

    first = randint(1, target - 1)
    second = randint(1, target - 1)
    third = target - first

    numbers = [first, second, third]
    shuffle(numbers)

    numbers.append(target)

    return numbers
