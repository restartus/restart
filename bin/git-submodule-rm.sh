#!/usr/bin/env bash
##
## Change the origin of a cloned submodule
## This is actually much hard than it looks there do not seem to
## https://gist.github.com/myusuf3/7f645819ded92bda6677
##
##@author Rich Tong
##@returns 0 on success
#
# https://stackoverflow.com/questions/4604486/how-do-i-move-an-existing-git-submodule-within-a-git-repository
# Note: if you just want to move a submodule within your tree
# git mv old/submodule new/submodule now works.
#
# This is the way to do with command line
#  https://stackoverflow.com/questions/60003502/git-how-to-change-url-path-of-a-submodule
#
# git config --file=.gitmodules submodule.Submod.url _new path_
# git config --file=.gitmodules submodule.Submod.branch Development
# git submodule sync
# This command means update all the module, initialize if they don't exis
# If there are submodules nested, keep traversing donw
# Sync with the remote
# git submodule update --init --recursive --remote
#
# This is the oldest way to do by manually hacking
# https://stackoverflow.com/questions/10317676/git-change-origin-of-cloned-submodule
# 1. change the url entry in .gitmodules
# 2. change the url entry in .git/config
# https://help.github.com/en/github/using-git/changing-a-remotes-url
# 3. git submodule sync --recursive or git remote set-url
#
#
set -u && SCRIPTNAME="$(basename "${BASH_SOURCE[0]}")"
SCRIPT_DIR=${SCRIPT_DIR:=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}
# this replace set -e by running exit on any error use for bashdb
trap 'exit $?' ERR
OPTIND=1
MAIN="${MAIN:-""}"
REPOS="${REPOS:-""}"
FORCE="${FORCE:-false}"
export FLAGS="${FLAGS:-""}"
while getopts "hdvm:" opt
do
    case "$opt" in
        h)
            cat <<-EOF
    Delete git submodule
    usage: $SCRIPTNAME [ flags ] [ submodule_within_main_repo_full_relative_to_main ]
    flags: -d debug, -v verbose, -h help
           -m main repo the default is set in SOURCE_DIR
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
        m)
          MAIN="$OPTARG"
            ;;
    esac
done
shift $((OPTIND-1))
if [[ -e "$SCRIPT_DIR/include.sh" ]]; then source "$SCRIPT_DIR/include.sh"; fi
source_lib lib-util.sh

if ! in_os mac
then
    log_warning only tested on the Mac
fi

if [[ -z $MAIN ]]
then
  MAIN="$SOURCE_DIR/extern"
fi
log_verbose root of git parent is $MAIN

log_verbose arguments left are $#
if [[ $# > 0 ]]
then
  log_verbose found arguments taking set REPOS to  $@
  REPOS="$@"
fi
log_verbose moving to $MAIN
pushd "$MAIN" >/dev/null
log_verbose looking for $REPOS
for repo_path in $REPOS
do
  repo=$(realpath --relative-to="$MAIN" "$repo_path")
  log_verbose cleaning $repo relative to $MAIN
  if [[ ! -e $repo ]]
  then
    log_warning $MAIN/$repo does not exist skipping
    continue
  fi
  log_verbose deinit
  if ! git submodule deinit "$repo"
  then
    log_warning no inited submodule "$repo"
  fi
  log_verbose remove "$repo"
  if ! git rm -rf "$repo"
  then
    log_warning git does not track $repo trying to use regular rm
    rm -rf "$repo"
  fi
  if [[ -e ".git/modules/$repo" ]]
  then
    log_verbose remote .git/modules/$repo
    rm -rf ".git/modules/$repo"
  fi
  git commit -m "Deleted submodule $repo"
done
popd >/dev/null
