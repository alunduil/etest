#!/bin/bash -e

#arches=(
#	amd64
#	x86
#	arm64
#	armv5
#	armv7
#	ppc64
#)

opts=$(getopt \
	--longoptions "arch: env: all" \
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


if [ $all ]
	then echo "all"
else
	# We have to dance around x86 needing more privileges :/
	if [ "$arch" ] ; then
		if [ "$arch" = "ppc64" ] ; then img_arch="ppc64le" ; else img_arch=$arch ; fi
		docker buildx build . --build-arg ARCH="$img_arch" --tag etest/pre-sync:"$arch"
		docker run --name sync --privileged etest/pre-sync:"$arch" /bin/bash -c "emerge-webrsync"
		docker commit sync alunduil/etest:"$arch"
		docker rm sync
		docker image rm etest/pre-sync:"$arch"
	else
		arch="amd64"
		docker buildx build . --build-arg ARCH="$arch" --tag etest/pre-sync:"$arch"
                docker run --name sync --privileged etest/pre-sync:"$arch" /bin/bash -c "emerge-webrsync"
                docker commit sync alunduil/etest:"$arch"
                docker rm sync
                docker image rm etest/pre-sync:"$arch"
	fi
fi

#docker buildx build . --build-arg ARCH=$arch --tag alunduil/etest:$arch
