import graycode
import random
import math


print()
print("(0,8*cos(3*x) + cos(x))*(x-4)")
print("Критерий останова: Выполнение алгоритмом априорно заданного числа итераций без улучшения целевой функции")
print("Селекция: Турнирная")
print("Виды скрещивания: Двухточечное")
print("Виды мутаций: Перестановка случайных битов местами")





Q = 50          # количество поколений
MAX_ENT = 10    # размер популяции
MAX_CH = 10     # количество детей в одном цинкле вспроизводства
N = 8           # длина хромосомы

values=[random.randint(1,10) for _ in range(N)]
print(values)
weights=[random.randint(1,10) for _ in range(N)]
print(weights)

fit_q = [[0 for _ in range(MAX_ENT)] for _ in range(Q)]  # лучший из поколения

def fitness(inp): # inp – входной список из нулей и единиц
    y =0.0;
    al=1
    bet=1
    for i in range(N):
        if inp[i]==1:
            y = 0.8 * math.cos(3 * x)

    return y

# Начальное поколение
entity=[[random.randint(0,1) for j in range(N)] for i in range(MAX_ENT)]

for q in range(Q):     # цикл поколений

    # Считаем fitness для каждого организма
    fit = [0 for _ in range(MAX_ENT)]
    for i in range(MAX_ENT):
        fit[i] = fitness(entity[i])
    print('fit = ', max(fit))
    # Запомнили лучшего в поколении
    fit_q[q][:] = sorted(fit[:], reverse=True)

    # Воспроизводство

    fl_parent = [True for _ in range(MAX_ENT)]  #до цикла воспроизводства все могут быть родителями

    child1 = [0 for _ in range(N)]
    child2 = [0 for _ in range(N)]

    k=0
    while (k < MAX_CH):         # цикл воспроизводства 2*MAX_CH потомков
        m1=random.randint(0,MAX_ENT-1)   # первый кандидат родитель
        m2=random.randint(0,MAX_ENT-1)   # второй кандидат родитель
        #print(k,m1,m2)
        if (m1 == m2):
            continue      # должны быть разные
        if not(fl_parent[m1] & fl_parent[m2]):
            continue      # кто-то уже имел потомка
        # построение 2 потомков от m1 и m2
        l=random.randint(3,N-4); # точка обмена хромосом
        child1[:l]=entity[m1][:l] # первый потомок
        child1[l:]=entity[m2][l:]
        child2[:l]=entity[m2][:l] # второй потомок
        child2[l:]=entity[m1][l:]
        #print('Родители {}  {}  Разрыв {}'.format(entity[m1],entity[m2],l))
        #print('Потомки {}  {} '.format(child1,child2))

        ch1=child1[:]
        ch2=child2[:]
        # добавка к массиву организмов двух потомков
        entity.append(ch1)
        entity.append(ch2)

        '''
        for row in entity:
            print(' '.join([str(elem) for elem in row]))
        '''
        fl_parent[m1]=False # больше потомков у особей не будет
        fl_parent[m2]=False # в данном поколении

        k+=1
    #  конец цикла воспроизводства
    #print('Воспроизводство',len(entity))
    '''
    # МУТАЦИИ
    
    p_vm=0.1   # Вероятность мутации гена
    p_m=0.2    # Вероятность победы менее приспособленного
    mut_entity = [0 for _ in range(N)]    #  мутант
    
    for j in range(MAX_ENT+2*MAX_CH): # цикл по всем организмам вместе с потомками
        for k in range(N):   # цикл по всем битам каждого организма
            if(random.random() < p_m):    # инвертирование бита для мутанта
                # print('mut')
                if (entity[j][k] == 1):
                    mut_entity[k] = 0    # tстроим строку генов мутанта для каждого организма
                else:
                    mut_entity[k] = 1
            else:
                mut_entity[k] = entity[j][k]
        #print(' Орг {} '.format(entity[j]))
        #print(' Mut {} '.format(temp)) 
        f1 = fitness(entity[j])   # приспособленность организма
        f2 = fitness(mut_entity)        # приспособленность мутанта
        if (f1 > f2):
            if(random.random() < p_vm):    # останется менее приспособленный
                entity[j]=mut_entity[:]
        else:
            entity[j]=mut_entity[:]       # остается более приспособленный !!!!
        
    # конец мутаций
    '''
    # ЕСТЕСТВЕННЫЙ ОТБОР

    tmp_entity=[]   # врем массив для хранения выживших
    fl_duel = [True for _ in range(MAX_ENT+2*MAX_CH)]   # в начале каждый может участвовать в дуэли

    k=0
    while (k < MAX_ENT):   # цикл по отбору наиболее приспособленных
        m1=random.randint(0,MAX_ENT+2*MAX_CH-1)     # выбор двух организмов
        m2=random.randint(0,MAX_ENT+2*MAX_CH-1)
        #print(k,m1,m2)
        if (m1 == m2):
            continue             # должны быть различны
        if not(fl_duel[m1] & fl_duel[m2]):
            continue             # уже отбирался в пару один или оба
        f1 = fitness(entity[m1])
        f2 = fitness(entity[m2])

        if (f1 > f2):            # первый приспособленнее
            # print(m1, entity[m1])
            tmp_entity.append(entity[m1][:])
            fl_duel[m1] = False
        else:
            #print(m2, entity[m2])
            tmp_entity.append(entity[m2][:])
            fl_duel[m2] = False
        #print('Otbor ',len(tmp_entity))
        k+=1

    entity=tmp_entity[:]
    # конец цикла естественного отбора

# конец цикла количества поколнеий Q

