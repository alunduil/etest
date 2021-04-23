"""etest bash parser tests."""
import logging
import textwrap
from typing import Dict, Tuple

import pytest

import etest.parsers.bash as sut
from etest.lexers.bash import BashLexer

_LOGGER = logging.getLogger(__name__)


@pytest.fixture()
def bash(tmp_path_factory: pytest.TempPathFactory) -> Tuple[BashLexer, sut.BashParser]:
    """Bash lexer and parser fixture for pytest."""
    lexer = BashLexer()
    lexer.build()

    parser = sut.BashParser()
    parser.build(debug=1, debugfile=tmp_path_factory.mktemp("etest") / "parsers" / "bash" / "parser.out", debuglog=None)

    return lexer, parser


@pytest.mark.parametrize(
    "symbols,script",
    [
        # Correctly parse case statements.
        (
            {},
            textwrap.dedent(
                """\
                case ${EBUILD_PHASE} in
                prepare|configure|compile|install)
                    pushd python > /dev/null || die
                    distutils_src_${EBUILD_PHASE}
                    popd > /dev/null
                    ;;
                esac
                """,
            ),
        ),
        # Correctly parse implicit string concatenation.
        (
            {"FOO": "barbaz"},
            textwrap.dedent(
                """\
                FOO="bar"baz
                """,
            ),
        ),
        # Correctly parse empty string values.
        (
            {"IUSE": ""},
            textwrap.dedent(
                """\
                IUSE=""
                """,
            ),
        ),
        # Correctly parse equals signs in values.
        (
            {"FOO": "bar=baz"},
            textwrap.dedent(
                """\
                FOO=bar=baz
                """,
            ),
        ),
        # Correctly parse a variable assigned to a variable.
        (
            {"MY_PN": "${PN/-/.}"},
            textwrap.dedent(
                """\
                MY_PN=${PN/-/.}
                """,
            ),
        ),
        # Correctly parse a number as a word token.
        (
            {},
            textwrap.dedent(
                """\
                pkg_setup() {
                    python_set_active_version 2
                    python_pkg_setup
                }
                """,
            ),
        ),
        # Correctly parse arguments to functions starting with bang.
        (
            {},
            textwrap.dedent(
                """\
                use !gtk3
                """,
            ),
        ),
        # Correctly parse words with equals without assignment in array.
        (
            {
                "mycmakeargs": (
                    "-DVALA_EXECUTABLE=${VALAC}",
                    "-DGSETTINGS_COMPILE=OFF",
                    "-DMINIMAL_FLAGS=ON",
                ),
            },
            textwrap.dedent(
                """\
                local mycmakeargs=(
                    -DVALA_EXECUTABLE="${VALAC}"
                    -DGSETTINGS_COMPILE=OFF
                    -DMINIMAL_FLAGS=ON
                )
                """,
            ),
        ),
        # Correctly parse unexpected die.
        (
            {},
            textwrap.dedent(
                """\
                die
                mv "${WORKDIR}"/${P}-${lang}.po po/${lang}.po || die
                """,
            ),
        ),
        # Correctly parse empty text.
        (
            {},
            textwrap.dedent(
                """\

                """,
            ),
        ),
        # Correctly parse a single comment.
        (
            {},
            textwrap.dedent(
                """\
                # comment
                """,
            ),
        ),
        # Correctly parses plus operator to find arguments.
        (
            {},
            textwrap.dedent(
                """\
                find "${D}" -name '*.la' -exec rm -f '{}' +
                """,
            ),
        ),
        # Correctly parse escaped characters as a word.
        (
            {},
            textwrap.dedent(
                r"""\
                find bin.* -mindepth 1 -maxdepth 1 -type f -exec dobin '{}' \; || die
                """,
            ),
        ),
        # Correctly parse a single variable assignment.
        (
            {"FOO": "bar"},
            textwrap.dedent(
                """\
                FOO=bar
                """,
            ),
        ),
        # Correctly parse an array variable assignment.
        (
            {"FOO": ("bar",)},
            textwrap.dedent(
                """\
                FOO=( bar )
                """,
            ),
        ),
        # Correctly parse an if statement with else.
        (
            {
                "mycmakeargs": (
                    "$(cmake-utils_use_with semantic-desktop Soprano)",
                    "$(cmake-utils_use_with kipi)",
                ),
                "mycmakeargs+": ("-DGWENVIEW_SEMANTICINFO_BACKEND=None",),
            },
            textwrap.dedent(
                """\
                src_configure() {
                    local mycmakeargs=(
                        $(cmake-utils_use_with semantic-desktop Soprano)
                        $(cmake-utils_use_with kipi)
                    )
                    # Workaround for bug #479510
                    if [[ -e ${EPREFIX}/usr/include/${CHOST}/jconfig.h ]]; then
                        mycmakeargs+=( -DJCONFIG_H="${EPREFIX}/usr/include/${CHOST}/jconfig.h" )
                    fi

                    if use semantic-desktop; then
                        mycmakeargs+=(-DGWENVIEW_SEMANTICINFO_BACKEND=Nepomuk)
                    else
                        mycmakeargs+=(-DGWENVIEW_SEMANTICINFO_BACKEND=None)
                    fi

                    kde4-base_src_configure
                }
                """,
            ),
        ),
        # Correctly parse command containing path argument.
        (
            {},
            textwrap.dedent(
                """\
                python_install_all() {
                    distutils-r1_python_install_all

                    keepdir /etc/holland
                }
                """,
            ),
        ),
        # Correctly parse quoted subshell.
        (
            {
                "currentamanda": "$(set | egrep \"^AMANDA_\" | grep -v '^AMANDA_ENV_SETTINGS' | xargs)",
            },
            textwrap.dedent(
                """\
                currentamanda="$(set | egrep "^AMANDA_" | grep -v '^AMANDA_ENV_SETTINGS' | xargs)"
                """,
            ),
        ),
        # Correctly parse quoted variable expressions.
        (
            {
                "SRC_URI": "mirror://pypi/${MY_PN:0:1}/${MY_PN}/${MY_PN}-${PV}.tar.gz",
            },
            textwrap.dedent(
                """\
                SRC_URI="mirror://pypi/${MY_PN:0:1}/${MY_PN}/${MY_PN}-${PV}.tar.gz"
                """,
            ),
        ),
        # Correctly parse for over a list of numbers.
        (
            {},
            textwrap.dedent(
                """\
                for i in 1 2 3 4; do
                    foo
                done
                """,
            ),
        ),
        # Correctly parse multiline array assignment.
        (
            {
                "FOO": ("bar",),
            },
            textwrap.dedent(
                """\
                local FOO=(
                    bar
                )
                """,
            ),
        ),
        # Correctly parse an ebuild.
        (
            {"DESTDIR": "${D}"},
            textwrap.dedent(
                """\
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
                """,
            ),
        ),
        # Correctly parse a word with an underscore.
        (
            {
                "MY_P": "${PN}_${PV}",
            },
            textwrap.dedent(
                """\
                MY_P=${PN}_${PV}
                """,
            ),
        ),
        # Correctly parse array without padded parentheses.
        (
            {"HTML_DOCS": ("doc/build/html/.",), "EXAMPLES": ("examples/.",)},
            textwrap.dedent(
                """\
                python_install_all() {
                    use doc && local HTML_DOCS=( doc/build/html/. )
                    use examples && local EXAMPLES=(examples/.)

                    distutils-r1_python_install_all
                }
                """,
            ),
        ),
        # Correctly parse nested curly braces.
        (
            {"CTARGET": "${CTARGET:-${CHOST}}"},
            textwrap.dedent(
                """\
                local CTARGET=${CTARGET:-${CHOST}}
                """,
            ),
        ),
        # Correctly parse double quote assignment.
        (
            {"FOO": "bar bar", "EGIT_REPO_URI": "git://github.com/alunduil/etest.git"},
            textwrap.dedent(
                """\
                FOO="bar bar"
                EGIT_REPO_URI="git://github.com/alunduil/etest.git"
                """,
            ),
        ),
        # Correctly parses function definition.
        (
            {},
            textwrap.dedent(
                """\
                python_test() {
                    nosetests || die "Tests failed under ${EPYTHON}"
                }
                """,
            ),
        ),
        # Correctly parse for loop with unencapsulated word list.
        (
            {},
            textwrap.dedent(
                """\
                for test in test.py selftest.py selftest2.py; do
                    echo foo
                done
                """,
            ),
        ),
        # Correctly parse curly brace expansion.
        (
            {"FOO": ("python2_7", "python3_3")},
            textwrap.dedent(
                """\
                FOO=python{2_7,3_3}
                """,
            ),
        ),
        # Correctly parse assign keywords.
        (
            {
                "IUSE_LINGUAS": (
                    "en",
                    "da",
                    "de",
                    "es",
                    "fi",
                    "fr",
                    "it",
                    "ja",
                    "ko",
                    "nl",
                    "no",
                    "pt_BR",
                    "se",
                    "zh_CN",
                ),
            },
            textwrap.dedent(
                """\
                IUSE_LINGUAS=( en da de es fi fr it ja ko nl no pt_BR se zh_CN )
                """,
            ),
        ),
        # Correctly parse asterisk word token.
        (
            {},
            textwrap.dedent(
                """\
                dodoc -r *
                """,
            ),
        ),
        # Correctly parse equals inside quotes.
        (
            {},
            textwrap.dedent(
                """\
                echo "CONFIG_EAP=y" >> ${CONFIG}
                """,
            ),
        ),
        # Correctly parse word with subshell embedded.
        (
            {},
            textwrap.dedent(
                """\
                insinto /usr/$(get_libdir)/crda/
                """,
            ),
        ),
        # Correctly parse function with subshells.
        (
            {},
            textwrap.dedent(
                """\
                src_configure() {
                    econf \
                        $(use_enable python) \
                        $(use_enable java)
                }
                """,
            ),
        ),
        # Correctly parse variables in double quotes.
        (
            {},
            textwrap.dedent(
                """\
                if [[ "${LC_ALL}" = "C" ]]; then
                    echo
                fi
                """,
            ),
        ),
        # Correctly parse line continuation.
        (
            {},
            textwrap.dedent(
                """\
                foo \
                    continues \
                    on
                """,
            ),
        ),
        # Correctly parse unadorned curly braces.
        (
            {},
            textwrap.dedent(
                """\
                find "${ED}" -name '*.la' -exec rm -f {} +
                """,
            ),
        ),
    ],
)
def test_correctly_parsed_symbols(bash: Tuple[BashLexer, sut.BashParser], symbols: Dict[str, str], script: str) -> None:
    """Test example scripts for correct symbols parsing."""
    _LOGGER.debug(f"script: {script}")
    lexer, parser = bash
    parser.parser.parse(debug=_LOGGER, input=script, lexer=lexer.lexer)
    assert symbols == parser.symbols


@pytest.mark.parametrize(
    "script",
    [
        # Error on dangling double quote.
        (
            textwrap.dedent(
                """\
                Foo="
                """,
            ),
        ),
    ],
)
def test_correctly_parsed_errors(bash: Tuple[BashLexer, sut.BashParser], script: str) -> None:
    """Test example scripts for errored parsing."""
    _LOGGER.debug(f"script: {script}")
    lexer, parser = bash
    with pytest.raises(sut.BashSyntaxError):
        parser.parser.parse(debug=_LOGGER, input=script, lexer=lexer.lexer)
