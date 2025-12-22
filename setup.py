from setuptools import setup, Extension
from Cython.Build import cythonize
import sys

extension_kwargs = {}
options = {}

is_gil_enabled = hasattr(sys, "_is_gil_enabled") and sys._is_gil_enabled()

if sys.version_info >= (3, 11) and not is_gil_enabled:
    extension_kwargs["define_macros"] = [
        ("Py_LIMITED_API", 0x030B0000)
    ]
    extension_kwargs["py_limited_api"] = True
    options["bdist_wheel"] = {"py_limited_api": "cp311"}


setup(ext_modules=cythonize(
    [
        Extension(
            name="wordcloud.query_integral_image",
            sources=["wordcloud/query_integral_image.pyx"],
            **extension_kwargs
        )
    ],
    options=options
))
