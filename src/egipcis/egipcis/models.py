# -*- coding: utf-8 -*-

from pyramid.security import (
    Allow,
    Everyone,
    Authenticated,
    )
    
    
class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, Authenticated, 'sacerdots'),
                (Allow, 'group:farao', 'master')
            ]
    def __init__(self, request):
        pass
        

