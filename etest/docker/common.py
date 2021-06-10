"""Common Docker components."""

import datetime
import os
import ssl

import docker

BASE_URL = os.environ.get("DOCKER_HOST")
TLS_CONFIG = None

if len(os.environ.get("DOCKER_TLS_VERIFY", "")):
    if BASE_URL is None:
        raise RuntimeError("DOCKER_HOST not set.")

    BASE_URL = "https://{}".format(BASE_URL.split("://", 1)[-1])

    CERT_PATH = os.environ.get("DOCKER_CERT_PATH", "")
    if not len(CERT_PATH):
        CERT_PATH = os.path.join(os.environ.get("HOME", ""), ".docker")

    TLS_CONFIG = docker.tls.TLSConfig(
        ssl_version=ssl.PROTOCOL_TLSv1,
        verify=True,
        assert_hostname=False,
        client_cert=(os.path.join(CERT_PATH, "cert.pem"), os.path.join(CERT_PATH, "key.pem")),
        ca_cert=os.path.join(CERT_PATH, "ca.pem"),
    )

TIMEOUT = int(datetime.timedelta(minutes=10).total_seconds())

CLIENT = docker.from_env(timeout=TIMEOUT)
API_CLIENT = docker.APIClient(base_url=BASE_URL, tls=TLS_CONFIG, timeout=TIMEOUT)
