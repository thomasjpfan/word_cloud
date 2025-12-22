from setuptools import setup, Extension
from Cython.Build import cythonize
import sys

extension_kwargs = {}

if sys.version_info >= (3, 11):
    extension_kwargs["define_macros"] = [
        ("Py_LIMITED_API", 0x030B0000)
    ]
    extension_kwargs["py_limited_api"] = True


setup(ext_modules=cythonize(
    [
        Extension(
            name="wordcloud.query_integral_image",
            sources=["wordcloud/query_integral_image.pyx"],
            **extension_kwargs
        )
    ]
))
