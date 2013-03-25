from collective.lead.interfaces import IDatabase
from Products.PloneFormGen.config import FORM_ERROR_MARKER
from sqlalchemy.exc import ProgrammingError
from zope.component import provideUtility, getGlobalSiteManager
from zope.publisher.browser import TestRequest

from base import RDBPloneFormGenAdapterTestCase

FAIL = u'special fail statement'
STMTS = []


class DummyEngine(object):
    def connect(self):
        return DummyConnection()


class DummyTransaction(object):
    def commit(self):
        pass

    def rollback(self):
        pass


class DummyConnection(object):
    engine = DummyEngine()

    def execute(self, stmt, **kwargs):
        if stmt == FAIL:
            raise ProgrammingError('Doh', None, None)
        STMTS.append(stmt)

    def begin(self):
        return DummyTransaction()


class DummyDatabase(object):
    connection = DummyConnection()


class TestContent(RDBPloneFormGenAdapterTestCase):

    def setUp(self):
        provideUtility(DummyDatabase, provides=IDatabase, name='test.database')
        super(TestContent, self).setUp()

    def tearDown(self):
        getGlobalSiteManager().unregisterUtility(
            provided=IDatabase, name='test.database')
        super(TestContent, self).tearDown()

    def test_performAction(self):
        query = u'INSERT INTO NOTHING'
        self.ff.invokeFactory('RDBPloneFormGenAdapter', 'action')
        self.ff.addActionAdapter('action')
        self.ff.action.db_utility_name = u'test.database'
        self.ff.action.query = query
        errors = self.ff.fgvalidate(
            REQUEST=TestRequest(
                form={'replyto': 'info@syslab.com',
                      'topic': 'topic',
                      'comments': 'comments'})
        )
        self.assertFalse(errors)
        self.assertEquals(1, len(STMTS))
        self.assertEquals(query, STMTS[0])

    def test_permActionMissingAdapter(self):
        query = u'INSERT INTO NOTHING'
        self.ff.invokeFactory('RDBPloneFormGenAdapter', 'action')
        self.ff.addActionAdapter('action')
        self.ff.action.db_utility_name = u'invalid'
        self.ff.action.query = query
        errors = self.ff.fgvalidate(
            REQUEST=TestRequest(
                form={'replyto': 'info@syslab.com',
                      'topic': 'topic',
                      'comments': 'comments'})
        )
        self.assertEquals(
            'Can not write to database, wrong configuration. '
            'Please contact site owner.',
            errors[FORM_ERROR_MARKER]
        )

    def test_performActionWithInvalidStatement(self):
        self.ff.invokeFactory('RDBPloneFormGenAdapter', 'action')
        self.ff.addActionAdapter('action')
        self.ff.action.db_utility_name = u'test.database'
        self.ff.action.query = FAIL
        errors = self.ff.fgvalidate(
            REQUEST=TestRequest(
                form={'replyto': 'info@syslab.com',
                      'topic': 'topic',
                      'comments': 'comments'}))
        self.assertEquals(
            u"Can not write to database, wrong configuration. "
            "Please contact site owner.",
            errors[FORM_ERROR_MARKER]
        )
        self.assertEquals(1, len(STMTS))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestContent))
    return suite
