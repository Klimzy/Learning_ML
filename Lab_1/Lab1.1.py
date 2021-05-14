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

Q = 76          # количество поколений
MAX_ENT = 150   # размер популяции
MAX_CH = 60     # количество циклов скрещивания
N = 9           # длина хромосомы
MUTATION_PROBABILITY = 0.5  # вероятность мутации


def ds_to_gray(chromosome):
    return '{:09b}'.format(graycode.tc_to_gray_code(chromosome))


def gray_to_ds(chromosome):
    return graycode.gray_code_to_tc(int(chromosome, 2))


def fitness(chromosome):
    y = (0.8 * math.cos(3 * chromosome) + math.cos(chromosome)) * (chromosome - 4)

    return round(y, 4)


def tournament_for_max(first_gladiator, second_gladiator):
    first_gladiator = gray_to_ds(first_gladiator) * sampling_step
    second_gladiator = gray_to_ds(second_gladiator) * sampling_step

    if fitness(first_gladiator) >= fitness(second_gladiator):
        return ds_to_gray(int(first_gladiator / sampling_step))
    else:
        return ds_to_gray(int(second_gladiator / sampling_step))


def tournament_for_min(first_gladiator, second_gladiator):
    first_gladiator = gray_to_ds(first_gladiator) * sampling_step
    second_gladiator = gray_to_ds(second_gladiator) * sampling_step

    if fitness(first_gladiator) <= fitness(second_gladiator):
        return ds_to_gray(int(first_gladiator / sampling_step))
    else:
        return ds_to_gray(int(second_gladiator / sampling_step))


def mutation(chromosome):
    # Проверка, что хромосома состоит не из одних нулей или единиц
    if graycode.gray_code_to_tc(int(chromosome, 2)) == 0 or graycode.gray_code_to_tc(int(chromosome, 2)) == 1:
        return chromosome

    chromosome = list(chromosome)

    # Рандомный поиск неодинаковых номеров локусов и различных локусов. Обмен битами

    for _ in range(0, 10):
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
sampling_step = round(35 / 2 ** N, 3)
print("Шаг дискреизации = ", sampling_step)
discrete_values = [round(i * sampling_step, 5) for i in range(0, 2 ** N)]  # все дискретные значения

entity_for_min = []  # Начальное поколение для минимума
entity_for_max = []  # Начальное покаоление для максимума

for i in range(MAX_ENT):  # генерация начальной популяции
    entity_for_min.append(discrete_values[random.randint(0, 2 ** N - 1)])
    entity_for_max.append(discrete_values[random.randint(0, 2 ** N - 1)])

# кодирование номера хромосомы кодом Грея
entity_for_min = [int(entity_for_min[i] / sampling_step) for i in range(0, MAX_ENT)]
entity_for_max = [int(entity_for_max[i] / sampling_step) for i in range(0, MAX_ENT)]

entity_for_min = [ds_to_gray(entity_for_min[i]) for i in range(0, MAX_ENT)]
entity_for_max = [ds_to_gray(entity_for_max[i]) for i in range(0, MAX_ENT)]

# ТУРНИРНЫЙ ОТБОР
tournament_size = 2  # численность турнира

for _ in range(0, Q):
    middle_entity_for_min = [0 for _ in range(0, MAX_ENT)]  # промежуточное поколение для поиска максимума
    middle_entity_for_max = [0 for _ in range(0, MAX_ENT)]  # промежуточное поколение для поиска минимума

    # проведение турнира
    for i in range(MAX_ENT):
        # генерация неодинаковых номеров для выбора хромосом-гладиаторов
        while True:
            k1 = random.randint(0, MAX_ENT - 1)
            k2 = random.randint(0, MAX_ENT - 1)
            if k1 != k2:
                break

        middle_entity_for_min[i] = tournament_for_min(entity_for_min[k1], entity_for_min[k2])
        middle_entity_for_max[i] = tournament_for_max(entity_for_max[k1], entity_for_max[k2])

    entity_for_min = middle_entity_for_min[:]
    entity_for_max = middle_entity_for_max[:]

    # СКРЕЩИВАНИЕ
    parent_flag = [True for _ in range(0, MAX_ENT)]

    k = 0
    child1 = []
    child2 = []
    while k < MAX_CH:
        parent1_num = random.randint(0, MAX_ENT - 1)
        parent2_num = random.randint(0, MAX_ENT - 1)

        if parent1_num == parent2_num:
            continue
        if not parent_flag[parent1_num] & parent_flag[parent2_num]:
            continue

        # ДЛЯ МИНИМУМА
        child1 = list(entity_for_min[parent1_num])
        child2 = list(entity_for_min[parent2_num])

        parent1 = list(entity_for_min[parent1_num])
        parent2 = list(entity_for_min[parent2_num])

        child1[2:7] = parent2[2:7]
        child2[2:7] = parent1[2:7]

        child1 = ''.join(child1)
        child2 = ''.join(child2)

        entity_for_min[parent1_num] = child1
        entity_for_min[parent2_num] = child2

        # ДЛЯ МАКСИМУМА
        child1 = list(entity_for_max[parent1_num])
        child2 = list(entity_for_max[parent2_num])

        parent1 = list(entity_for_max[parent1_num])
        parent2 = list(entity_for_max[parent2_num])

        child1[2:7] = parent2[2:7]
        child2[2:7] = parent1[2:7]

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

        for i in range(0, 10):
            num_of_mutating_individual = random.randint(0, MAX_ENT - 1)  # номер мутирующей хромосомы в поколении

            entity_for_min[num_of_mutating_individual] = mutation(entity_for_min[num_of_mutating_individual])

            entity_for_max[num_of_mutating_individual] = mutation(entity_for_max[num_of_mutating_individual])



entity_for_min = [graycode.gray_code_to_tc(int(entity_for_min[i], 2)) * sampling_step for i in
                      range(0, MAX_ENT)]
entity_for_max = [graycode.gray_code_to_tc(int(entity_for_max[i], 2)) * sampling_step for i in
                      range(0, MAX_ENT)]

print('48.7 -54.8')
functoin_min = min(fitness(entity_for_min[i]) for i in range(0, MAX_ENT))
function_max = max(fitness(entity_for_max[i]) for i in range(0, MAX_ENT))
print("Функция f(x) имеет минимальное значение на отрезке [0; 35] равное ", functoin_min)
print("Функция f(x) имеет максимальное значение на отрезке [0; 35] равное ", function_max)
