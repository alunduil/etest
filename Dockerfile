FROM wking/gentoo
MAINTAINER Alex Brandt <alunduil@alunduil.com>

ENV ACCEPT_KEYWORDS ~amd64
ENV PORTDIR_OVERLAY /overlay

RUN echo FEATURES="collision-protect parallel-fetch strict stricter" >> /etc/portage/make.conf

RUN mkdir /etc/portage/env
RUN echo FEATURES="test" >> /etc/portage/env/test

RUN mkdir /overlay
