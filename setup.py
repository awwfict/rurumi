from setuptools import setup, find_packages

version = '0.1.0a1'

setup(name='rrmis',
    version=version,
    description="перевод англоязычного парсера повторяющихся событий !",
      
    classifiers=[
        'Natural Language :: Russian',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: MIT License'
    ],
    keywords='парсер повторяющиеся даты события NLP нлп',
    author='Ken Van Haren',
    author_email='kvh@science.io',
    url='http://github.com/awwfict/rurumi',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=False,
    install_requires=[
        'parsedatetime',
    ],
    python_requires='>3.6.0',
    )
