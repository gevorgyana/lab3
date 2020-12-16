import setuptools

setuptools.setup(
    name="psycho_orm_frankenstein",
    version="0.0.3",
    author="Artyom Gevorgyan",
    author_email="artemhevorhian@gmail.com",
    description="A toy ORM tool",
    long_description="This package is for interacting with PostgresQL via Python, mapping classes and objects onto the database.",
    long_description_content_type="text/markdown",
    url="https://github.com/gevorgyana/lab3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'psycopg2-binary'
    ]
)
