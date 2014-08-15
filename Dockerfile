FROM wking/gentoo
MAINTAINER Alex Brandt <alunduil@alunduil.com>

ENV ACCEPT_KEYWORDS "~amd64"
ENV FEATURES "collision-protect parallel-fetch strict stricter test"
ENV PORTDIR_OVERLAY "/overlay"

RUN mkdir /overlay
