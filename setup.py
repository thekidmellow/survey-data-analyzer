from setuptools import setup, find_packages

setup(
    name='survey_data_analyzer',
    version='0.1.0',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[],  # or leave empty and use requirements.txt
    entry_points={
        "console_scripts": [
            "analyze=main:main",  # if main.py has a main() function
        ]
    },
)

