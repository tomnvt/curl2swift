import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="curl2swift",
    version="0.0.1",
    description="Tool for converting cURL to Swift code",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="Tom Novotny",
    author_email="tom.novota@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["curl2swift"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "curl2swift=curl2swift.__main__:main",
        ]
    },
)