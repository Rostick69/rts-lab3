"""Анализ планируемости: загрузка, тест Liu & Layland, RMS, EDF, время отклика."""

import math


def utilization(tasks):
    """Коэффициент загрузки процессора U = сумма C/T."""
    return sum(t.C / t.T for t in tasks)


def liu_layland_bound(n):
    """Граница Liu & Layland для n задач: n * (2^(1/n) - 1)."""
    return n * (2 ** (1 / n) - 1)


def rms_order(tasks):
    """Задачи в порядке приоритета RMS: меньший период - выше приоритет."""
    return sorted(tasks, key=lambda t: t.T)


def rms_schedulable(tasks):
    """Утилизационный тест RMS: U <= границы Liu & Layland.

    Тест достаточный: если он пройден - набор точно планируем,
    если нет - ответ даёт только анализ времени отклика.
    """
    return utilization(tasks) <= liu_layland_bound(len(tasks))


def edf_schedulable(tasks):
    """Тест EDF для неявных дедлайнов (D = T): U <= 1 (необходимо и достаточно)."""
    return utilization(tasks) <= 1


def response_time_steps(task, higher):
    """Все шаги рекуррентной формулы R = C + сумма(ceil(R / Tj) * Cj) по задачам выше приоритетом.

    Итерация останавливается, когда R перестаёт меняться (найдено время отклика)
    или когда R превысил дедлайн (задача не успевает, дальше считать нет смысла).
    """
    steps = [task.C]  # начальное приближение R0 = C
    while True:
        r = steps[-1]
        # вмешательство: сколько раз за время r успеют запуститься задачи выше приоритетом
        interference = sum(math.ceil(r / h.T) * h.C for h in higher)
        new_r = task.C + interference
        steps.append(new_r)
        if new_r == r or new_r > task.D:
            return steps


def response_time(task, higher):
    """Время отклика задачи в худшем случае (последний шаг итерации)."""
    return response_time_steps(task, higher)[-1]


def response_times(tasks):
    """Время отклика каждой задачи по RMS: словарь {имя задачи: R}."""
    ordered = rms_order(tasks)
    result = {}
    for i, task in enumerate(ordered):
        higher = ordered[:i]  # все задачи с меньшим периодом
        result[task.name] = response_time(task, higher)
    return result


def hyperperiod(tasks):
    """Гиперпериод - наименьшее общее кратное всех периодов."""
    h = 1
    for t in tasks:
        h = h * t.T // math.gcd(h, t.T)
    return h