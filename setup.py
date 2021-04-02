import os
import sys
import pathlib

from setuptools import setup, find_packages
from setuptools.command.install import install

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# circleci.py version
VERSION = "0.3.0"

class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)

setup(
    name="curl2swift",
    version=VERSION,
    description="Tool for transforming cURL to Swift code.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tomnvt/curl2swift",
    author="Tom Novotny",
    author_email="tom.novota@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(include=["curl2swift", "curl2swift.*"]),
    include_package_data=True,
    install_requires=["Pygments", "requests", "pyp3rclip", "gitpython"],
    entry_points={
        "console_scripts": [
            "curl2swift=curl2swift.__main__:main",
        ]
    },    
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)