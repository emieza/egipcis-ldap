# -*- coding: utf-8 -*-

import ldap
from pyramid_ldap import (
    get_ldap_connector,
#    groupfinder,
    )

def groupfinder(dn, request):
    connector = get_ldap_connector(request)
    group_list = connector.user_groups(dn)
    if group_list is None:
        return None
    group_dns = []
    for dn, attrs in group_list:
        group_dns.append(dn)
    return group_dns

# FUNCIONS ANTIGUES (Pyramid Auth)
#USERS = {   'tutankamon':'tutan123',
#            'ramfis':'ramfis123',
#            'radames':'radames123',
#            'aida':'aida123',
#        }
#GROUPS = {  'tutankamon':['group:farao','group:sacerdots'],
#            'ramfis':['group:sacerdots'],
#        }
#def groupfinder(userid, request):
#    if userid in USERS:
#        return GROUPS.get(userid, [])
# Aquesta funció comprova el nostre usuari/contrasenya
# si cal fer-ho a una base de dades ho encapsularem en aquesta funció
#def comprova_usuari(userid, passw):
    # de moment ho resolem amb un diccionari amb el id/pass dels usuaris
#    if USERS.get(userid)==passw:
#        return True
#    return False

