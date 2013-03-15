from setuptools import setup, find_packages
from xml.dom.minidom import parse
import sys, os

mdfile = os.path.join(os.path.dirname(__file__), 'src', 'slc', 
                      'rdbploneformgenadapter', 'profiles', 'default', 
                      'metadata.xml')

metadata = parse(mdfile)
version = metadata.getElementsByTagName('version')[0].childNodes[0].data
shortdesc = metadata.getElementsByTagName('description')[0].childNodes[0].data

setup(name='slc.rdbploneformgenadapter',
      version=version,
      description=shortdesc,
      long_description=open('README.txt').read() + '\n' + 
                       "Change history\n"
                       "**************\n" + 
                       open('CHANGES.txt').read() + '\n' +
                       "Future features, mabye\n"
                       "**********************\n" + 
                       open('TODO.txt').read() + '\n',
#                       "Contributors.txt\n"
#                       "****************\n" + 
#                       open('CONTRIBUTORS.txt').read()
      classifiers=[
        "Framework :: Plone",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Syslab.com GmbH',
      author_email='info@syslab.com',
      url='http://products.syslab.com/products.slc.rdbploneformgenadapter',
      license='GPL',
      packages=['slc', 'slc/rdbploneformgenadapter'],
      package_dir = {'' : 'src'},
      namespace_packages = ['slc'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        "collective.lead",
        "Products.PloneFormGen",
        'setuptools',
        'Plone',
      ],
      extras_require=dict(test=[
        'Products.PloneTestCase',
        'PIL',
        ]),
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
