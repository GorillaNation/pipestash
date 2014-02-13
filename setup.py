from distutils.core import setup

setup(
    name='pipestash',
    version='0.1.4',
    author='GorillaNation',
    author_email='noc@evolvemediallc.com',
    packages=['pipestash', 'pipestash.output'],
    scripts=['bin/pipestash'],
    url='https://github.com/GorillaNation/pipestash',
    license='LICENSE.txt',
    description="read from stdin, write events to logstash's redis input",
    long_description=open('README.markdown').read(),
    install_requires=[
        "python-redis",
    ],
)
