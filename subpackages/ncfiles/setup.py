from setuptools import setup

setup(
    name="ncfiles",
    version="0.0",
    py_modules=["ncfiles"],
    package_dir={"": "../../src"},
    install_requires=["netCDF4"],
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