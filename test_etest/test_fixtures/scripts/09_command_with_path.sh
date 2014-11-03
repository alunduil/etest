python_install_all() {
        distutils-r1_python_install_all

        keepdir /etc/holland
        keepdir /etc/holland/backupsets
        keepdir /etc/holland/providers

        insinto /etc/holland/backupsets
        doins "${S}"/../../config/backupsets/examples/${PN##*-}.conf

        insinto /etc/holland/providers
        doins "${S}"/../../config/providers/${PN##*-}.conf
}
