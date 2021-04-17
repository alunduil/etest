# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

from test_etest.test_fixtures.test_scripts import SCRIPTS

_ = '''
src_configure() {
        # Bigloo doesn't use autoconf and consequently a lot of options used by econf give errors
        # Manuel Serrano says: "Please, dont talk to me about autoconf. I simply dont want to hear about it..."
        ./configure \
                $(use java && echo "--jvm=yes --java=$(java-config --java) --javac=$(java-config --javac)") \
                --prefix=/usr \
                --mandir=/usr/share/man \
                --infodir=/usr/share/info \
                --libdir=/usr/$(get_libdir) \
                --docdir=/usr/share/doc/${PF} \
                --benchmark=yes \
                --sharedbde=no \
                --sharedcompiler=no \
                --coflags="" || die "configure failed"

#               --bee=$(if use fullbee; then echo full; else echo partial; fi) \

}

src_compile() {
        if use emacs; then
                elisp-compile etc/*.el || die "elisp-compile failed"
        fi

        # parallel build is broken
        emake -j1 || die "emake failed"
}

src_install () {
#       dodir /etc/env.d
#       echo "LDPATH=/usr/$(get_libdir)/bigloo/${PV}/" > ${D}/etc/env.d/25bigloo

        # make the links created not point to DESTDIR, since that is only a temporary home
        sed 's/ln -s $(DESTDIR)/ln -s /' -i Makefile.misc
        emake -j1 DESTDIR="${D}" install || die "install failed"

        if use emacs; then
                elisp-install ${PN} etc/*.{el,elc} || die "elisp-install failed"
                elisp-site-file-install "${FILESDIR}/${SITEFILE}"
        fi

#       einfo "Compiling bee..."
#       emake compile-bee || die "compiling bee failed"
}

pkg_postinst() {
        use emacs && elisp-site-regen
}

pkg_postrm() {
        use emacs && elisp-site-regen
}
'''

_ = {
    'uuid': '41a217e3-097c-487b-8a0e-cc1ffc7ffe40',

    'description': 'spurious quote token',

    'text': _,

    'symbols': {
        'DESTDIR': '${D}',
    },

    'correct': None,
}

SCRIPTS.setdefault('all', []).append(_)
SCRIPTS.setdefault('bash', []).append(_)
