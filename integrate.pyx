# integrate.pyx
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: language_level=3

from libc.math cimport sin

# Внутренняя нативная функция, которую можно вызывать без GIL
cdef double _integrate_sin_nogil(double a, double b, int n_iter) nogil:
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x
    for i in range(n_iter):
        x = a + i * step
        acc += sin(x) * step
    return acc

# Внешняя функция для Python, которая отпускает GIL внутри вычисления
cpdef double integrate_sin_nogil(double a, double b, int n_iter=100000):
    with nogil:
        return _integrate_sin_nogil(a, b, n_iter)

# Оставь и обычную однопоточную версию (для сравнения)
cpdef double integrate_sin(double a, double b, int n_iter=100000):
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x
    for i in range(n_iter):
        x = a + i * step
        acc += sin(x) * step
    return acc
