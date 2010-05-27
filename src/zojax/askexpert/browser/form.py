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
from zope import interface, event
from zope.security.proxy import removeSecurityProxy
from zope.cachedescriptors.property import Lazy
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.component.hooks import getSite
from zope.traversing.browser import absoluteURL

from z3c.form import group

from zojax.content.type.interfaces import IOrder
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.layoutform import button, Fields, PageletForm, PageletDisplayForm
from zojax.persistent.fields.interfaces import IField

from zojax.askexpert.interfaces import _, IGroup, FormSubmittedEvent


class Form(group.GroupForm, PageletForm):

    confirm = False
    ignoreContext = True
    formErrorsMessage = _('There were some errors.')
    confirmTemplate = ViewPageTemplateFile('confirm.pt')
    site_url = None

    @property
    def label(self):
        return self.context.title

    @property
    def description(self):
        if self.context.body is not None:
            return self.context.body.cooked

    @Lazy
    def fields(self):
        form = self.context
        order = IOrder(form)

        groupFields = []
        for grp in order.values():
            if IGroup.providedBy(grp):
                for fieldId in grp.fields:
                    field = form.get(fieldId)
                    if IField.providedBy(field):
                        groupFields.append(fieldId)

        fields = []
        for field in order.values():
            if IField.providedBy(field) and field.__name__ not in groupFields:
                fields.append(field)
        return Fields(*fields)

    @Lazy
    def groups(self):
        form = self.context

        groups = []
        for grp in self.context.values():
            if IGroup.providedBy(grp):
                fields = []
                for fieldId in grp.fields:
                    field = form.get(fieldId)
                    if IField.providedBy(field):
                        fields.append(field)
                fields = Fields(*fields)

                grpCls = type(str(grp.__name__), (group.Group,),
                              {'label': grp.title,
                               'description': grp.description, 'fields': fields})
                groups.append(grpCls)
        return groups

    def render(self):
        if self.confirm:
            return self.confirmTemplate()
        else:
            return super(Form, self).render()

    @button.buttonAndHandler(_(u'Submit'), name='submit')
    def handleSubmit(self, action):
        data, errors = self.extractData()
        if errors:
            IStatusMessage(self.request).add(self.formErrorsMessage, 'warning')
        else:
            removeSecurityProxy(self.context).processData(data, self.request)
            event.notify(FormSubmittedEvent(data))
            IStatusMessage(self.request).add('Request has been processed.')

            if self.context.confirm:
                self.confirm = True

            if self.context.nextURL:
                self.redirect(self.context.nextURL)

    def update(self):
        super(Form, self).update()
        self.site_url = '%s/'%absoluteURL(getSite(), self.request)

def getSubmitTitle(adapter):
    if adapter.form.context.submitLabel is not None and adapter.form.context.submitLabel:
        return adapter.form.context.submitLabel
    return adapter.widget.label

ApplyLabel = button.ComputedButtonActionAttribute(getSubmitTitle, button=Form.buttons['submit'])


class grpClass(group.Group):

    def getContent(self):
        return self.__parent__.getContent()


class DisplayForm(group.GroupForm, PageletDisplayForm):

    @property
    def label(self):
        return self.context.title

    @Lazy
    def fields(self):
        form = self.context
        order = IOrder(form)

        groupFields = []
        for grp in order.values():
            if IGroup.providedBy(grp):
                for fieldId in grp.fields:
                    field = form.get(fieldId)
                    if IField.providedBy(field):
                        groupFields.append(fieldId)

        fields = []
        for field in order.values():
            if IField.providedBy(field) and field.__name__ not in groupFields:
                fields.append(field)
        return Fields(*fields)

    @Lazy
    def groups(self):
        form = self.context

        groups = []
        for grp in self.context.values():
            if IGroup.providedBy(grp):
                fields = []
                for fieldId in grp.fields:
                    field = form.get(fieldId)
                    if IField.providedBy(field):
                        fields.append(field)
                fields = Fields(*fields)

                grpCls = type(str(grp.__name__), (grpClass,),
                              {'label': grp.title,
                               'description': grp.description, 'fields': fields})
                groups.append(grpCls)
        return groups

    def getContent(self):
        return self._context_data

    def update(self):
        self._context_data = data

        return super(DisplayForm, self).update()
