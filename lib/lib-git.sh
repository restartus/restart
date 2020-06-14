#!/usr/bin/env bash
##
##
## helper functions for git management
## @author rich
##
##
## git_check_connection git-key
##
## git_install_or_update [ -f ] repo [ organization ]
## Remember use only local variables!
## Assumes HOME and SCRIPTNAME are set
## 

## git_get_org returns as a string the name of the organization for this repo
## git_organization [ directory to check ]
git_organization() {    
    # this needs to change when you fork the repo
    # first get the front half
    dir="$PWD"
    # if there is an argument use it
    if [[ $# > 1 ]]
    then
      dir="$1"
    fi
    
    if [[ ! -e $dir ]]
    then
      return
    fi

    pushd "$dir" >/dev/null
    org="$(git remote get-url origin)"
    # expect a string like http://github.com/org/repo or
    # git@github.com:org/repo
    # strip off up the last slash and only up to there and only up to there
    # https://stackoverflow.com/questions/10535985/how-to-remove-filename-prefix-with-a-posix-shell
    # https://www.linuxjournal.com/content/pattern-matching-bash
    # remove up to the first slash you find
    org="${org%/*}"
    org="${org##*[:/]}"
    # consume everything up the last colon or slash you find
    export org="${org#$*[:/]}"
    popd >/dev/null

    echo $org
}

## git_set_ssh repo switch the remote pull to ssh from https
## https://gist.github.com/m14t/3056747
## usage: git_set_ssh repo path_to_git
git_set_ssh(){
    local repo=${1:-"$src"}
    local git_dir=${2:-"$WS_DIR/git"}
    cd "$git_dir/$repo" 
    if ! git status
    then
        >&2 echo $FUNCNAME: $repo is not a git repo
        return 1
    fi
    local url=$(git remote -v | grep -m1 '^origin' | sed -Ene's#.*(https://[^[:space:]]*).*#\1#p')
    if [[ -z $url ]]
    then
        log_verbose $repo already uses ssh
        return 0
    fi
    git remote set-url origin "git@github.com:${url#https://github.com/}"
    cd -

}

## git_set_config variable value
git_set_config() {
	if (( $# != 2 ))
	then
		return 1
	fi
	if ! git config --get "$1"
	then
		git config --global "$1" "$2"
	fi
}

## usage: git_install_or_update [-f] repo [user [ destination ]]
##
## examples git_install_or_update -f src
##          git_install_or_update rpi-motion-mmal jritsma
##          git_install_or_update flash hypriot "$WS_DIR/cache"
##          git_install_or_update "https://gist.github.com/schickling/2c48da462a7def0a577e" docker-machine-import-export
##
git_install_or_update() {
    local return_code=0
    
    if (( $# < 1 ))
    then
        >&2 echo $FUNCNAME: missing repo to update
        return_code=1
    fi

    # -f means force reset to origin/master
    if [[ $1 == -f ]]
    then
        git_command='git fetch --all && 
                     git reset --hard origin/master && 
                     git checkout master && 
        		     git pull'
        shift
    else
        # handles the case that we are in detached head mode
        # http://git-blame.blogspot.com/2013/06/checking-current-branch-programatically.html
        git_command='if ! git symbolic-ref HEAD;
                     then
                         git checkout master;
                     fi &&
                     git pull'
    fi
    if [[ $1 =~ ^https ]]
    then
        local repo="${2:-$(basename "$1")}"
        local full_repo_name="$1"
    else
        local repo=$1
        local full_repo_name="${2:-"richtong"}/$1"
    fi
    local git_dir="${3:-"$WS_DIR/git"}"

    mkdir -p "$git_dir"

    if cd "$git_dir/$repo" 2>/dev/null
    then
        if ! eval $git_command
        then
            >&2 echo $FUNCNAME: in $repo, $git_command failed
	    return_code=2
        fi
	cd -
    elif cd "$git_dir"
    then
        if [[ ! $full_repo_name =~ ^https ]]
        then
            full_repo_name="git@github.com:$full_repo_name"
        fi

    	if ! git clone "$full_repo_name" "$repo"
        then 
            >&2 echo $FUNCNAME: git clone "$full_repo_name" failed
            return_code=3
        fi
        cd -
    else
        >&2 echo $FUNCNAME: no $git_dir found
        return_code=4
    fi

    return "$return_code"
}
