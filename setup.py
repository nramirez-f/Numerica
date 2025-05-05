from setuptools import setup

setup(
    name="numerica",
    version="0.0",
    install_requires=[
        "ncviewer @ git+https://github.com/nramirez-f/NcViewer.git@main#egg=ncviewer",
        "fdm @ git+https://github.com/nramirez-f/Finite-Difference.git@main#egg=fdm",
        "initial_conditions @ git+https://github.com/nramirez-f/Initial_Conditions.git@main#egg=initial_conditions",
    ],
    author="Nramirez",
    description="Numerical tools repository",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nramirez-f/Numerica",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)