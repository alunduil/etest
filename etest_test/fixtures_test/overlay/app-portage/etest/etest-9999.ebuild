# Copyright 1999-2014 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

EAPI=5
PYTHON_COMPAT=( python3_3 python3_4 )

inherit distutils-r1 git-r3

EGIT_REPO_URI="git://github.com/alunduil/etest.git"

DESCRIPTION="ebuild testing framework"
HOMEPAGE="https://github.com/alunduil/etest"
SRC_URI=""

LICENSE="MIT"
SLOT="0"
KEYWORDS=""
IUSE="test"

DEPEND="
	dev-python/setuptools[${PYTHON_USEDEP}]
	test? (
		dev-python/coverage[${PYTHON_USEDEP}]
		dev-python/nose[${PYTHON_USEDEP}]
	)
"
RDEPEND="
	dev-python/click[${PYTHON_USEDEP}]
	dev-python/docker-py[${PYTHON_USEDEP}]
	dev-python/ply[${PYTHON_USEDEP}]
"

python_test() {
	nosetests test_etest/test_unit || die "Tests failed under ${EPYTHON}"
}
