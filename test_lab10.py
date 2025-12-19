import unittest
import math
from lab10 import integrate   # предполагаем, что твоя функция лежит в файле lab10.py


class TestIntegrate(unittest.TestCase):

    def test_sin_integral(self):
        # ∫₀^π sin(x) dx = 2
        result = integrate(math.sin, 0, math.pi, n_iter=10000)
        self.assertAlmostEqual(result, 2.0, places=3)

    def test_cos_integral(self):
        # ∫₀^π cos(x) dx = 0
        result = integrate(math.cos, 0, math.pi, n_iter=10000)
        self.assertAlmostEqual(result, 0.0, places=3)

    def test_polynomial_integral(self):
        # ∫₀^1 x^2 dx = 1/3 ≈ 0.333...
        result = integrate(lambda x: x**2, 0, 1, n_iter=10000)
        self.assertAlmostEqual(result, 1/3, places=3)

    def test_accuracy_with_iterations(self):
        # Проверка устойчивости к изменению числа итераций
        result_low = integrate(math.sin, 0, math.pi, n_iter=1000)
        result_high = integrate(math.sin, 0, math.pi, n_iter=100000)
        # Оба результата должны быть близки к 2
        self.assertAlmostEqual(result_low, 2.0, places=2)
        self.assertAlmostEqual(result_high, 2.0, places=4)


if __name__ == '__main__':
    unittest.main()
