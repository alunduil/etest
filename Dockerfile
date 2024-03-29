FROM gentoo/stage3:amd64
MAINTAINER Alex Brandt <alunduil@gmail.com>

# Set a locale
RUN echo en_US.UTF8 UTF-8 >> /etc/locale.gen
RUN echo en_US ISO-8859-1 >> /etc/locale.gen
RUN locale-gen
RUN eselect locale set en_US.utf8

ENV DISTDIR /tmp/distfiles.d
ENV EMERGE_LOG_DIR /tmp/etest.logs.d
ENV EPAUSE_IGNORE TRUE
ENV NOCOLOR true
ENV PORT_LOGDIR /tmp/etest.logs.d
ENV PORTAGE_ELOG_SYSTEM save
ENV PORTAGE_RO_DISTDIRS /usr/portage/distfiles
ENV PORTDIR_OVERLAY /overlay

RUN mkdir /tmp/distfiles.d
RUN chown root:portage /tmp/distfiles.d
RUN chmod 0775 /tmp/distfiles.d

RUN mkdir /tmp/etest.logs.d
RUN chown portage:portage /tmp/etest.logs.d
RUN chmod 2775 /tmp/etest.logs.d

RUN echo 'FEATURES="collision-protect parallel-fetch strict"' >> /etc/portage/make.conf

RUN mkdir /etc/portage/env
RUN echo 'FEATURES="test"' >> /etc/portage/env/test

RUN touch /etc/portage/package.env

RUN mkdir /overlay

RUN mkdir /etc/portage/package.accept_keywords

RUN emerge --sync
