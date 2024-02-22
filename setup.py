from setuptools import setup

with open("README.md") as readme_file:
    readme = readme_file.read()


setup(
    name="pageplus-transkribus-utils",
    version="0.1",
    description="""some utility function to interact with the Transkribus-API""",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Jan Kamlah",
    original_author="Peter Andorfer, Matthias Schlögl, Carl Friedrich Haak",
    author_email="jan.kamlah@uni-mannheim.de",
    url="https://github.com/jkamlah/PagePlus-transkribus-utils",
    packages=[
        "transkribus_utils",
    ],
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    keywords="pageplus-transkribus-utils",
)
