# setup.py
from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        name="integrate",
        sources=["integrate.pyx"],
        extra_compile_args=["-O3"],
    )
]

setup(
    name="integrate",
    version="0.1.0",
    ext_modules=cythonize(
        extensions,
        annotate=True,          # сгенерирует integrate.html для анализа
        compiler_directives={
            "boundscheck": False,
            "wraparound": False,
            "cdivision": True,
            "language_level": 3,
        },
    ),
)
