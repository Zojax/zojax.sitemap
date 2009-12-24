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
from zope import interface, component
from zope.security.proxy import removeSecurityProxy
from zope.cachedescriptors.property import Lazy

from z3c.form import group

from zojax.content.type.interfaces import IOrder
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.layoutform import button, Fields, PageletForm, PageletDisplayForm
from zojax.persistent.fields.interfaces import IField, IRichText

from zojax.askexpert.interfaces import _, IGroup, IForm

from interfaces import IFormResults


class FormResults(object):

    component.adapts(IForm, None)
    interface.implements(IFormResults)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def update(self, record):
        form = self.context
        record = dict(record)
        order = IOrder(form)

        groups = []

        def getFieldData(field, fields):
            fieldId = field.__name__
            if IRichText.providedBy(field):
                fields.append((field.title, record.pop(fieldId).text))
            elif IField.providedBy(field):
                fields.append((field.title, record.pop(fieldId)))

        for grp in order.values():
            if IGroup.providedBy(grp):
                fields = []
                for fieldId in grp.fields:
                    field = form.get(fieldId)
                    getFieldData(field, fields)
                groups.append((grp.title, fields))
        fields = []
        for field in order.values():
            getFieldData(field, fields)
        if fields:
            groups.append((u'', fields))
        self.dictionary = groups
