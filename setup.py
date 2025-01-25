import platform
from setuptools import setup, Extension
from wheel.bdist_wheel import bdist_wheel
import sys
from Cython.Build import cythonize

# With memoryview, Limited ABI is only available in 3.11
min_python_abi = (3, 11)
newer_than_min_python = sys.version_info[:2] >= min_python_abi
is_cpython = platform.python_implementation() == "CPython"
if hasattr(sys, "_is_gil_enabled") and not sys._is_gil_enabled():
    is_gil_enabled = False
else:
    is_gil_enabled = True

use_abi3 = newer_than_min_python and is_cpython and is_gil_enabled


if use_abi3:
    py_limited_api = True
    define_macros = [
        ("Py_LIMITED_API", "0x030b00f0"),
        ("CYTHON_LIMITED_API", "1"),
    ]
else:
    py_limited_api = False
    define_macros = []


class bdist_wheel_abi3(bdist_wheel):
    def get_tag(self):
        python, abi, plat = super().get_tag()
        if use_abi3:
            min_python_str = "".join(str(v) for v in min_python_abi)
            return f"cp{min_python_str}", "abi3", plat
        return python, abi, plat


extensions = [
    Extension(
        "wordcloud.query_integral_image",
        sources=["wordcloud/query_integral_image.pyx"],
        py_limited_api=py_limited_api,
        define_macros=define_macros,
    )
]


setup(
    ext_modules=cythonize(extensions),
    cmdclass={"bdist_wheel": bdist_wheel_abi3},
)
