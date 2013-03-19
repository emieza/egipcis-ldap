# -*- coding: utf-8 -*-

from pyramid.security import (
    Allow,
    Everyone,
    Authenticated,
    )
    
    
class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, Authenticated, 'sacerdots'),
                (Allow, 'cn=farao,ou=grups,dc=enric,dc=tk', 'master')
            ]
    def __init__(self, request):
        pass
        

