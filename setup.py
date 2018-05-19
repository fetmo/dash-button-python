try:
    # Try using ez_setup to install setuptools if not already installed.
    from ez_setup import use_setuptools

    use_setuptools()
except ImportError:
    # Ignore import error and assume Python 3 which already has setuptools.
    pass

from setuptools import setup, find_packages

classifiers = ['Development Status :: 3 - Alpha',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

setup(name='DashButtonShopware',
      version='0.1',
      author='Moritz Jung',
      author_email='moritz.jung@outlook.de',
      description='Python Application for connecting an RPi to Showpare',
      license='MIT',
      classifiers=classifiers,
      url='https://github.com/fetmo/dash-button-goes-shopware/',
      dependency_links=['https://github.com/adafruit/Adafruit_Python_GPIO/tarball/master#egg=Adafruit-GPIO-0.6.5'],
      install_requires=['Adafruit_SSD1306>=1.6.0', 'Adafruit-GPIO>=0.6.5', 'Pillow', 'requests', 'RPi', 'RPi.GPIO'],
      packages=find_packages())
