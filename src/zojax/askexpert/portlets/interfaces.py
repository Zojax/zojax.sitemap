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

from zojax.askexpert.interfaces import _


class IFormPortlet(interface.Interface):
    """ Form portlet """

    label = schema.TextLine(
        title = _(u'Label'),
        required = False)

    submitLabel = schema.TextLine(
        title = _(u'Submit label'),
        description = _(u'Form submit button label.'),
        required = False,
        default=_(u'Submit'))

    redirectToForm = schema.Bool(
        title = _(u'Redirect to real form'),
        required = True,
        default = True)

    form = schema.Choice(title= _(u'Ask expert Form'),
                         vocabulary="zojax.askexpert.forms",
                         required=False)

    formObject = interface.Attribute('formObject')

    fields = schema.List(
        title = _(u'Fields'),
        description = _(u'Fields list'),
        value_type = schema.Choice(vocabulary='zojax.askexpert-portletFormFields'),
        required = True,
        default = [])
