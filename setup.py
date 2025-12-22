from setuptools import setup, Extension
from Cython.Build import cythonize
import sys

is_gil_enabled = hasattr(sys, "_is_gil_enabled") and sys._is_gil_enabled()
enable_abi3 = sys.version_info >= (3, 11) and is_gil_enabled


setup(ext_modules=cythonize(
    [
        Extension(
            name="wordcloud.query_integral_image",
            sources=["wordcloud/query_integral_image.pyx"],
            define_macros=[("Py_LIMITED_API", 0x030B0000) ] if enable_abi3 else [],
            py_limited_api=enable_abi3
        )
    ],
),
    options={"bdist_wheel": {"py_limited_api": "cp311"}} if enable_abi3 else {},
)
