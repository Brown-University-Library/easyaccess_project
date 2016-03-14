# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging, os, pprint
from .classes.login_helper import LoginHelper
from django.http import HttpRequest
from django.test import TestCase
from django.test.client import Client


log = logging.getLogger( 'access' )
TestCase.maxDiff = None


class LoginHelper_Test( TestCase ):
    """ Tests classes.LoginHelper() """

    def setUp( self ):
        self.helper = LoginHelper()

    def test__check_referrer( self ):
        """ Tests whether referrer is valid. """
        ## empty request should fail
        client = Client()
        session = client.session
        meta_dict = {}
        self.assertEqual(
            False,
            self.helper.check_referrer(session, meta_dict) )
        ## good request should return True
        client = Client()
        session = client.session
        session['findit_illiad_check_flag'] = 'good'
        session['findit_illiad_check_enhanced_querystring'] = 'querystring_a'
        meta_dict = { 'QUERY_STRING': 'querystring_a' }
        self.assertEqual(
            True,
            self.helper.check_referrer(session, meta_dict) )

    def test__assess_shib_redirect_need( self ):
        """ Tests whether a shib logout or login url needs to be built. """
        ## localdev never needs shib redirect
        session = {}
        host = '127.0.0.1'
        meta_dict = {}
        self.assertEqual(
            { 'redirect': False, 'shib_status': '' },
            self.helper.assess_shib_redirect_need(session, host, meta_dict) )
        ## clean entry needs logout-redirect
        session = { 'shib_status': '' }
        host = 'foo'
        meta_dict = {}
        self.assertEqual(
            { 'redirect': True, 'shib_status': '' },
            self.helper.assess_shib_redirect_need(session, host, meta_dict) )
        ## logout was forced; needs login-redirect
        session = { 'shib_status': 'will_force_logout' }
        host = 'foo'
        meta_dict = {}
        self.assertEqual(
            { 'redirect': True, 'shib_status': 'will_force_logout' },
            self.helper.assess_shib_redirect_need(session, host, meta_dict) )
        ## login was forced and shib headers filled; good, no redirect
        session = { 'shib_status': 'will_force_login' }
        host = 'foo'
        meta_dict = { 'Shibboleth-eppn': 'foo' }
        self.assertEqual(
            { 'redirect': False, 'shib_status': 'will_force_login' },
            self.helper.assess_shib_redirect_need(session, host, meta_dict) )
        ## 'will_force_login' normally good, but this needs shib-headers regrabbed
        session = { 'shib_status': 'will_force_login' }
        host = 'foo'
        meta_dict = { 'Shibboleth-eppn': '' }
        self.assertEqual(
            { 'redirect': True, 'shib_status': 'will_force_logout' },
            self.helper.assess_shib_redirect_need(session, host, meta_dict) )

    def test__build_shib_redirect_url( self ):
        """ Tests the redirect-url. """
        ## clean entry
        redirect_dct = self.helper.build_shib_redirect_url(
            shib_status='', scheme='https', host='foo.edu', session_dct={'login_openurl':'a=b&c=d'}, meta_dct={} )
        self.assertTrue( 'logout' in redirect_dct['redirect_url'] )
        self.assertEqual( 'will_force_logout', redirect_dct['updated_shib_status'] )
        ## logout was forced; needs login-redirect
        redirect_dct = self.helper.build_shib_redirect_url(
            shib_status='will_force_logout', scheme='https', host='foo.edu', session_dct={'login_openurl':'a=b&c=d'}, meta_dct={} )
        self.assertTrue( 'login' in redirect_dct['redirect_url'] )
        self.assertEqual( 'will_force_login', redirect_dct['updated_shib_status'] )
        ## 'will_force_login' normally good, but this needs shib-headers regrabbed
        redirect_dct = self.helper.build_shib_redirect_url(
            shib_status='will_force_login', scheme='https', host='foo.edu', session_dct={'login_openurl':'a=b&c=d'}, meta_dct={'Shibboleth-eppn': ''} )
        self.assertTrue( 'logout' in redirect_dct['redirect_url'] )
        self.assertEqual( 'will_force_logout', redirect_dct['updated_shib_status'] )

    # end class LoginHelper_Test
