from Products.CMFCore.utils import getToolByName
from xml.dom.minidom import parse

import logging
import os
import transaction

log = logging.getLogger('slc.rdbploneformgenadapter.setuphandlers.py')
mdfile = os.path.join(
    os.path.dirname(__file__), 'profiles', 'default', 'metadata.xml')


def isNotSelf(self):
    return self.readDataFile('slc.rdbploneformgenadapter_marker.txt') is None


def installDependencies(self):
    if isNotSelf(self):
        pass

    log.info('install Dependencies')

    site = self.getSite()
    metadata = parse(mdfile)
    dependencies = metadata.getElementsByTagName('dependencies')[0]\
                           .getElementsByTagName('dependency')
    qi = getToolByName(site, 'portal_quickinstaller')
    for dependency in dependencies:
        profile = dependency.childNodes[0].data
        product = str(profile.split('-')[1].split(':')[0])
        if not qi.isProductInstalled(product):
            log.info("Installing dependency: %s" % product)
            qi.installProduct(product)
            transaction.savepoint(optimistic=True)
    transaction.commit()
