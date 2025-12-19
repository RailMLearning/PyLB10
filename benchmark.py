import math
import timeit
from typing import Callable

def integrate(f: Callable[[float], float], a: float, b: float, *, n_iter: int = 100000) -> float:
    acc = 0.0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc

n_values = [10**3, 10**4, 10**5]

results = []
for n in n_values:
    t = timeit.timeit(lambda: integrate(math.sin, 0, math.pi, n_iter=n), number=3)
    results.append((n, t))

print("| n_iter | Время выполнения (сек) |")
print("|--------|-------------------------|")
for n, t in results:
    print(f"| {n:<6} | {t:.6f}                 |")

