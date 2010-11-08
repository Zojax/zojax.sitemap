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

_ = MessageFactory('zojax.sitemap')


class ISitemap(schema.interfaces.IIterable):
    """ sitemap """
    
