from setuptools import setup, find_packages

setup(
	name = 'latexgrammar',
	version = '3.0',
	author = 'Local Ghost',
	description = 'antlr4 support for LaTeX',
	license = 'MIT',
	keywords = 'antlr4 grammar LaTeX',
	packages = find_packages(),
	install_requires = ['antlr4-python3-runtime==4.7.2']
)