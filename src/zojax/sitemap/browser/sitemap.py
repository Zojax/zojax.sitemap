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
from zope.app.component.hooks import getSite
from zope.traversing.browser.absoluteurl import absoluteURL
from zojax.content.type.interfaces import IItem, IContentContainer
from zope.schema.interfaces import IIterable
"""

$Id$
"""
from zope.security import checkPermission
from zope import interface, component

from zojax.sitemap.interfaces import _, ISitemap


class SitemapView(object):

    def update(self):
        self.sitemap = component.getMultiAdapter((self.context, self.request), ISitemap)
        
        
class BaseSitemap(object):
    
    component.adapts(interface.Interface, interface.Interface)
    interface.implements(ISitemap)
    
    def __init__(self, context, request):
        self.context, self.request = context, request
        
    @property
    def items(self):
        return self._getItems()
    
    def _getItems(self, context = None):
        if context is None:
            context = getSite()
        container = IContentContainer(context, None)
        if container is not None:
            for value in container.values():
                if checkPermission('zope.View', value):
                    item = IItem(value, None)
                    if item is not None:
                        yield {'title': item.title,
                               'url': absoluteURL(item, self.request),
                               'items': self._getItems(value)}