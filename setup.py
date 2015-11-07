from setuptools import setup


setup(
    name='PyDidYouMean',
    version=__import__('pydidyoumean').__version__,
    url='https://github.com/asweigart/pydidyoumean',
    author='Al Sweigart',
    author_email='al@inventwithpython.com',
    description=('A module to improve "file/command not found" error messages with "did you mean" suggestions.'),
    license='BSD',
    packages=['pydidyoumean'],
    test_suite='tests',
    install_requires=[],
    keywords="didyoumean did you mean suggestions suggest levenshtein",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
)