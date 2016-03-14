# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime, json, logging, os, pprint, random
from .shib_helper import ShibChecker
from article_request_app import settings_app
from django.conf import settings as project_settings
from django.core.urlresolvers import reverse
from django.utils.http import urlquote


log = logging.getLogger('access')
shib_checker = ShibChecker()


class LoginHelper( object ):
    """ Contains helpers for views.login() """

    def check_referrer( self, session, meta_dict ):
        """ Ensures request came from findit app.
            Called by views.login() """
        findit_check = False
        findit_illiad_check_flag = session.get( 'findit_illiad_check_flag', '' )
        findit_illiad_check_openurl = session.get( 'findit_illiad_check_enhanced_querystring', '' )
        if findit_illiad_check_flag == 'good' and findit_illiad_check_openurl == meta_dict.get('QUERY_STRING', ''):
            findit_check = True
        elif findit_check is not True:
            log.warning( 'Bad attempt from source-url, ```%s```; ip, `%s`' % (
                meta_dict.get('HTTP_REFERER', ''), meta_dict.get('REMOTE_ADDR', '') ) )
        log.debug( 'findit_check, `%s`' % findit_check )
        return findit_check



    def assess_shib_redirect_need( self, session, host, meta_dict ):
        """ Determines whether a shib-redirect login or logout url is needed.
            Returns needed-boolean, and extracted/updated shib_status.
            Called by views.login()
            `shib_status` flow:
            - '', from a new-request, will be changed to 'will_force_logout' and trigger a shib-logout redirect
            - 'will_force_logout' will be changed to 'will_force_login' and trigger a shib-login redirect
            - 'will_force_login' is usually ok, and the session should contain shib info, but if not, a logout-login will be triggered
            TODO: figure out why settings.DEBUG is getting changed unexpectedly and fix it. """
        ( needed, shib_status ) = ( False, session.get('shib_status', '') )
        if host == '127.0.0.1' and project_settings.DEBUG2 == True:  # eases local development
            needed = False
        else:
            if shib_status == '' or shib_status == 'will_force_logout':
                needed = True
            elif shib_status == 'will_force_login' and meta_dict.get('Shibboleth-eppn', '') == '':
                ( needed, shib_status ) = ( True, 'will_force_logout' )
        return_dct = { 'redirect': needed, 'shib_status': shib_status }
        log.debug( 'return_dct, `{}`'.format(return_dct) )
        return return_dct



    def build_shib_redirect_url( self, shib_status, scheme, host, session_dct, meta_dct ):
        """ Builds shib-redirect login or logout url.
            Called by views.login() """
        if shib_status == '':  # clean entry: builds logout url
            redirect_dct = self._make_force_logout_redirect_url( scheme, host, session_dct )
        elif shib_status == 'will_force_logout':  # logout occurred; builds login url
            url = self.make_force_login_redirect_url( request )
        elif shib_status == 'will_force_login' and meta_dict.get('Shibboleth-eppn', '') == '':  # also builds logout url
            url =self.make_force_logout_redirect_url( request )
        log.debug( 'redirect_dct, ```{}```'.format(redirect_dct) )
        return redirect_dct

    def _make_force_logout_redirect_url( self, scheme, host, session_dct ):
        """ Builds logout-redirect url
            Called by build_shib_redirect_url() """
        new_shib_status = 'will_force_logout'
        app_login_url = '%s://%s%s?%s' % ( scheme, host, reverse('article_request:login_url'), session_dct['login_openurl'] )  # app_login_url isn't the shib url; it's the url to this login-app
        log.debug( 'app_login_url, `%s`' % app_login_url )
        encoded_app_login_url = urlquote( app_login_url )  # django's urlquote()
        force_logout_redirect_url = '%s?return=%s' % ( settings_app.SHIB_LOGOUT_URL_ROOT, encoded_app_login_url )
        redirect_dct = { 'redirect_url': force_logout_redirect_url, 'new_shib_status': new_shib_status }
        log.debug( 'redirect_dct, `{}`'.format(redirect_dct) )
        return redirect_dct



    def assess_status( self, request ):
        """ Assesses localdev status and shib_status.
            Called by views.login() """
        localdev = False
        shib_status = request.session.get( 'shib_status', '' )
        if request.get_host() == '127.0.0.1' and project_settings.DEBUG == True:  # eases local development
            localdev = True
        log.debug( 'localdev, `%s`; shib_status, `%s`' % (localdev, shib_status) )
        return ( localdev, shib_status )

    def make_force_logout_redirect_url( self, request ):
        """ Builds logout-redirect url
            Called by views.login() """
        request.session['shib_status'] = 'will_force_logout'
        login_url = '%s://%s%s?%s' % ( request.scheme, request.get_host(), reverse('article_request:login_url'), request.session['login_openurl'] )  # for logout and login redirections
        log.debug( 'login_url, `%s`' % login_url )
        encoded_login_url = urlquote( login_url )  # django's urlquote()
        force_logout_redirect_url = '%s?return=%s' % ( settings_app.SHIB_LOGOUT_URL_ROOT, encoded_login_url )
        log.debug( 'force_logout_redirect_url, `%s`' % force_logout_redirect_url )
        return force_logout_redirect_url

    def make_force_login_redirect_url( self, request ):
        """ Builds login-redirect url
            Called by views.login()
            Note, fyi, normally a shib httpd.conf entry triggers login via a config line like `require valid-user`.
                This SHIB_LOGIN_URL setting, though, is a url like: `https://host/shib.sso/login?target=/this_url_path`
                ...so it's that shib.sso/login url that triggers the login, not this app login url.
                This app login url _is_ shib-configured, though to perceive shib headers if they exist. """
        request.session['shib_status'] = 'will_force_login'
        encoded_openurl = urlquote( request.session['login_openurl'] )
        force_login_redirect_url = '%s?%s' % ( settings_app.SHIB_LOGIN_URL, encoded_openurl )
        log.debug( 'force_login_redirect_url, `%s`' % force_login_redirect_url )
        return force_login_redirect_url

    def grab_user_info( self, request, localdev, shib_status ):
        """ Updates session with real-shib or development-shib info.
            Called by views.login() """
        # if localdev is False and shib_status == 'will_force_login':
        if localdev is False:
            request.session['shib_status'] = ''
            shib_dct = shib_checker.grab_shib_info( request )
        else:  # localdev
            shib_dct = settings_app.DEVELOPMENT_SHIB_DCT
        request.session['user'] = json.dumps( shib_dct )
        log.debug( 'shib_dct, `%s`' % pprint.pformat(shib_dct) )
        return shib_dct

    def update_session( self, request ):
        """ Updates necessary session attributes.
            Called by views.login() """
        request.session['illiad_login_check_flag'] = 'good'
        request.session['findit_illiad_check_flag'] = ''
        request.session['findit_illiad_check_enhanced_querystring'] = ''
        # request.session['shib_status'] = ''
        return

    # end class LoginHelper
