from distutils.core import setup

setup(
    name='API_Client',
    packages=[''],
    version='1.0',
    license='GNU',
    description='API Client, which automatically authenticates and refreshes',
    author='tj0vtj0v',
    author_email='BurdorfTjorven@gmail.com',
    url='https://github.com/tj0vtj0v/API_Client',
    download_url='https://github.com/tj0vtj0v/API_Client/archive/refs/tags/Beta.tar.gz',
    keywords=['Connector', 'REST', 'CRUD', 'Private'],
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
