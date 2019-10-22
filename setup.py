from setuptools import setup, find_packages


if __name__ == '__main__':
    setup(
        name='mysite',
        version='1.0',
        author='axju',
        author_email='axel.juraske@short-report.de',
        packages=find_packages(),
        install_requires=[
            'django',
        ],
        entry_points={
            'console_scripts': [
                'mysite=mysite.__main__:main',
            ],
        },
    )
