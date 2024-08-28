from setuptools import setup, find_packages

setup(
    name='flappy_bird',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pygame',
    ],
    package_data={
        'flappy_bird': ['assets/*.png', 'assets/*.wav'],
    },
    entry_points={
        'console_scripts': [
            'flappy_bird=flappy_bird.game:main',
        ],
    },
    description='A simple Flappy Bird clone made with Pygame',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mustafa',
    author_email='mustafatinwala6@gmail.com',
    url='https://github.com/MUSTAFA892/Flappy-Bird-Pygame',  # Change this to your repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
