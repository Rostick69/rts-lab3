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


def print_gantt(tasks, timeline):
    """Печатает диаграмму: строка на задачу, █ - задача выполняется, · - не выполняется."""
    ordered = rms_order(tasks)
    interval = len(timeline)
    name_w = max(len("Время, мс"), max(len(t.name) for t in tasks))

    # шкала времени: подпись каждые 5 мс
    scale = "".join(f"{time:<{CELL * 5}}" for time in range(0, interval + 1, 5))
    print(f"{'Время, мс':<{name_w}} {scale}")

    for t in ordered:
        row = ""
        for time in range(interval):
            row += "█" * CELL if timeline[time] == t.name else "·" + " " * (CELL - 1)
        print(f"{t.name:<{name_w}} {row}")

    idle = timeline.count(None)
    print(f"Простой процессора: {idle} из {interval} мс")


def save_gantt_png(tasks, timeline, path):
    """Сохраняет диаграмму картинкой (нужна библиотека matplotlib, она не обязательна)."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib не установлен - картинка диаграммы не сохранена")
        return

    ordered = rms_order(tasks)
    fig, ax = plt.subplots(figsize=(10, 0.8 * len(ordered) + 1.2))
    for row, t in enumerate(reversed(ordered)):
        # соседние миллисекунды одной задачи склеиваем в один отрезок (начало, длина)
        segments = []
        for time, name in enumerate(timeline):
            if name != t.name:
                continue
            if segments and segments[-1][0] + segments[-1][1] == time:
                segments[-1] = (segments[-1][0], segments[-1][1] + 1)
            else:
                segments.append((time, 1))
        ax.broken_barh(segments, (row - 0.35, 0.7), color="tab:blue", edgecolor="black")
        # стрелки - моменты выхода новых заданий задачи
        for release in range(0, len(timeline), t.T):
            ax.annotate("", xy=(release, row + 0.35), xytext=(release, row + 0.6),
                        arrowprops=dict(arrowstyle="->", color="red"))

    ax.set_yticks(range(len(ordered)))
    ax.set_yticklabels([t.name for t in reversed(ordered)])
    ax.set_xlim(0, len(timeline))
    ax.set_ylim(-0.6, len(ordered) - 0.2)
    ax.set_xticks(range(0, len(timeline) + 1))
    ax.set_xlabel("Время, мс")
    ax.grid(axis="x", linestyle=":")
    ax.set_axisbelow(True)  # сетка под полосами, а не поверх
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Диаграмма сохранена в файл {path}")