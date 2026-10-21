"""Вывод таблицы задач и заключения о планируемости в консоль."""

from analysis import (utilization, liu_layland_bound, rms_order, rms_schedulable,
                      edf_schedulable, response_time_steps, response_times, hyperperiod)


def fmt(x):
    """Число без лишних нулей: 0.250 -> 0.25, 0.77976 -> 0.78."""
    return f"{round(x, 3):g}"


def print_table(tasks):
    """Печатает таблицу: Приоритет | Задача | C | T | D | C/T | R | Уложилась."""
    ordered = rms_order(tasks)
    r = response_times(tasks)
    # ширина колонки подстраивается под самое длинное название задачи
    name_w = max(len("Задача"), max(len(t.name) for t in tasks))

    header = (f"{'Пр.':>3} | {'Задача':<{name_w}} | {'C':>3} | {'T':>4} | {'D':>4} | "
              f"{'C/T':>5} | {'R':>4} | Уложилась")
    print(header)
    print("-" * len(header))
    for prio, t in enumerate(ordered, start=1):
        fits = "да" if r[t.name] <= t.D else "НЕТ"
        print(f"{prio:>3} | {t.name:<{name_w}} | {t.C:>3} | {t.T:>4} | {t.D:>4} | "
              f"{fmt(t.C / t.T):>5} | {r[t.name]:>4} | {fits}")
    print("-" * len(header))
    print("Пр. - приоритет RMS (1 - наивысший, меньший период - выше приоритет)")


def print_conclusion(tasks):
    """Печатает загрузку, тест Liu & Layland, анализ времени отклика и вывод по EDF."""
    ordered = rms_order(tasks)
    n = len(tasks)
    u = utilization(tasks)
    bound = liu_layland_bound(n)

    print("\nЗАГРУЗКА ПРОЦЕССОРА")
    parts = " + ".join(fmt(t.C / t.T) for t in ordered)
    print(f"U = {parts} = {fmt(u)}")

    print("\nRMS: УТИЛИЗАЦИОННЫЙ ТЕСТ LIU & LAYLAND")
    print(f"Граница для n = {n}: n·(2^(1/n) - 1) = {fmt(bound)}")
    if rms_schedulable(tasks):
        print(f"U = {fmt(u)} <= {fmt(bound)} - тест пройден, набор планируем по RMS.")
    else:
        print(f"U = {fmt(u)} > {fmt(bound)} - тест не пройден. Тест достаточный, "
              f"поэтому вывод делаем по анализу времени отклика.")

    print("\nRMS: АНАЛИЗ ВРЕМЕНИ ОТКЛИКА")
    all_fit = True
    for i, t in enumerate(ordered):
        steps = response_time_steps(t, ordered[:i])
        r = steps[-1]
        chain = " -> ".join(str(s) for s in steps)
        if r <= t.D:
            print(f"{t.name}: R = {chain}; R = {r} <= D = {t.D} - укладывается")
        else:
            print(f"{t.name}: R = {chain}; R = {r} > D = {t.D} - НЕ укладывается")
            all_fit = False
    if all_fit:
        print("Вывод: все задачи укладываются в дедлайны, набор планируем по RMS.")
    else:
        print("Вывод: есть задачи, не укладывающиеся в дедлайн, набор НЕ планируем по RMS.")

    print("\nEDF")
    if edf_schedulable(tasks):
        print(f"U = {fmt(u)} <= 1 - набор планируем по EDF.")
    else:
        print(f"U = {fmt(u)} > 1 - набор НЕ планируем по EDF (процессор перегружен).")
    if any(t.D < t.T for t in tasks):
        print("Внимание: есть задачи с D < T, условие U <= 1 для них только необходимое.")

    print(f"\nГиперпериод (НОК периодов) = {hyperperiod(tasks)} мс")