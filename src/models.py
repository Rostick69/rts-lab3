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
        tasks.append(task)

    title = data.get("title", "без названия")  # если названия в файле нет, программа не упадёт
    return title, tasks