import math
import timeit

def integrate_py(f, a, b, *, n_iter=100000) -> float:
    """
    Численно интегрирует f(x) на [a, b] методом левых прямоугольников.
    Базовая Python-версия для сравнения.
    """
    acc = 0.0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc

def main():
    import integrate as cy  # compiled Cython module
    n_iter = 100_000

    print("| Имплементация        | Время (сек) |")
    print("|----------------------|-------------|")

    t_py = timeit.timeit(lambda: integrate_py(math.sin, 0.0, math.pi, n_iter=n_iter), number=3)
    print(f"| Python (math.sin)    | {t_py:.6f}   |")

    t_cy = timeit.timeit(lambda: cy.integrate_sin(0.0, math.pi, n_iter), number=3)
    print(f"| Cython (C sin)       | {t_cy:.6f}   |")

if __name__ == "__main__":
    main()
