##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
""" zojax.sitemap tests

$Id$
"""
import os, unittest, doctest
from zope import interface, component, event
from zojax.content.type.interfaces import IContentContainer
from zope.location.interfaces import IPossibleSite
from zope.security.management import newInteraction, endInteraction
from zope.app.component.hooks import setSite
from zope.app.testing import functional
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.app.security.interfaces import IAuthentication
from zope.lifecycleevent import ObjectCreatedEvent
from zope.app.rotterdam import Rotterdam
from zojax.personal.space.manager import PersonalSpaceManager
from zojax.personal.space.interfaces import IPersonalSpaceManager
from zojax.catalog.catalog import Catalog, ICatalog
from zojax.content.space.content import ContentSpace
from zojax.layoutform.interfaces import ILayoutFormLayer
from zope.app.component.interfaces import ISite
from zope.app.folder.folder import Folder
from zope.app.component.site import LocalSiteManager, SiteManagementFolder

from content import Portal

zojaxsitemapLayer = functional.ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'zojaxsitemapLayer', allow_teardown=True)


class TestSite(Folder):
    interface.implements(IPossibleSite, ISite, IContentContainer)
    title = u'Tets site'

    def setSiteManager(self, sm):
       self._sm = sm
       setattr(self._sm, 'title', self.title)

    def getSiteManager(self):
        return self._sm


class PrincipalInformation(object):

    readonly = True
    firstname = u''
    lastname = u''
    email = u''

    def __init__(self, principal):
        self.principal = principal


def FunctionalDocFileSuite(*paths, **kw):
    layer = zojaxsitemapLayer

    globs = kw.setdefault('globs', {})
    globs['http'] = functional.HTTPCaller()
    globs['getRootFolder'] = functional.getRootFolder
    globs['sync'] = functional.sync

    kw['package'] = doctest._normalize_module(kw.get('package'))

    kwsetUp = kw.get('setUp')
    def setUp(test):
        functional.FunctionalTestSetup().setUp()

        newInteraction()

        root = functional.getRootFolder()
        setSite(root)
        sm = root.getSiteManager()
        setattr(root, 'title', 'Site Title')

        # IIntIds
        root['ids'] = IntIds()
        sm.registerUtility(root['ids'], IIntIds)
        root['ids'].register(root)

        # catalog
        root['catalog'] = Catalog()
        sm.registerUtility(root['catalog'], ICatalog)

        # space
        space = ContentSpace(title=u'Space')
        event.notify(ObjectCreatedEvent(space))
        root['space'] = space

        #space
        site = TestSite()
        site.setSiteManager(LocalSiteManager(root))
        event.notify(ObjectCreatedEvent(site))
        root['site'] = site

        # people
        people = PersonalSpaceManager(title=u'People')
        event.notify(ObjectCreatedEvent(people))
        root['people'] = people
        sm.registerUtility(root['people'], IPersonalSpaceManager)

        user = sm.getUtility(IAuthentication).getPrincipal('zope.mgr')
        people.assignPersonalSpace(user)
        
        user = sm.getUtility(IAuthentication).getPrincipal('zope.user')
        people.assignPersonalSpace(user)




        endInteraction()
        
    kw['setUp'] = setUp

    kwtearDown = kw.get('tearDown')
    def tearDown(test):
        setSite(None)
        functional.FunctionalTestSetup().tearDown()

    kw['tearDown'] = tearDown

    if 'optionflags' not in kw:
        old = doctest.set_unittest_reportflags(0)
        doctest.set_unittest_reportflags(old)
        kw['optionflags'] = (old|doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)

    suite = doctest.DocFileSuite(*paths, **kw)
    suite.layer = layer
    return suite


class IDefaultSkin(ILayoutFormLayer, Rotterdam):
    """ skin """


def test_suite():
    return unittest.TestSuite((
            FunctionalDocFileSuite("testbrowser.txt"),
            ))
