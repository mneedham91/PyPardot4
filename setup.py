from setuptools import setup


setup(
    name="PyPardot4",
    version="0.2",
    author="Matt Needham",
    author_email="matthew.m.needham@gmail.com",
    description=("API wrapper for APIv4 of Pardot marketing automation software."),
    keywords="pardot",
    url="https://github.com/mneedham91/PyPardot4",
    packages=['pypardot', 'pypardot.objects'],
    install_requires=['requests'],
)
