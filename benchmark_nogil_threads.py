import math
import timeit
from concurrent.futures import ThreadPoolExecutor, as_completed
import integrate as cy

def integrate_py(f, a, b, n_iter=100000):
    acc = 0.0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc

def integrate_nogil_threads(a, b, n_iter, n_jobs):
    step = (b - a) / n_jobs
    per_iter = n_iter // n_jobs
    with ThreadPoolExecutor(max_workers=n_jobs) as ex:
        futs = [
            ex.submit(cy.integrate_sin_nogil, a + i * step, a + (i + 1) * step, per_iter)
            for i in range(n_jobs)
        ]
        return sum(f.result() for f in as_completed(futs))

def run():
    # Выбирай нагрузку не меньше 1e6 для заметной параллелизации
    n_iter = 2_000_000
    jobs = [2, 4, 6]

    print("| Имплементация                 | Время (сек) |")
    print("|-------------------------------|-------------|")

    t_py = timeit.timeit(lambda: integrate_py(math.sin, 0.0, math.pi, n_iter), number=3)
    print(f"| Python (math.sin)             | {t_py:.6f}   |")

    t_cy_single = timeit.timeit(lambda: cy.integrate_sin(0.0, math.pi, n_iter), number=3)
    print(f"| Cython (1 поток, GIL)         | {t_cy_single:.6f}   |")

    t_cy_nogil_single = timeit.timeit(lambda: cy.integrate_sin_nogil(0.0, math.pi, n_iter), number=3)
    print(f"| Cython (1 поток, noGIL)       | {t_cy_nogil_single:.6f}   |")

    for n in jobs:
        t_threads = timeit.timeit(lambda: integrate_nogil_threads(0.0, math.pi, n_iter, n), number=3)
        print(f"| Cython (noGIL, {n} потоков)    | {t_threads:.6f}   |")

if __name__ == "__main__":
    run()