from setuptools import setup, Extension
from wheel.bdist_wheel import bdist_wheel
import sys
from Cython.Build import cythonize

# Limited ABI is only available in 3.11
use_abi3 = sys.version_info >= (3, 11)

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
        if use_abi3 and python.startswith("cp") and not abi.endswith("t"):
            # on CPython, our wheels are abi3 and compatible back to 3.11
            return "cp311", "abi3", plat

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
