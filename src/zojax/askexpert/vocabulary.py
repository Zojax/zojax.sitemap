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
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.app.intid.interfaces import IIntIds
from zope.app.component.hooks import getSite

from zojax.persistent.fields.interfaces import IField
from zojax.catalog.interfaces import ICatalog

from interfaces import IForm


class Vocabulary(SimpleVocabulary):

    def getTerm(self, value):
        try:
            return self.by_value[value]
        except KeyError:
            return self.by_value[self.by_value.keys()[0]]


class FormFieldsVocabulary(object):
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        form = context
        while not IForm.providedBy(form):
            form = getattr(form, '__parent__', None)
            if form is None:
                return SimpleVocabulary(())

        fields = []
        for name, field in form.items():
            if IField.providedBy(field):
                fields.append((field.title, field.__name__))

        fields.sort()
        return Vocabulary(
            [SimpleTerm(name, name, title) for title, name in fields])

class PortletFormFieldsVocabulary(FormFieldsVocabulary):

    def __call__(self, context):
        if context.form is not None:
            form = component.getUtility(IIntIds).queryObject(context.form)
            if form is not None:
                context = form
        return super(PortletFormFieldsVocabulary, self).__call__(context)

def FormsVocabulary(context):
    forms = (i for i in component.getUtility(ICatalog).searchResults(type={'any_of': ('askexpert.form',)},
                                                                     isDraft={'any_of': (False,)},))
    ids = component.getUtility(IIntIds)
    return SimpleVocabulary(
            [SimpleTerm(ids.getId(x), ids.getId(x), x.title) for x in forms]
        )
