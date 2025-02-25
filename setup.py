from setuptools import setup, find_packages

setup(
    name="agentnexus",
    version="0.1.0",
    packages=find_packages(where="src"),  
    package_dir={"": "src"},  
    install_requires=[
        "requests",
        "fastapi",
        "uvicorn"
    ],
    entry_points={
        "console_scripts": [
            "framework-api=framework.api:main"
        ]
    },
)
