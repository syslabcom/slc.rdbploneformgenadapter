from slc.rdbploneformgenadapter import SlcMessageFactory as _
from zope.interface import Interface
from zope import schema


class IRDBPloneFormGenAdapterContent(Interface):

    query = schema.Text(
        title=_(u'Insert query'),
        description=_(u'The query that will be performed to insert all '
                      'data'),
        required=True
    )

    db_utility_name = schema.TextLine(
        title=_('Database utility name'),
        description=_('The name of the utility that provides '
                      'collective.lead.interfaces.IDatabase'),
        required=True
    )
