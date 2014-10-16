FROM wking/gentoo:latest
MAINTAINER Alex Brandt <alunduil@gentoo.org>

RUN sed -e '/en_US/s/^#//' -i /etc/locale.gen 
RUN locale-gen
RUN eselect locale set en_US.utf8

ENV ACCEPT_KEYWORDS ~amd64
ENV PORTDIR_OVERLAY /overlay
ENV EGIT3_STORE_DIR /tmp

RUN echo 'FEATURES="collision-protect parallel-fetch strict"' >> /etc/portage/make.conf

RUN mkdir /etc/portage/env
RUN echo 'FEATURES="test"' >> /etc/portage/env/test
RUN touch /etc/portage/package.env

RUN mkdir /overlay
