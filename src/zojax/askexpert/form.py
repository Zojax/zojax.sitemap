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
from zope import interface
from zope.app.container.ordered import OrderedContainer
from zope.schema.fieldproperty import FieldProperty

from zojax.content.type.item import PersistentItem
from zojax.content.type.container import ContentContainer
from zojax.content.type.interfaces import IContentContainer
from zojax.richtext.field import RichTextProperty

from interfaces import IForm, IGroup, IFormDataStorage


class Form(ContentContainer):
    interface.implements(IForm, IContentContainer)

    confirm = RichTextProperty(IForm['confirm'])
    body = RichTextProperty(IForm['body'])
    submitLabel = FieldProperty(IForm['submitLabel'])


    def processData(self, record, request):
        for value in self.values():
            if IFormDataStorage.providedBy(value):
                value.append(self, record, request)


class Group(PersistentItem):
    interface.implements(IGroup)
