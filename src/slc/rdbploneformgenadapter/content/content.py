from collective.lead.interfaces import IDatabase
from plone.app.content.item import Item
from Products.PloneFormGen.config import FORM_ERROR_MARKER
from Products.PloneFormGen.interfaces import IPloneFormGenActionAdapter
from slc.rdbploneformgenadapter import SlcMessageFactory as _
from slc.rdbploneformgenadapter.interfaces import \
    IRDBPloneFormGenAdapterContent
from sqlalchemy.exc import ProgrammingError
from zope.component import getUtility, ComponentLookupError
from zope.component.factory import Factory
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty


class RDBPloneFormGenAdapterContent(Item):
    """The content item that must be added to have an RDB Action available.
    Also stores configuration.
    """
    implements(IRDBPloneFormGenAdapterContent, IPloneFormGenActionAdapter)
    portal_type = "RDBPloneFormGenAdapter"

    query = FieldProperty(IRDBPloneFormGenAdapterContent['query'])
    db_utility_name = FieldProperty(
        IRDBPloneFormGenAdapterContent['db_utility_name'])

    def _getProperty(self):
        return _("RDB Action Adapter")

    def _setProperty(self, new_title):
        pass
    title = property(_getProperty, _setProperty)

    def _constructQueryData(self, fields, form_table_name, REQUEST):
        """Parses form fields and prepares data for saving into the database.

        :param fields: form fields
        :param form_table_name: name of the table used for the form
        :param REQUEST: request object
        :returns: A list of tuples that contain two elements:
            @tuple[0] is the name of the SQL table to save the data in
            @tuple[1] is either a dict, or a list of dicts (for data grid
                fields) with the values needed to execute the query
        """
        query_data = [(form_table_name, {})]
        query_args = query_data[0][1]

        for field in fields:
            field_id = field.id.replace('-', '_')

            # handle file fields
            if field.isFileField():
                field_name = field.fgField.getName()
                file_upload = REQUEST.form.get(
                    '{0}_file'.format(field_name.replace('-', '_')))
                query_args[field_id + '_file'] = buffer(
                    file_upload.blob.open().read())

            # handle datagrid fields
            elif field.portal_type == "FormDataGridField":
                field_name = form_table_name + '_' + field_id
                grid_list = []
                for row in REQUEST.form.get(field.id, ''):
                    # ignore form metadata
                    if row.get('orderindex_', '') != 'template_row_marker':
                        item = dict(row)
                        for key, value in item.iteritems():
                            item[key] = item[key].decode('utf8')
                            item[key.replace('-', '_')] = item.pop(key)
                        del item['orderindex_']
                        # check for duplicates
                        if(item not in grid_list):
                            grid_list.append(item)
                query_data.append((field_name, grid_list))

            # handle all other fields
            else:
                query_args[field_id] = REQUEST.form.get(
                    field.id, '').decode('utf8')

        return query_data

    def onSuccess(self, fields, REQUEST=None):
        """Save the data from the form into a relational database.

        It works in the following way: if a query is defined on the adapter,
        it will use that query to insert the data into the database. If no
        query is defined, it will try to automatically save all form fields.
        "Normal" fields will be saved into the primary table, while every
        FormDataGridField field will be saved into a separate table.

        For this to work, your database and tables have to be created and set
        up according to the following rules:
          - Name of the primary table for storing the form data is same as
            the id of the form (with '-' changed to '_')
          - All "auxiliary" tables for FormDataGridField fields are named in
            the convention of form_table_name + _ + FormDataGridField.id.
            Also, each auxiliary table must have a form_table_name_id column,
            which is a foreign key.
          - All table colums must be named after form field id's (with '-'
            changed to '_')

        :param fields: form fields
        :param REQUEST: request object
        """
        def concatenate(attributes, colon=False):
            """Helper function for constructing SQL queries."""

            # TODO think about setting column names manually
            s = '('
            if(colon):
                s += ':'
                tmp = ', :'.join(attributes)
            else:
                tmp = ', '.join(attributes)
            s += tmp + ')'
            return(s)

        try:
            db = getUtility(IDatabase, self.db_utility_name)
        except ComponentLookupError:
            return {
                FORM_ERROR_MARKER: _(
                    'Can not write to database, wrong configuration. Please '
                    'contact site owner.'
                )
            }

        form_table_name = self.getParentNode().id.replace('-', '_')
        query_args = self._constructQueryData(
            fields, form_table_name, REQUEST)
        query = self.query

        try:
            if(query):
                # custom query was defined on the adapter, let's use that
                db.connection.engine.execute(query, **query_args[0][1])
            else:
                # no query was defined, store all form fields
                select_string = "SELECT MAX(ID) FROM {0}".format(
                    form_table_name)
                form_id = (db.connection.engine.execute(
                    select_string).scalar() or 0) + 1

                for field in query_args:
                    table_name = field[0]

                    # handle FormDataGridField fields
                    if(type(field[1]) == list):
                        for item in field[1][:]:
                            # Setting grid table name, based on the form name
                            item[form_table_name + "_id"] = form_id
                            attributes = item.keys()
                            query_string = \
                                "INSERT INTO {0} {1} VALUES {2}".format(
                                    table_name,
                                    concatenate(attributes),
                                    concatenate(attributes, colon=True)
                                )
                            db.connection.engine.execute(
                                query_string, **item)
                    else:
                        attributes = field[1].keys()
                        query_string = \
                            "INSERT INTO {0} {1} VALUES {2}".format(
                                table_name,
                                concatenate(attributes),
                                concatenate(attributes, colon=True)
                            )
                        db.connection.engine.execute(
                            query_string, **field[1])
        except ProgrammingError, e:
            return {
                FORM_ERROR_MARKER: _(
                    'Can not write to database, wrong '
                    'configuration. Please contact site owner.') + str(e)
            }


RDBPloneFormGenAdapterFactory = Factory(
    RDBPloneFormGenAdapterContent,
    title=_('Add RDB Action Configuration')
)
