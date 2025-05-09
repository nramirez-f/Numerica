from setuptools import setup

setup(
    name="initial_conditions",
    version="0.0",
    py_modules=["initial_conditions"],
    package_dir={"": "../../src"},
    install_requires=["numpy"],
    author="Nramirez",
    description="Initial Conditions for Numerical Methods",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nramirez-f/Numerica",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)