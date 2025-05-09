from setuptools import setup, find_packages

setup(
    name="numerica",
    version="0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "numpy",
        "scipy",
        "netCDF4",
        "xarray",
        "plotly"
    ],
)