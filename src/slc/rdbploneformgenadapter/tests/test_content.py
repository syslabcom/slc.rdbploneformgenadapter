from base import RDBPloneFormGenAdapterTestCase


class TestContent(RDBPloneFormGenAdapterTestCase):
    def test_contentAdd(self):
        self.setRoles(('Manager', ))
        self.ff.invokeFactory('RDBPloneFormGenAdapter', 'xxx')
        ob = getattr(self.ff, 'id', None)
        self.assertTrue(ob)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestContent))
    return suite
