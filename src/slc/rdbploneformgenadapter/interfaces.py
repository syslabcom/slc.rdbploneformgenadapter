from plone.app.discussion.interfaces import IDiscussionLayer
from slc.rdbploneformgenadapter import SlcMessageFactory as _
from zope.interface import Interface
from zope import schema


class IRDBPloneFormGenAdapterContent(Interface):

    db_utility_name = schema.TextLine(
        title=_('Database utility name'),
        description=_('The name of the utility that provides '
                      'collective.lead.interfaces.IDatabase'),
        required=True
    )

    query = schema.Text(
        title=_(u'Insert query'),
        description=_(u'The query that will be performed to insert all '
                      'data. If no query is provided, all fields will be '
                      'saved (except the ones listed under "Form fields to '
                      'exclude"'),
        required=False
    )

    exclude_fields = schema.List(
        title=_('Form fields to exclude'),
        description=_("List ids of fields which you don't want to save to "
                      "the database."),
        value_type=schema.TextLine(),
        required=False
    )


class IRDBPloneFormGenAdapterLayer(IDiscussionLayer):
    """Custom browser layer for this package"""
