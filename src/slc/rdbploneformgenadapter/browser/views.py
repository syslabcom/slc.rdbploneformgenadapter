from plone.app.form import base
from slc.rdbploneformgenadapter import SlcMessageFactory as _
from slc.rdbploneformgenadapter.content.content import \
    RDBPloneFormGenAdapterContent
from slc.rdbploneformgenadapter.interfaces import \
    IRDBPloneFormGenAdapterContent
from zope.formlib import form

try:
    from Products.Five.formlib.formbase import DisplayFormBase
except:  # Plone 4
    from five.formlib.formbase import DisplayFormBase


class AddForm(base.AddForm):
    """Add form for ActionProvider"""

    form_fields = form.fields(IRDBPloneFormGenAdapterContent)
    label = _(u'Add Action Provider Configuration')

    def create(self, data):
        adapter = RDBPloneFormGenAdapterContent()
        form.applyChanges(adapter, self.form_fields, data)
        return adapter


class EditForm(base.EditForm):
    """Edit Form for ActionProvider"""

    form_fields = form.fields(IRDBPloneFormGenAdapterContent)
    label = _(u'Edit Action Provider Configuration')


class ViewForm(DisplayFormBase):
    """View Form for ActionProvider"""

    form_fields = form.fields(IRDBPloneFormGenAdapterContent)
    label = _(u'View Action Provider Configuration')
