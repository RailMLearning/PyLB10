import math
import timeit

from lab10 import integrate, integrate_async_process


def benchmark_processes():
    n_iter = 100000000
    jobs_list = [2, 4, 6, 8]

    print("| Процессы | Время выполнения (сек) |")
    print("|----------|-------------------------|")

    # базовая функция
    base_time = timeit.timeit(lambda: integrate(math.sin, 0, math.pi, n_iter=n_iter), number=3)
    print(f"| Базовая  | {base_time:.6f}                 |")

    # многопроцессная версия
    for jobs in jobs_list:
        t = timeit.timeit(lambda: integrate_async_process(math.sin, 0, math.pi, n_jobs=jobs, n_iter=n_iter), number=3)
        print(f"| {jobs:<8} | {t:.6f}                 |")


if __name__ == "__main__":
    benchmark_processes()
