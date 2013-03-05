# -*- coding: utf-8 -*-
from pyramid.httpexceptions import HTTPFound

import ldap
from pyramid_ldap import (
    get_ldap_connector,
    groupfinder,
    )

from pyramid.view import (
    view_config,
    forbidden_view_config,
)
from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    unauthenticated_userid,
)
from .security import comprova_usuari

@view_config(route_name='home', renderer='main.mako')
def home_view(request):
    return { 'project':'egipcis', 'page':"home", 'logged_in':unauthenticated_userid(request) }

@view_config(route_name='keops', renderer='keops.mako', permission='master')
def keops_view(request):
    return { 'project':'egipcis', 'page':"Keops", 'logged_in':unauthenticated_userid(request) }

@view_config(route_name='temple', renderer='temple.mako', permission='sacerdots')
def temple_view(request):
    return { 'project':'egipcis', 'page':"Temple", 'logged_in':unauthenticated_userid(request) }

@view_config(route_name='cairo', renderer='cairo.mako', permission='view')
def admin_view(request):
    return { 'project':'egipcis', 'page':"El Cairo", 'logged_in':unauthenticated_userid(request) }


# aquest decorator és per establir la ruta per /login
@view_config( route_name='login', renderer='login.mako')
# aquest altre ens redirigirà aquí quan algú intenti entrar en una web que no té permís
@forbidden_view_config(renderer='login.mako')
def login(request):
    login_url = request.current_route_url()
    # detectem des de quina URL ve el visitant
    referrer = request.url
    # retornem l'usuari a la home page si ha vingut directe al login
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    user = authenticated_userid(request)
    if user:
        lloc = came_from.split("/")
        message = "Ets %s, i com a tal no pots entrar a %s" % (user,lloc[len(lloc)-1])
    else:
        message = "Identifica't per entrar al sagrat mon d'Egipte"
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        connector = get_ldap_connector( request )
        data = connector.authenticate( login, password )
        if data is not None:
            #dn = data[0]
            dn = data[1]["uid"][0]
            print "DADES=" + str(data)
            print "login OK per " + data[1]["uid"][0] + " dn="+dn
            headers = remember(request,dn)
            return HTTPFound( location=came_from, headers=headers )
            
        #if comprova_usuari(login,password):
        #    headers = remember(request, login)
        #    return HTTPFound(location = came_from,
        #                     headers = headers)
        message = 'Failed login'

    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password,
        user = authenticated_userid(request), # afegim usuari autenticat si l'hi ha
        )
    

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('home'),
                     headers = headers)
                     
