#!/usr/bin/env bash
##
## Mac OS X specific routines
##

# If this is full xcode make sure to accept the license
xcode_license_accept() {
    # https://apple.stackexchange.com/questions/175069/how-to-accept-xcode-license:w
    # command line tools do not have xcodebuild and do not need a license
    # note we cannot use bash 4.x constructs as this might be called with vanilla MacOS
    if ! xcode-select -p | grep -q  CommandLineTools
    then
        sudo xcodebuild -license accept
    fi
}

# returns the mac release
mac_version() {
    echo $(sw_vers -productVersion)
}

#  converst version to the code name used for things like install-macports.sh which needs names
# https://en.wikipedia.org/wiki/MacOS
mac_codename() {
    case $(mac_version) in
        10.15*)
            echo Catalina
            ;;
        10.14*)
            echo Mojave
            ;;
        10.13*)
            echo High Sierra
            ;;
        10.12*)
            echo Sierra
            ;;
        10.11*)
            echo El Capitan
            ;;
        10.10*)
            echo Yosemite
            ;;
        10.9*)
            echo Mavericks
            ;;
        10.8*)
            echo Mountain Lion
            ;;
        10.7*)
            echo Lion
            ;;
        10.6*)
            echo Snow Leopard
            ;;
        10.5*)
            echo Leopard
            ;;
        10.4*)
            echo Tiger
            ;;
        10.3*)
            echo Panther
            ;;
        10.2*)
            echo Jaguar
            ;;
        10.1*)
            echo Puma
            ;;
        10.0*)
            echo Cheetah
            ;;
        *)
            return 1
    esac
}

# install_app application [location]
install_in_dir() {
    if [[ ! $OSTYPE =~ darwin ]]; then return 0; fi
	if (( $# < 1 )); then return 1; fi
    src="$1"
    dir="${2:-/Application}"
    # move the app if it does not already exist
    if [[ ! -e "$dir/$(basename "$src")" ]]
    then
        sudo mv "$src" "$dir"
    fi
}

# find a file in the /Volumes and you can use the wild card at the end
# usage: find_in_volume filename [volume with wild carding]
find_in_volume() {
    if [[ ! $OSTYPE =~ darwin ]]; then return 0; fi
    if (( $# < 1 )); then return 1; fi
    local path="/Volumes"
    if (( $# > 1 )); then local path="$path/$2"; fi
    # Find the first volume that has the app
    # Note that we use $path so there are can be multiple directories here
    # http://askubuntu.com/questions/444551/get-absolute-path-of-files-using-find-command
    # but readlink -f not availabe on Mac OS, so use feeding find an absolute path
    # returns an absolute path trick
    echo $(find "$path"* -name "$1" -print -quit 2>/dev/null)
}

# install_app application [location]
install_in_dir() {
    if [[ ! $OSTYPE =~ darwin ]]; then return 0; fi
	if (( $# < 1 )); then return 1; fi
    src="$1"
    dir="${2:-/Application}"
    # move the app if it does not already exist
    if [[ ! -e "$dir/$(basename "$src")" ]]
    then
        sudo mv "$src" "$dir"
    fi
}

# find a file in the /Volumes and you can use the wild card at the end
# usage: find_in_volume filename [volume with wild carding]
find_in_volume() {
    if [[ ! $OSTYPE =~ darwin ]]; then return 0; fi
    if (( $# < 1 )); then return 1; fi
    local path="/Volumes"
    if (( $# > 1 )); then local path="$path/$2"; fi
    # Find the first volume that has the app
    # Note that we use $path so there are can be multiple directories here
    # http://askubuntu.com/questions/444551/get-absolute-path-of-files-using-find-command
    # but readlink -f not availabe on Mac OS, so use feeding find an absolute path
    # returns an absolute path trick
    echo $(find "$path"* -name "$1" -print -quit 2>/dev/null)
}

# Looks in /Volumes for the app, runs the command and then detaches
# find_in_volume_open_then_detach name_of_app [volume]
find_in_volume_open_then_detach() {
    if [[ ! $OSTYPE =~ darwin ]]; then return 0; fi
    if (( $# < 1 )); then return 1; fi

    # Find the first volume that hass the app
    # http://stackoverflow.com/questions/5720194/bash-argument-passing-to-child-or
    # uses special behaviou or $@ in double quotes to keep arguments wrapped
    local app=$(find_in_volume "$@" )
    if [[ -z $app ]]; then return 1; fi

    open "$app"
    read -p "Press any key when you are done installing $app "
    hdiutil detach "$(dirname "$app")"
}

# Looks in /Volumes and then moves the app it finds
# usage find_in_volume_copy_then_detach app [volumes]
find_in_volume_copy_then_detach() {
    if [[ ! $OSTYPE =~ darwin ]]; then return 0; fi
    if (( $# < 1 )); then return 1; fi
    local app=$(find_in_volume "$@")
    if [[ -z $app ]]; then return 1; fi

    if [[ ! -e /Applications/$(basename "$app") ]]
    then
        cp -r  "$app" /Applications
    fi
	hdiutil detach "$(dirname "$app")"
}

