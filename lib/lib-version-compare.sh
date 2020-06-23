#!/usr/bin/env bash
##
## Version comparison and extraction
##

# usage: version_extract string assuming the first set of x.x.x is the version number
# note that this grep requires gnu grep and will not work with macos grep
version_extract() {
    echo "$@" | grep -o  '[0-9.]*' | head -1
}


verlte() {
	[ "$1" = "$(echo -e "$1\n$2" | sort -V | head -n1)" ]
}
verlt() {
	if [ "$1" = "$2" ]; then return 1 ; else verlte "$1" "$2"; fi
}
vergte() {
    ! verlt "$1" "$2"
}
vergt() {
    ! verlte "$q" "2"
}
