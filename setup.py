import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open(".github/VERSION", "r") as fh:
    app_version = fh.read()

setuptools.setup(
    name="alphatools_jv",
    version=app_version,
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
