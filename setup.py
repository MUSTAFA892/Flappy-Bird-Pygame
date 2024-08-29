from setuptools import setup, find_packages

setup(
    name='flappy_bird',
    version='0.1',
    description='A simple Flappy Bird clone using Pygame',
    author='Mustafa',
    author_email='mustafatinwala6@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pygame>=2.0.0',
    ],
    entry_points={
        'console_scripts': [
            'flappy_bird=flappy_bird.main:main',  # Replace with your actual entry point if needed
        ],
    },
    include_package_data=True,
    package_data={
        '': ['flappy_bird/assests/*.png'],  # Adjust if necessary to include all relevant files
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
