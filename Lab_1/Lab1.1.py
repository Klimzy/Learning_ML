import graycode
import random
import math

print()
print("y = (0,8 * cos(3*x) + cos(x))*(x-4)")
print("Критерий останова: Выполнение алгоритмом априорно заданного числа итераций без улучшения целевой функции")
print("Селекция: Турнирная")
print("Виды скрещивания: Двухточечное")
print("Виды мутаций: Перестановка случайных битов местами")
print('\n\n')

Q = 100  # количество поколений
MAX_ENT = 100  # размер популяции
MAX_CH = 80  # количество детей в одном цинкле вспроизводства
N = 9  # длина хромосомы
MUTATION_PROBABILITY = 0.3  # вероятность мутации

def ds_to_gray(chromosome):
    return '{:09b}'.format(graycode.tc_to_gray_code(int(chromosome / sampling_step)))


def fitness(chromosome):
    y = (0.8 * math.cos(3 * chromosome) + math.cos(chromosome)) * (chromosome - 4)

    return round(y, 4)


def tournament_for_max(first_gladiator, second_gladiator):
    if fitness(first_gladiator) > fitness(second_gladiator):
        return ds_to_gray(first_gladiator)
    else:
        return ds_to_gray(second_gladiator)


def tournament_for_min(first_gladiator, second_gladiator):
    if fitness(first_gladiator) < fitness(second_gladiator):
        return ds_to_gray(first_gladiator)
    else:
        return ds_to_gray(second_gladiator)


def mutation(chromosome):
    # Проверка, что хромосома состоит не из одних нулей или единиц
    if graycode.gray_code_to_tc(int(chromosome, 2)) == 0 or graycode.gray_code_to_tc(int(chromosome, 2)) == 1:
        return chromosome

    chromosome = list(chromosome)

    # Рандомный поиск неодинаковых номеров локусов и различных локусов. Обмен битами

    while True:
        num_of_first_bit = random.randint(0, N - 1)
        num_of_second_bit = random.randint(0, N - 1)

        if num_of_first_bit == num_of_second_bit:
            continue

        if chromosome[num_of_first_bit] == chromosome[num_of_second_bit]:
            continue
        else:
            buffer = chromosome[num_of_first_bit]
            chromosome[num_of_first_bit] = chromosome[num_of_second_bit]
            chromosome[num_of_second_bit] = buffer
            break

    chromosome = ''.join(chromosome)

    return chromosome


# main code

entity_for_min = []  # Начальное поколение для минимума
entity_for_max = []  # Начальное покаоление для максимума
gray_entity_for_min = []  # Поколение, преобразованное в код Грея
gray_entity_for_max = []
value = []  # Приспособленность

sampling_step = round(35 / 2 ** N, 3)
print("Шаг дискреизации = ", sampling_step)
discrete_values = [round(i * sampling_step, 5) for i in range(0, 2 ** N)]  # дискретные значения

for i in range(MAX_ENT):  # генерация начальной популяции
    entity_for_min.append(discrete_values[random.randint(0, 2 ** N - 1)])
    entity_for_max.append(discrete_values[random.randint(0, 2 ** N - 1)])

for i in range(MAX_ENT):  # кодирование номера хромосомы кодом Грея
    gray_entity_for_min.append(ds_to_gray(entity_for_min[i]))
    gray_entity_for_max.append(ds_to_gray(entity_for_max[i]))

print("Рандомная начальная популяция для поиска минимума", entity_for_min)
print("Рандомная начальная популяция для поиска максимума", entity_for_max)
print("Номера хромосом в коде Грея для минимума", gray_entity_for_min)
print("Номера хромосом в коде Грея для максимума", gray_entity_for_max)

# ТУРНИРНЫЙ ОТБОР
middle_entity_for_max = []  # промежуточное поколение для поиска максимума
middle_entity_for_min = []  # промежуточное поколение для поиска минимума
tournament_size = 2  # численность турнира

for _ in range(0, Q):

    # проведение турнира
    for i in range(MAX_ENT):

        # генерация неодинаковых номеров для выбора хромосом-гладиаторов
        for k in range(1, 10):
            k1 = random.randint(0, MAX_ENT - 1)
            k2 = random.randint(0, MAX_ENT - 1)
            if k1 != k2:
                break

        middle_entity_for_min.append(tournament_for_min(entity_for_min[k1], entity_for_min[k2]))
        middle_entity_for_max.append(tournament_for_max(entity_for_max[k1], entity_for_max[k2]))

    # print("Промежуточное поколение после отбора для минимума", middle_entity_for_min)
    # print("Промежуточное поколение после отбора для максимума", middle_entity_for_max)

    # СКРЕЩИВАНИЕ
    parent_flag = [True for _ in range(0, MAX_ENT)]

    k = 0
    child1 = []
    child2 = []
    while k < MAX_ENT / 2:
        parent1_num = random.randint(0, MAX_ENT - 1)
        parent2_num = random.randint(0, MAX_ENT - 1)

        if parent1_num == parent2_num:
            continue
        if not parent_flag[parent1_num] & parent_flag[parent2_num]:
            continue

        # ДЛЯ МИНИМУМА
        child1 = list(middle_entity_for_min[parent1_num])
        child2 = list(middle_entity_for_min[parent2_num])

        parent1 = list(middle_entity_for_min[parent1_num])
        parent2 = list(middle_entity_for_min[parent2_num])

        child1[3:6] = parent2[3:6]
        child2[3:6] = parent1[3:6]

        child1 = ''.join(child1)
        child2 = ''.join(child2)

        entity_for_min[parent1_num] = child1
        entity_for_min[parent2_num] = child2

        # ДЛЯ МАКСИМУМА
        child1 = list(middle_entity_for_max[parent1_num])
        child2 = list(middle_entity_for_max[parent2_num])

        parent1 = list(middle_entity_for_max[parent1_num])
        parent2 = list(middle_entity_for_max[parent2_num])

        child1[3:6] = parent2[3:6]
        child2[3:6] = parent1[3:6]

        child1 = ''.join(child1)
        child2 = ''.join(child2)

        entity_for_max[parent1_num] = child1
        entity_for_max[parent2_num] = child2

        # Сброс флага, чтобы эти особи больше не могли размножаться
        parent_flag[parent1_num] = False
        parent_flag[parent2_num] = False

        k += 1

    # МУТАЦИЯ


    if MUTATION_PROBABILITY > (random.randint(0, 100) / 100):

        for i in range(0, 20):
            num_of_mutating_individual = random.randint(0, MAX_ENT - 1)  # номер мутирующей хромосомы в поколении
            middle_entity_for_min[num_of_mutating_individual] = mutation(middle_entity_for_min[num_of_mutating_individual])
            middle_entity_for_max[num_of_mutating_individual] = mutation(middle_entity_for_max[num_of_mutating_individual])

    entity_for_min = [graycode.gray_code_to_tc(int(middle_entity_for_min[i], 2)) * sampling_step for i in
                      range(0, MAX_ENT)]
    entity_for_max = [graycode.gray_code_to_tc(int(middle_entity_for_min[i], 2)) * sampling_step for i in
                      range(0, MAX_ENT)]

print('48.7 -54.8')
functoin_min = min(fitness(entity_for_min[i]) for i in range(0, MAX_ENT))
function_max = max(fitness(entity_for_max[i]) for i in range(0, MAX_ENT))
print("Функция f(x) имеет минимальное значение на отрезке [0; 35] равное ", functoin_min)
print("Функция f(x) имеет максимальное значение на отрезке [0; 35] равное ", function_max)
