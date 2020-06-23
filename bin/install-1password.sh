#!/usr/bin/env bash
##
## install 1Password
## https://news.ycombinator.com/item?id=9091691 for linux gui
## https://news.ycombinator.com/item?id=8441388 for cli
## https://www.npmjs.com/package/onepass-cli for npm package
## 
##@author Rich Tong
##@returns 0 on success
#
# To enable compatibility with bashdb instead of set -e
# https://marketplace.visualstudio.com/items?itemName=rogalmic.bash-debug
# use the trap on ERR
set -u && SCRIPTNAME="$(basename "${BASH_SOURCE[0]}")"
SCRIPT_DIR=${SCRIPT_DIR:=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}
# this replace set -e by running exit on any error use for bashdb
trap 'exit $?' ERR
OPTIND=1
VERSION="${VERSION:-7}"
export FLAGS="${FLAGS:-""}"
while getopts "hdvr:" opt
do
    case "$opt" in
        h)
            cat <<-EOF
Installs 1Password
    usage: $SCRIPTNAME [ flags ]
    flags: -d debug, -v verbose, -h help"
           -r version number (default: $VERSION)
EOF
            exit 0
            ;;
        d)
            export DEBUGGING=true
            ;;
        v)
            export VERBOSE=true
            # add the -v which works for many commands
            export FLAGS+=" -v "
            ;;
        r)
          VERSION="$OPTARG"
          ;;
    esac
done
shift $((OPTIND-1))
if [[ -e "$SCRIPT_DIR/include.sh" ]]; then source "$SCRIPT_DIR/include.sh"; fi
source_lib lib-git.sh lib-mac.sh lib-install.sh lib-util.sh



if [[ -n $(find /Applications -maxdepth 1 -name "1Password*" -print -quit) ]]
then
    log_verbose 1Password for Mac already installed
    exit
fi

log_verbose using brew to install on Mac 1Password and the CLI
if cask_install 1password 1password-cli
then
    log_exit 1password already installed
fi

log_verbose brew cask install failed trying to cure the package
# download_url_open "https://d13itkw33a7sus.cloudfront.net/dist/1P/mac4/1Password-6.0.2.zip"
# more general location
# usage: download_url url [dest_file [dest_dir [md5 [sha256]]]]
# Have to increment the OPM number as versions increase
log_verbose installed 1Password Version $VERSION
download_url_open "https://app-updates.agilebits.com/download/OPM$VERSION" "1Password.pkg"
