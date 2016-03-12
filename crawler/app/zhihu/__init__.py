#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class User(object):
    __slots__ = ('user_id', 'user_name', 'have_disposed')

    def __init__(self, user_id, user_name, have_disposed='false'):
        self.user_id = user_id
        self.user_name = user_name
        self.have_disposed = have_disposed
        super().__init__()







