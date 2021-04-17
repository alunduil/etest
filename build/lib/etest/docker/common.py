# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import docker
import os
import ssl

BASE_URL = os.environ.get('DOCKER_HOST')
TLS_CONFIG = None

if len(os.environ.get('DOCKER_TLS_VERIFY', '')):
    BASE_URL = 'https://{0}'.format(BASE_URL.split('://', 1)[-1])

    CERT_PATH = os.environ.get('DOCKER_CERT_PATH', '')
    if not len(CERT_PATH):
        CERT_PATH = os.path.join(os.environ.get('HOME', ''), '.docker')

    TLS_CONFIG = docker.tls.TLSConfig(
        ssl_version = ssl.PROTOCOL_TLSv1,
        verify = True,
        assert_hostname = False,
        client_cert = ( os.path.join(CERT_PATH, 'cert.pem'), os.path.join(CERT_PATH, 'key.pem') ),
        ca_cert = os.path.join(CERT_PATH, 'ca.pem')
    )

CLIENT = docker.Client(base_url = BASE_URL, tls = TLS_CONFIG)
