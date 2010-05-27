##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface, schema
from zope.i18nmessageid import MessageFactory
from z3c.schema.email import RFC822MailAddress
from z3c.schema.email.interfaces import IRFC822MailAddress
from zojax.richtext.field import RichText
from zojax.content.type.interfaces import IItem, IContent, IContentType

_ = MessageFactory('zojax.askexpert')


class IForm(IItem):
    """ form """

    submitLabel = schema.TextLine(
        title = _(u'Submit label'),
        description = _(u'Form submit button label.'),
        required = False,
        default=_(u'Submit'))

    body = RichText(
        title = _(u'Body text'),
        description = _(u'Form confirmation text.'),
        required = False)

    confirm = RichText(
        title = _(u'Confirm text'),
        description = _(u'Form confirmation text.'),
        required = False)

    nextURL = schema.TextLine(
        title = _(u'Next URL'),
        description = _(u'URL to redirect after submission. Preferably relative.'),
        required = False)


class IGroup(IItem):
    """ fields group """

    fields = schema.List(
        title = _(u'Fields'),
        description = _(u'Group list'),
        value_type = schema.Choice(vocabulary='zojax.askexpert-formFields'),
        required = True)


class IGroupType(interface.Interface):
    """ group content type """


class IFormDataStorageType(interface.Interface):
    """ data storage type """

class IPortletFormView(interface.Interface):
    """ portlet form view """

class IFormDataStorage(interface.Interface):
    """ data storage """

    count = interface.Attribute('Records count')

    def append(form, record, request):
        """ append record to storage """


class IMailDataStorage(IFormDataStorage):
    """ send result of form to defined email """

    emailto = RFC822MailAddress(
        title = u'Email',
        description = u'Destination email',
        required = True)

    fromname = schema.TextLine(
        title = u'From name',
        required = False)

    fromaddr = RFC822MailAddress(
        title = u'From email address',
        required = True)


class IFormSubmittedEvent(interface.Interface):
    """ form submission event """

    data = interface.Attribute('Submitted data')


class FormSubmittedEvent(object):
    interface.implements(IFormSubmittedEvent)

    def __init__(self, data):
        self.data = data
