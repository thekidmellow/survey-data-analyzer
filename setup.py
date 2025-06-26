from setuptools import setup, find_packages

setup(
    name="survey_data_analyzer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "Flask>=3.0.0",
        "pandas>=2.0.0",
        "matplotlib>=3.0.0"
    ],
    python_requires=">=3.8",
)