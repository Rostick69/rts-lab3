"""Анализ планируемости: загрузка, тест Liu & Layland, RMS, EDF, время отклика."""

import math


def utilization(tasks):
    """Коэффициент загрузки процессора U = сумма C/T."""
    return sum(t.C / t.T for t in tasks)


def liu_layland_bound(n):
    """Граница Liu & Layland для n задач: n * (2^(1/n) - 1)."""
    return n * (2 ** (1 / n) - 1)