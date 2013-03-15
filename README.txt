.. contents::

.. Note!
   -----

   - code repository
   - bug tracker
   - questions/comments feedback mail

- Code repository: http://svn.plone.org/svn/collective/slc.rdbploneformgenadapter
- Questions and comments to info (at) syslab (dot) com
- Report bugs at http://plone.org/products/slc.rdbploneformgenadapter

Detailed Documentation
**********************

RDB Action Adapter for PloneFormGen
===================================

The Action Adapter can be used to store form submissions of PloneFormGen
forms into a relations database. 

Dependencies
------------

The Action Adapter users the IDatabase Utility from collective.lead
to write data to the database. You must provide such an IDatabase Utility.

Configuration
-------------

After you installed the Action Adapter in the Plone Control Panel, you can
start adding The Action Adapter to PloneFormGen forms.

The Action Adapter Configuration Screen contains two parameters:
 
Insert query
    The query to insert data. We do not use the SQLAlchemy mapping features,
    but write data directly into the database. The fields from the form
    are added as a dictionary to the execute statement. See pep-0249
    for formatting strings. As we pass a dict, you must use positional
    arguments. in PEP 249 they are called paramstyle named and pyformat
    An Example looks like this::

        insert into test_questions (replyto, topic, comments) values(%(replyto)s, %(topic)s, %(comments)s);

    or::
        
        insert into test_questions (replyto, topic, comments) values(:replyto, :topic, :comments);

Databae utility Name
    The name of the IDatabase Utility that you must configure


