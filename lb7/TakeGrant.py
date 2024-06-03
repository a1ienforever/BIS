def de_jure_closure(S, O, E):
    # Создаем копию множества ребер для работы
    Etg = set(E)
    changed = True

    # Повторяем, пока добавляются новые ребра
    while changed:
        changed = False
        new_edges = set()

        # Применяем правило take
        for (x, y, t) in Etg:
            if t == 't':
                for (y2, z, α) in Etg:
                    if y == y2 and (x, z, α) not in Etg:
                        new_edges.add((x, z, α))

        # Применяем правило grant
        for (x, y, g) in Etg:
            if g == 'g':
                for (y2, z, α) in Etg:
                    if y == y2 and (x, z, α) not in Etg:
                        new_edges.add((x, z, α))

        # Обновляем множество ребер, если были добавлены новые
        if new_edges:
            Etg.update(new_edges)
            changed = True

    return Etg


def de_facto_closure(S, O, E, F):
    # Определяем правила де-факто
    defacto_rules = {('w', 'spy'), ('w', 'find'), ('r', 'post'), ('r', 'pass')}

    # Получаем де-юре замыкание
    Es_de_jure = de_jure_closure(S, O, E)
    F_new = set(F)

    # Применяем первые два де-факто правила
    for (x, y, α) in Es_de_jure:
        if α in {'w', 'r'}:
            for rule in defacto_rules:
                if α == rule[0] and (x, y, rule[1]) not in F_new:
                    F_new.add((x, y, rule[1]))

    # Инициализируем список ребер и множество вершин
    L = list(F_new)
    N = set()

    # Повторяем, пока список L не пуст
    while L:
        (x, y, α) = L.pop(0)
        N.add(y)
        for z in S:
            for (x2, y2, β) in Es_de_jure:
                if y == x2 and (x, z, β) not in F_new:
                    F_new.add((x, z, β))
                    L.append((x, z, β))

    return F_new


def full_closure(S, O, E, F):
    # Получаем де-юре замыкание
    Etg = de_jure_closure(S, O, E)
    # Получаем де-факто замыкание
    F_new = de_facto_closure(S, O, E, F)
    # Объединяем де-юре и де-факто замыкания
    return Etg.union(F_new)

if __name__ == '__main__':
    # Пример 1
    S1 = {'A', 'B'}
    O1 = {'obj1', 'obj2'}
    E1 = {('A', 'obj1', 't'), ('A', 'obj1', 'g'), ('B', 'obj2', 't')}
    F1 = set()

    # Пример 2
    S2 = {'C', 'D', 'E'}
    O2 = {'obj3', 'obj4'}
    E2 = {('C', 'obj3', 'r'), ('D', 'obj3', 'w'), ('E', 'obj4', 't'), ('C', 'D', 'g')}
    F2 = set()

    # Выполнение замыканий для примера 1
    Etg_closure_1 = de_jure_closure(S1, O1, E1)
    F_closure_1 = de_facto_closure(S1, O1, E1, F1)
    full_closure_result_1 = full_closure(S1, O1, E1, F1)

    # Выполнение замыканий для примера 2
    Etg_closure_2 = de_jure_closure(S2, O2, E2)
    F_closure_2 = de_facto_closure(S2, O2, E2, F2)
    full_closure_result_2 = full_closure(S2, O2, E2, F2)

    # Вывод результатов для примера 1
    print("Пример 1:")
    print("Де-юре замыкание:", Etg_closure_1)
    print("Де-факто замыкание:", F_closure_1)
    print("Полное замыкание:", full_closure_result_1)

    # Вывод результатов для примера 2
    print("\nПример 2:")
    print("Де-юре замыкание:", Etg_closure_2)
    print("Де-факто замыкание:", F_closure_2)
    print("Полное замыкание:", full_closure_result_2)
