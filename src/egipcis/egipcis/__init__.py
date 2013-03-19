# -*- coding: utf-8 -*-
from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .models import RootFactory
from .security import groupfinder
# enlloc del mòdul clàssic de seguretat farem servir el groupfinder de LDAP
#from pyramid_ldap import groupfinder

import ldap
import os
here = os.path.dirname(os.path.abspath(__file__))

# Adaptat de:
# http://docs.pylonsproject.org/projects/pyramid/en/latest/tutorials/wiki2/authorization.html
# LDAP de:
# http://docs.pylonsproject.org/projects/pyramid_ldap/en/latest/

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['mako.directories'] = os.path.join(here, 'templates')
    
    # afegit del auth module
    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(root_factory='.models.RootFactory', settings=settings)
    
    # setup LDAP server
    config.include("pyramid_ldap")
    config.ldap_setup('ldap://enric.tk',
                bind="",passwd="", # anonymous bind
#                bind = 'CN=admin,DC=enric,DC=tk',
#                passwd = 'tralala'
            )
    config.ldap_set_login_query(
                base_dn = "ou=usuaris,dc=enric,dc=tk",
                filter_tmpl = "(uid=%(login)s)",
                scope = ldap.SCOPE_ONELEVEL,
            )
    config.ldap_set_groups_query(
                base_dn='ou=grups,dc=enric,dc=tk',
                filter_tmpl='(&(objectClass=groupOfNames)(member=%(userdn)s))',
                scope = ldap.SCOPE_SUBTREE,
 #           cache_period = 600,
    )
 
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    # static view setup
    #config.add_static_view('static', os.path.join(here, 'static'))
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('keops', '/keops')
    config.add_route('temple', '/temple')
    config.add_route('cairo', '/cairo')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.scan()
    return config.make_wsgi_app()
