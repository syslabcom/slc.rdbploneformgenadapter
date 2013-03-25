"""Base class for integration tests"""
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing import z2

import unittest2 as unittest


class SlcRDBPloneFormGenLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        import plone.app.jquery
        import slc.rdbploneformgenadapter
        self.loadZCML(package=plone.app.jquery)
        self.loadZCML(package=slc.rdbploneformgenadapter)
        z2.installProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        """Set up Plone."""

        # Install into Plone site using portal_setup
        applyProfile(portal, 'slc.rdbploneformgenadapter:default')

        # Login and create a test folder
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Folder', 'folder')

        # Commit so that the test browser sees these objects
        portal.portal_catalog.clearFindAndRebuild()
        import transaction
        transaction.commit()

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'Products.PloneFormGen')


FIXTURE = SlcRDBPloneFormGenLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="SlcRDBPloneFormGenLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="SlcRDBPloneFormGenLayer:Functional")


class RDBPloneFormGenAdapterTestCase(unittest.TestCase):
    """Base class for integration tests."""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.folder = self.portal['folder']
        self.folder.invokeFactory('FormFolder', 'ff')
        self.ff = self.folder.ff
        self.ff.manage_delObjects(['mailer'])
        self.ff.toggleActionActive('mailer')

    def tearDown(self):
        self.folder.manage_delObjects(['ff'])


class RDBPloneFormGenAdapterFunctionalTestCase(unittest.TestCase):
    """Base class for functional integration tests."""
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.folder = self.portal['folder']
        self.folder.invokeFactory('FormFolder', 'ff')
        self.ff = self.folder.ff
        self.ff.manage_delObjects(['mailer'])
        self.ff.toggleActionActive('mailer')

    def getBrowser(self, url):
        """Create an instance of zope.testbrowser."""
        browser = z2.Browser(self.layer['app'])
        # self.layer['portal'].absolute_url()
        browser.open(url + '/login_form')
        browser.getControl(name='__ac_name').value = TEST_USER_NAME
        browser.getControl(name='__ac_password').value = TEST_USER_PASSWORD
        browser.getControl(name='submit').click()
        self.assertIn('You are now logged in', browser.contents)
        return browser
