from setuptools import setup

setup(
    name='webotron-sb',
    version='0.1',
    author='SB',
    description='Webotron automates deploying a static website to AWS S3',
    packages=['webotron'],
    url='https://github.com/sbreevoort/automating-aws-python',
    install_requires=[
        'boto3',
        'click'
    ],
    entry_points='''
        [console_scripts]
        webotron=webotron.webotron:cli
    '''
)
