#!/bin/bash -e

#arches=(
#	amd64
#	x86
#	arm64
#	armv5
#	armv7
#	ppc64
#)

# Correctly handle no-arg options.
for arg in "$@"; do
	shift
	case "$arg" in
		"--hardened") set -- "$@" "--hardened" "''" ;;
		"--no-multilib") set -- "$@" "--no-multilib" "''" ;;
		"--systemd") set -- "$@" "--systemd" "''" ;;
		"--all") set -- "$@" "--all" "''" ;;
		*) set -- "$@" "$arg"
	esac
done

opts=$(getopt \
	--longoptions "hardened: no-multilib: systemd: all: arch: env:" \
	--name "$(basename "$0")" \
	--options "" \
	-- "$@"
)

eval set "--$opts"

while [[ $# -gt 0 ]]; do
	case "$1" in
		--arch)
			arch=$2
			shift 2
			;;
		--env)
			env=$2
			shift 2
			;;
		--hardened)
			hardened=True
			shift 2
			;;
		--no-multilib)
			nomultilib=True
			shift 2
			;;
		--systemd)
			systemd=True
			shift 2
			;;
		--all)
			all=True
			shift 2
			;;
		*)
			break
			;;
	esac
done

# Decide which profile to pull
if [ ! "$arch" ] ; then arch="amd64" ; fi
if [ "$arch" = "ppc64" ] ; then img_arch="ppc64le" ; else img_arch=$arch ; fi

libc=$env
if [ "$libc" ] ; then profile="-$libc" ; fi

if [ "$hardened" ] ; then profile="$profile-hardened" ; elif [ "$libc" ] ; then profile="$profile-vanilla" ; fi
if [ "$nomultilib" ] ; then env="$profile-nomultilib" ; fi
if [ "$systemd" ] ; then env="$profile-systemd" ; fi

img_profile="$img_arch$profile"
profile="$arch$profile"

if [ "$all" ]
	then echo "$profile"
	echo "$img_profile"
else
	# We have to dance around x86 needing more privileges :/
	docker buildx build . --build-arg PROFILE="$img_profile" --build-arg LIBC="$libc" --tag etest/pre-sync:"$profile"
	if [ "$libc" = "musl" ] ; then
		docker run --name sync --privileged etest/pre-sync:"$profile" /bin/bash -c "emerge-webrsync && emerge dev-vcs/git && emerge --sync musl"
	else
		docker run --name sync --privileged etest/pre-sync:"$profile" /bin/bash -c "emerge-webrsync"
	fi
	docker commit sync alunduil/etest:"$profile"
	docker rm sync
	docker image rm etest/pre-sync:"$profile"
fi
