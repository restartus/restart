"""Setuptools info for the model pip package.

Not yet tested
"""
# https://micropyramid.com/blog/publishing-python-modules-with-pip-via-pypi/
import setuptools  # type:ignore # noqa:

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="restart",
    version="2.5.0.6",
    # this script doesn't exist
    # scripts=["model"],
    author="Restart Partners",
    author_email="lucas@restart.us",  # need a valid email here
    description="COVID-19 decision model tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/restartus/restart",
    packages=setuptools.find_packages(include=["restart"]),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
