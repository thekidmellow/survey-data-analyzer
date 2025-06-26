from setuptools import setup, find_packages

setup(
    name="survey_data_analyzer",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # List dependencies here if you want, or keep empty if using requirements.txt
    ],
    python_requires=">=3.8",
)