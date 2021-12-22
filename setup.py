import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

with open("requirements/requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="rss_reader",
    version="1.2",
    description="RSS feed reader",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/SergeiPapina/rss_reader",
    author="Siarhei_Papina",
    author_email="Siarhei_Papina@epam.com",
    classifiers=["Programming Language :: Python :: 3"],
    # packages=find_packages(where="rss_reader", exclude=["tests"]),
    packages=["rss_reader"],
    install_requires=required,
    include_package_data=True,
    #python_requires=">=3.9",
    #package_dir={"": "rss_reader"},
    entry_points={
        "console_scripts": [
            "rss_reader=rss_reader.__main__:main"
        ]
    }
)