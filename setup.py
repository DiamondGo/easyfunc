import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easyfunc",
    version="0.2.5.1",
    author="K",
    author_email="mastercoderk@gmail.com",
    description="Easy and simple functional programming style helper for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DiamondGo/easyfunc",
    exclude_package_data={'': ['test_easyfunc.py']},
    packages=setuptools.find_packages(),
    keywords=['fp', 'python', 'functional'],
    classifiers=(
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ),
)
