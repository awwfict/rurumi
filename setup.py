from setuptools import setup, find_packages

version = '0.1 prerelease'

setup(name='rrmis',
    version=version,
    description="перевод англоязычного парсера повторяющихся событий на русский !",
      
    classifiers=[
        'Natural Language :: Русский',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: BSD License'
    ],
    keywords='парсер рекурсия даты события NLP нлп',
    author='Ken Van Haren',
    author_email='kvh@science.io',
    url='http://github.com/awwfict/rurumi',
    license='BSD',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=False,
    install_requires=[
        'parsedatetime',
    ],
    python_requires='>3.6.0',
    )
