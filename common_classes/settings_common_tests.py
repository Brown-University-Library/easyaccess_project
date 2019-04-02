# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os


ILLIAD_REMOTE_AUTH_URL = os.environ['EZACS__COMMON_CLASSES_ILLIAD_REMOTE_AUTH_URL']
ILLIAD_REMOTE_AUTH_HEADER = os.environ['EZACS__COMMON_CLASSES_ILLIAD_REMOTE_AUTH_HEADER']

## illiad-api (eventually all illiad calls will be to the API)
ILLIAD_API_URL = os.environ['EZACS__COMMON_ILLIAD_API_URL_ROOT']
ILLIAD_API_KEY = os.environ['EZACS__COMMON_ILLIAD_API_KEY']
ILLIAD_API_BASIC_AUTH_USER = os.environ['EZACS__COMMON_ILLIAD_API_BASIC_AUTH_USER']  # for gets
ILLIAD_API_BASIC_AUTH_PASSWORD = os.environ['EZACS__COMMON_ILLIAD_API_BASIC_AUTH_PASSWORD']

TEST_ILLIAD_GOOD_USERNAME = os.environ['EZACS__COMMON_CLASSES_TEST_ILLIAD_GOOD_USERNAME'].decode( 'utf-8' )
TEST_ILLIAD_DISAVOWED_USERNAME = os.environ['EZACS__COMMON_CLASSES_TEST_ILLIAD_DISAVOWED_USERNAME'].decode( 'utf-8' )
TEST_ILLIAD_BLOCKED_USERNAME = os.environ['EZACS__COMMON_CLASSES_TEST_ILLIAD_BLOCKED_USERNAME'].decode( 'utf-8' )

TEST_ILLIAD_NEW_USER_ROOT = os.environ['EZACS__COMMON_CLASSES_TEST_ILLIAD_NEW_USERNAME_ROOT'].decode( 'utf-8' )
