from setuptools import setup

setup(
    name="ncviewer",
    version="0.0",
    packages=["numerica.ncviewer"],
    package_dir={"numerica.ncviewer": "../../src/numerica/ncviewer"},
    install_requires=[
        "xarray",
        "plotly"],
    author="Nramirez",
    description="Module to save simulations within a NetCDF file",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nramirez-f/Numerica",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
