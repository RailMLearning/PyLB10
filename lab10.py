import math
from typing import Callable
import timeit
import concurrent.futures as ftres
from functools import partial


def integrate(f: Callable[[float], float], a: float, b: float, *, n_iter: int = 100000) -> float:
    """
    Численно вычисляет определённый интеграл функции f(x) на интервале [a, b]
    методом левых прямоугольников.

    Алгоритм:
    - Интервал [a, b] делится на n_iter равных частей.
    - В каждой точке берётся значение функции f(x) в левой границе отрезка.
    - Площадь прямоугольника (f(x) * step) добавляется к сумме.
    - Итоговая сумма приближает значение интеграла.

    Аргументы:
        f (Callable[[float], float]): функция одной переменной, которую нужно проинтегрировать.
        a (float): левая граница интегрирования.
        b (float): правая граница интегрирования.
        n_iter (int, необязательный): количество разбиений интервала (по умолчанию 100000).
            Чем больше значение, тем выше точность, но дольше время вычисления.

    Возвращает:
        float: приближённое значение интеграла функции f(x) на интервале [a, b].

    Ограничения:
        - Метод подходит для непрерывных и достаточно гладких функций.
        - Для функций с резкими скачками или особенностями точность может быть низкой.
        - При слишком малом n_iter результат может сильно отличаться от точного значения.

    Примеры:
        >>> round(integrate(math.sin, 0, math.pi, n_iter=10000), 3)
        2.0

        >>> round(integrate(lambda x: x**2, 0, 1, n_iter=10000), 3)
        0.333
    """
    acc = 0.0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc

def integrate_async(
    f: Callable[[float], float],
    a: float,
    b: float,
    *,
    n_jobs: int = 2,
    n_iter: int = 100000
) -> float:
    """
    Многопоточная версия интегратора.

    Делит интервал [a, b] на n_jobs частей и считает интеграл параллельно
    с использованием ThreadPoolExecutor.

    Args:
        f (Callable[[float], float]): функция одной переменной.
        a (float): левая граница интегрирования.
        b (float): правая граница интегрирования.
        n_jobs (int, optional): количество потоков (по умолчанию 2).
        n_iter (int, optional): количество итераций (по умолчанию 100000).

    Returns:
        float: приближённое значение интеграла.
    """
    executor = ftres.ThreadPoolExecutor(max_workers=n_jobs)
    spawn = partial(executor.submit, integrate, f, n_iter=n_iter // n_jobs)

    step = (b - a) / n_jobs
    futures = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]

    return sum(f.result() for f in ftres.as_completed(futures))

def integrate_async_process(
    f: Callable[[float], float],
    a: float,
    b: float,
    *,
    n_jobs: int = 2,
    n_iter: int = 100000
) -> float:
    """
    Многопроцессная версия интегратора.

    Делит интервал [a, b] на n_jobs частей и считает интеграл параллельно
    с использованием ProcessPoolExecutor.

    Args:
        f (Callable[[float], float]): функция одной переменной.
        a (float): левая граница интегрирования.
        b (float): правая граница интегрирования.
        n_jobs (int, optional): количество процессов (по умолчанию 2).
        n_iter (int, optional): количество итераций (по умолчанию 100000).

    Returns:
        float: приближённое значение интеграла.
    """
    with ftres.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        spawn = partial(integrate, f, n_iter=n_iter // n_jobs)
        step = (b - a) / n_jobs
        futures = [executor.submit(spawn, a + i * step, a + (i + 1) * step) for i in range(n_jobs)]
        return sum(f.result() for f in ftres.as_completed(futures))



integrate(math.cos, 0, math.pi, n_iter=1000)