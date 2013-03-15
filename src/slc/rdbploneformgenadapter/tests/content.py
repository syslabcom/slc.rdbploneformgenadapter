from base import RDBPloneFormGenAdapterTestCase


class TestContent(RDBPloneFormGenAdapterTestCase):
    def test_bla(self):
        self.assertTrue(False)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestContent))
    return suite
