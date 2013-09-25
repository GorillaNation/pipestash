from distutils.core import setup

setup(
    name='pipestash',
    version='0.1.0',
    author='GorillaNation',
    author_email='jeremy.kitchen@gorillanation.com',
    packages=['pipestash', 'pipestash.output'],
    scripts=['bin/pipestash'],
    url='https://github.com/GorillaNation/pipestash',
    license='LICENSE.txt',
    description="read from stdin, write events to logstash's redis input",
    long_description=open('README.markdown').read(),
    install_requires=[
        "redis",
    ],
)
