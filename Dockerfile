FROM wking/gentoo
MAINTAINER Alex Brandt <alunduil@gentoo.org>

ENV ACCEPT_KEYWORDS ~amd64
ENV PORTDIR_OVERLAY /overlay
ENV PYTHON_TARGETS *

RUN echo 'FEATURES="collision-protect parallel-fetch strict"' >> /etc/portage/make.conf

RUN mkdir /etc/portage/env
RUN echo 'FEATURES="test"' >> /etc/portage/env/test

RUN mkdir /overlay
