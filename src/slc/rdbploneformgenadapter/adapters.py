from collective.lead.interfaces import IDatabase
from Products.PloneFormGen.config import FORM_ERROR_MARKER
from Products.PloneFormGen.interfaces import IPloneFormGenActionAdapter
from zope.component import adapts, getUtility, ComponentLookupError
from zope.interface import implements

from slc.rdbploneformgenadapter.interfaces import IRDBPloneFormGenAdapterContent

class ActionProvider(object):
    implements(IPloneFormGenActionAdapter)
    adapts(IRDBPloneFormGenAdapterContent)

    def __init__(self, context):
        self.context = context

    def onSuccess(self, fields, REQUEST = None):
        try:
            db = getUtility(IDatabase, self.context.db_utility_name)
        except ComponentLookupError:
            return {FORM_ERROR_MARKER : 'Can not write to database, wrong configuration. Please contact site owner.'}

        execute = db.connection.engine.execute
        
        query = self.context.query

        query_args = {}
        for field in fields:
            query_args[field.id] = REQUEST.form.get(field.id, '')

        execute(query, **query_args)
