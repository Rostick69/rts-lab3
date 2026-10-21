"""Вывод таблицы задач и заключения о планируемости в консоль."""

from analysis import rms_order, response_times


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