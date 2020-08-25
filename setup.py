from setuptools import setup


setup(
    name="PyPardot4",
    version="1.1.13",
    author="Matt Needham",
    author_email="matthew.m.needham@gmail.com",
	license="MIT",
    description="API wrapper for APIv4 of Pardot marketing automation software.",
    keywords="pardot",
    url="https://github.com/mneedham91/PyPardot4",
    packages=['pypardot', 'pypardot.objects', 'pypardot.objects_v3'],
    install_requires=['requests'],
)
