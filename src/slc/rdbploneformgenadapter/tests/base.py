"""Base class for integration tests, based on ZopeTestCase and PloneTestCase.

Note that importing this module has various side-effects: it registers a set of
products with Zope, and it sets up a sandbox Plone site with the appropriate
products installed.
"""
from Testing import ZopeTestCase

from Products.Five import zcml
from Products.PloneTestCase import layer
from Products.PloneTestCase.setup import _placefulSetUp, portal_name

SiteLayer = layer.PloneSite

# Let Zope know about the two products we require above-and-beyond a basic
# Plone install (PloneTestCase takes care of these).

# Import PloneTestCase - this registers more products with Zope as
# a side effect
from Products.PloneTestCase.PloneTestCase import PloneTestCase
from Products.PloneTestCase.PloneTestCase import FunctionalTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite


# Set up a Plone site, and apply the membrane and borg extension profiles
# to make sure they are installed.
def startZServer(browser=None):
    ip, port = ZopeTestCase.utils.startZServer()
    if browser:
        return browser.url.replace('nohost', '%s:%i' % (ip, port))


def viewPage(browser):
    file('/tmp/bla.html', 'w').write(browser.contents)
    import webbrowser
    import os
    if not os.fork():
        webbrowser.open('/tmp/bla.html')
        os._exit(0)


def viewError(browser):
    browser.getLink('see the full error message').click()
    file('/tmp/bla.html', 'w').write(browser.contents)
    import webbrowser
    import os
    if not os.fork():
        webbrowser.open('/tmp/bla.html')
        os._exit(0)


class SlcRDBPloneFormGenLayer(SiteLayer):
    @classmethod
    def getPortal(cls):
        app = ZopeTestCase.app()
        portal = app._getOb(portal_name)
        _placefulSetUp(portal)
        return portal

    @classmethod
    def setUp(cls):

        ZopeTestCase.installProduct('PloneFormGen')

        setupPloneSite(
            extension_profiles=(
                'slc.rdbploneformgenadapter:default',
            ), products=(
            ))

        import slc.rdbploneformgenadapter
        zcml.load_config('configure.zcml', slc.rdbploneformgenadapter)

        SiteLayer.setUp()

    @classmethod
    def tearDown(cls):
        pass

    @classmethod
    def testSetUp(cls):
        pass

    @classmethod
    def testTearDown(cls):
        pass


class RDBPloneFormGenAdapterTestCase(PloneTestCase):
    """Base class for integration tests for the 'borg' product. This may
    provide specific set-up and tear-down operations, or provide convenience
    methods.
    """
    layer = SlcRDBPloneFormGenLayer

    def afterSetUp(self):
        self.folder.invokeFactory('FormFolder', 'ff')
        self.ff = self.folder.ff
        self.ff.manage_delObjects(['mailer'])
        self.ff.toggleActionActive('mailer')

    def afterTearDown(self):
        self.folder.manage_delObjects(['ff'])


class RDBPloneFormGenAdapterFunctionalTestCase(FunctionalTestCase):
    """Base class for functional integration tests for the 'borg' product.
    This may provide specific set-up and tear-down operations, or provide
    convenience methods.
    """
    layer = SlcRDBPloneFormGenLayer

    def afterSetUp(self):
        self.folder.invokeFactory('FormFolder', 'ff')
        self.ff = self.folder.ff
        self.ff.manage_delObjects(['mailer'])
        self.ff.toggleActionActive('mailer')

    def afterTearDown(self):
        self.folder.manage_delObjects(['ff'])
