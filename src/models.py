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


def load_tasks(path):
    """Читает файл с набором задач и возвращает (название системы, список задач)."""
    # utf-8-sig читает файл и с BOM, и без него
    # (Visual Studio иногда сохраняет файлы с BOM, и обычный utf-8 на этом падает)
    with open(path, encoding="utf-8-sig") as f:
        data = json.load(f)

    tasks = []
    for item in data["tasks"]:
        task = Task(item["name"], item["C"], item["T"], item["D"])

        # Диаграмма строится с шагом 1 мс, поэтому нужны целые числа
        for value in (task.C, task.T, task.D):
            if not isinstance(value, int) or value <= 0:
                raise ValueError(f"У задачи «{task.name}» C, T и D должны быть целыми и больше нуля")
        # Формула времени отклика в работе используется для дедлайнов D <= T
        if task.D > task.T:
            raise ValueError(f"У задачи «{task.name}» дедлайн больше периода (D > T)")

        tasks.append(task)

    if not tasks:
        raise ValueError("В файле нет ни одной задачи")

    title = data.get("title", "без названия")  # если названия в файле нет, программа не упадёт
    return title, tasks