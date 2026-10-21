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