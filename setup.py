import os

from setuptools import find_packages, setup

VERSION = "2.0.5"
HERE = os.path.abspath(os.path.dirname(__file__))


reqs_path = HERE + "/requirements.txt"
with open(reqs_path, encoding="utf-8") as reqs_file:
    reqs = reqs_file.read().splitlines()


with open("README.md", encoding="utf-8") as f:
    README = f.read()


setup(
    name="judge-pics",
    description="Database of Judge Pictures",
    long_description=README,
    long_description_content_type="text/markdown",
    version=VERSION,
    author="Mike Lissner",
    author_email="info@free.law",
    maintainer="Mike Lisser",
    maintainer_email="info@free.law",
    packages=find_packages(exclude=["tests", "judge_pics.data.orig"]),
    include_package_data=True,
    package_data={
        "judge_pics": [
            "data/people.json",
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    test_suite="tests",
    install_requires=reqs,
)
