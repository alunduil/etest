FROM wking/gentoo:latest
MAINTAINER Alex Brandt <alunduil@gentoo.org>

ENV ACCEPT_KEYWORDS ~amd64
ENV PORTDIR_OVERLAY /overlay

RUN echo 'FEATURES="collision-protect parallel-fetch strict"' >> /etc/portage/make.conf

RUN mkdir /etc/portage/env
RUN echo 'FEATURES="test"' >> /etc/portage/env/test
RUN touch /etc/portage/package.env

RUN mkdir /overlay
