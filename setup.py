from setuptools import setup, find_packages

setup(
	name='givav-scrape',
	version='1.0.0',
	# py_modules=['givav-scrape'],
	packages=find_packages(),
	install_requires=[
		'click',
	],
	entry_points={
		'console_scripts': [ 'givav-scrape = givav.scrape:cli' ],
	},
)