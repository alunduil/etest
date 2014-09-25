python_test() {
	nosetests || die "Tests failed under ${EPYTHON}"
}
