"""Практическая работа 3 (СРВ). Планирование периодических задач: RMS и EDF.
Вариант 2: бортовая система (датчики, управление, связь).

Запуск: python src/main.py [путь_к_файлу.json]
Без аргумента берётся data/variant2.json.
"""

import sys
from pathlib import Path

from models import load_tasks
from analysis import hyperperiod
from output import print_table, print_conclusion
from gantt import gantt, print_gantt, save_gantt_png

# Путь строим от расположения этого файла, а не от текущей папки,
# поэтому программа находит данные при запуске и из Visual Studio, и из консоли
PROJECT_DIR = Path(__file__).parent.parent
DEFAULT_DATA = PROJECT_DIR / "data" / "variant2.json"


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DATA
    title, tasks = load_tasks(path)

    print(f"Анализ планируемости: {title}\n")
    print_table(tasks)
    print_conclusion(tasks)

    # диаграмма выполнения по RMS на интервале [0, гиперпериод]
    interval = hyperperiod(tasks)
    timeline, misses = gantt(tasks, interval)
    print(f"\nДИАГРАММА ВЫПОЛНЕНИЯ ПО RMS на [0, {interval}] мс")
    print_gantt(tasks, timeline)
    if misses:
        for name, d in misses:
            print(f"Пропуск дедлайна: {name} в момент {d} мс")
    else:
        print("Пропусков дедлайнов на гиперпериоде нет.")

    # картинка диаграммы для отчёта (если установлен matplotlib)
    save_gantt_png(tasks, timeline, PROJECT_DIR / "docs" / f"gantt_{path.stem}.png")


if __name__ == "__main__":
    main()