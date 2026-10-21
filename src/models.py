"""Модель периодической задачи и загрузка набора задач из JSON."""

import json
from dataclasses import dataclass


@dataclass
class Task:
    """Периодическая задача. Все времена в миллисекундах."""
    name: str  # название задачи
    C: int     # время выполнения в худшем случае (WCET)
    T: int     # период
    D: int     # относительный дедлайн