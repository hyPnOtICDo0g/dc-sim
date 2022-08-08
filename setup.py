try:
    from setuptools import setup
except ImportError:
    print('`dc-sim` requires \'setuptools\' to continue installation.')
    exit(1)

if __name__ == '__main__':
    setup(
        name = 'dc-sim',
        version = '1.0.0',
        description = 'Simulate popular Data Communication techniques.',
        keywords = 'cli tool communication error detection transmission',
        python_requires = '>=3.7',
        license = 'MIT',
        install_requires = [
            'argparse',
        ],
        packages = [
            'dc_sim',
            'dc_sim.modules',
        ],
        entry_points = {
            'console_scripts': [
                'dc-sim = dc_sim.modules.app:main',
            ]
        },
        classifiers = [
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3 :: Only',
            'Operating System :: OS Independent',
        ],
    )
