from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys

# Custom install class to add build options for pyaudio
class CustomInstall(install):
    def run(self):
        # Set environment variables or pass options for building pyaudio
        os.environ["CFLAGS"] = "-I/usr/local/include"
        os.environ["LDFLAGS"] = "-L/usr/local/lib"
        
        # Run the original install command
        install.run(self)

# Package setup
setup(
    name='my_project',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scikit-learn',
        'jupyterlab',
        'torch',
        'torchvision',
        'matplotlib',
        'lightning',
        'tensorboard',
        'poetry',
        'mindsdb_sdk',
        'SpeechRecognition',
        'pdfminer.six',
        # 'pyaudio',  # No need for build options here
    ],
    cmdclass={
        'install': CustomInstall,
    },
)