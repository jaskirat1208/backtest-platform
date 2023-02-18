import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

__version__ = "2.1.1"

setuptools.setup(
    name="alphatools_jv",
    version=__version__,
    author="Jaskirat Singh",
    author_email="jaskiratsingh1208@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jaskirat1208/backtest-platform",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
