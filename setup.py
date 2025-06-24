from setuptools import setup, find_packages
import os

def read_readme():

    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()


def read_requirements():

    requirements = []
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            requirements = [line.strip() for line in fh 
                        if line.strip() and not line.startswith("#")]
    return requirements