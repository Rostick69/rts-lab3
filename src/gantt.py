"""Моделирование выполнения задач по RMS и временная диаграмма (диаграмма Ганта)."""

from analysis import rms_order

CELL = 2  # ширина одной миллисекунды в консольной диаграмме (символов)


def gantt(tasks, interval):
    """Пошагово (по 1 мс) моделирует RMS с вытеснением на отрезке [0, interval).

    Возвращает (timeline, misses):
      timeline - список длины interval, в каждой ячейке имя задачи или None (простой);
      misses   - список пропусков дедлайна (имя задачи, момент дедлайна).
    """
    ordered = rms_order(tasks)                  # порядок приоритетов RMS
    remaining = {t.name: 0 for t in tasks}      # сколько осталось выполнять текущему заданию
    deadline = {t.name: 0 for t in tasks}       # абсолютный дедлайн текущего задания
    timeline = []
    misses = []

    for time in range(interval):
        for t in ordered:
            # задание не успело к своему дедлайну - фиксируем пропуск
            if remaining[t.name] > 0 and time >= deadline[t.name]:
                misses.append((t.name, deadline[t.name]))
                remaining[t.name] = 0
            # в начале каждого периода выходит новое задание задачи
            if time % t.T == 0:
                remaining[t.name] = t.C
                deadline[t.name] = time + t.D

        # выполняется готовая задача с наивысшим приоритетом (вытесняя остальные)
        running = None
        for t in ordered:
            if remaining[t.name] > 0:
                running = t.name
                remaining[t.name] -= 1
                break
        timeline.append(running)

    # задания, которые не закончились к дедлайну на последнем шаге интервала
    for t in ordered:
        if remaining[t.name] > 0 and deadline[t.name] <= interval:
            misses.append((t.name, deadline[t.name]))

    return timeline, misses