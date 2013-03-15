from collective.lead.interfaces import IDatabase
from plone.app.content.item import Item
from Products.PloneFormGen.config import FORM_ERROR_MARKER
from Products.PloneFormGen.interfaces import IPloneFormGenActionAdapter
from sqlalchemy.exceptions import ProgrammingError
from zope.component import getUtility, ComponentLookupError
from zope.component.factory import Factory
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

from slc.rdbploneformgenadapter import SlcMessageFactory as _
from slc.rdbploneformgenadapter.interfaces import IRDBPloneFormGenAdapterContent

class RDBPloneFormGenAdapterContent(Item):
    """
    The content item that must be added to have an RDB Action available.
    Also stores configuration
    """
    implements(IRDBPloneFormGenAdapterContent, IPloneFormGenActionAdapter)
    portal_type = "RDBPloneFormGenAdapter"
    
    query = FieldProperty(IRDBPloneFormGenAdapterContent['query'])
    db_utility_name = FieldProperty(IRDBPloneFormGenAdapterContent['db_utility_name'])

    def _getProperty(self):
        return _("RDB Action Adapter")

    def _setProperty(self, new_title):
        pass
    title = property(_getProperty, _setProperty)

    def onSuccess(self, fields, REQUEST = None):
        try:
            db = getUtility(IDatabase, self.db_utility_name)
        except ComponentLookupError:
            return {FORM_ERROR_MARKER : _('Can not write to database, wrong configuration. Please contact site owner.')}

        execute = db.connection.engine.execute
        
        query = self.query

        query_args = {}
        for field in fields:
            query_args[field.id] = REQUEST.form.get(field.id, '')
        try:
            execute(query, **query_args)
        except ProgrammingError, e:
            return {FORM_ERROR_MARKER : _('Can not write to database, wrong configuration. Please contact site owner.') + str(e)}

RDBPloneFormGenAdapterFactory = Factory(RDBPloneFormGenAdapterContent, \
        title = _('Add RDB Action Configuration'))

