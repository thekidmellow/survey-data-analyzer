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

# Package configuration
setup(
    # Basic package information
    name="survey-data-analyzer",
    version="1.0.0",
    author="[Your Name]",
    author_email="your.email@example.com",
    
    # Package description
    description="A comprehensive Python command-line application for analyzing survey data",
    long_description=read_readme(),
    long_description_content_type="text/markdown",    

    # Project URLs
    url="https://github.com/[your-username]/survey-data-analyzer",
    project_urls={
        "Bug Tracker": "https://github.com/[your-username]/survey-data-analyzer/issues",
        "Documentation": "https://github.com/[your-username]/survey-data-analyzer#readme",
        "Source Code": "https://github.com/[your-username]/survey-data-analyzer",
    },

    # Package discovery and structure
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    # Dependencies
    install_requires=read_requirements(),
    
    # Python version requirement
    python_requires=">=3.8, <3.13",

    # Package classification
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    
    # Keywords for package discovery
    keywords="survey data analysis statistics research cli",

    # Entry points for command-line interface
    entry_points={
        "console_scripts": [
            "survey-analyzer=main:main",
        ],
    },

    # Additional package data
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.rst"],
    },
    
    # Development dependencies (optional)
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "isort>=5.10.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    
    # Zip safety
    zip_safe=False,
)