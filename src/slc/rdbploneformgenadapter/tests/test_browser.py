from Products.Five.testbrowser import Browser
from Products.PloneTestCase.setup import portal_owner, default_password

import base
import unittest


def getBrowser(url):
    browser = Browser()
    browser.open(url)
    browser.getControl(name='__ac_name').value = portal_owner
    browser.getControl(name='__ac_password').value = default_password
    browser.getControl(name='submit').click()
    return browser


class BrowserTests(base.RDBPloneFormGenAdapterFunctionalTestCase):

    def setUp(self):
        super(BrowserTests, self).setUp()
        self.portal_url = self.portal.absolute_url()
        self.browser = self.getBrowser(self.portal.folder.ff.absolute_url())

    def tearDown(self):
        self.folder.manage_delObjects(['ff'])

    def test_addView(self):
        self.assertTrue('RDBPloneFormGenAdapter' in self.browser.contents)
        self.browser.getLink('RDBPloneFormGenAdapter').click()
        self.assertTrue('Add Action Provider Configuration' in
                        self.browser.contents)

    def test_editView(self):
        test_msg = "This is an invalid query"
        self.browser.getLink('RDBPloneFormGenAdapter').click()
        self.browser.getControl(name='form.query').value = test_msg
        self.browser.getControl(name='form.db_utility_name').value = test_msg
        self.browser.getControl("Save").click()
        self.browser.getLink('Edit').click()
        self.assertTrue('Edit Action Provider Configuration' in
                        self.browser.contents)
        self.assertTrue(test_msg in self.browser.contents)
        self.browser.getControl(name='form.query').value = test_msg + test_msg
        self.browser.getControl("Save").click()
        self.assertTrue(test_msg + test_msg in self.browser.contents)

    def test_viewView(self):
        test_msg = "This is an invalid query"
        self.browser.getLink('RDBPloneFormGenAdapter').click()
        self.browser.getControl(name='form.query').value = test_msg
        self.browser.getControl(name='form.db_utility_name').value = test_msg
        self.browser.getControl("Save").click()
        self.assertTrue('View Action Provider Configuration' in
                        self.browser.contents)
        self.assertTrue(test_msg in self.browser.contents)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BrowserTests))
    return suite
