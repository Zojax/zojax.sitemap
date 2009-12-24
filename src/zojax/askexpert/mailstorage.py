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
from BTrees.Length import Length
from email.Utils import formataddr

from zope import interface
from zope.component import getUtility, adapts
from zope.component import getMultiAdapter
from zojax.content.type.item import PersistentItem
from zojax.mailtemplate.interfaces import IMailTemplate
from zojax.mail.interfaces import IFromAddress

from interfaces import IMailDataStorage


class MailDataStorage(PersistentItem):
    interface.implements(IMailDataStorage)

    def __init__(self, **kw):
        self.count = Length(0)
        super(MailDataStorage, self).__init__(**kw)

    def append(self, form, record, request):
        mail = getMultiAdapter((form, request), IMailTemplate)
        mail.send((self.emailto,), record=record, storage=self)
        self.count.change(1)
