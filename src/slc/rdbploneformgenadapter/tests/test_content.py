from base import RDBPloneFormGenAdapterTestCase
from plone.app.testing import setRoles


class TestContent(RDBPloneFormGenAdapterTestCase):
    def test_contentAdd(self):
        self.ff.invokeFactory('RDBPloneFormGenAdapter', 'xxx')
        ob = getattr(self.ff, 'id', None)
        self.assertTrue(ob)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestContent))
    return suite
