from setuptools import setup
# python setup.py install
# python setup.py develop
setup(
    name='leyts',
    version='3.7',
    description='the do that done',
    url='https://github.com/khensolomon/leyts',
    author='Khen Solomon Lethil',
    author_email='khensolomon@gmail.com',
    license='MIT',
    packages=[
    ],
    install_requires=[
        'Pillow', 'mutagen','numpy'
    ],
    dependency_links=[
    ],
    zip_safe=False
)