#!/usr/bin/env bash
##
## utility functions for @rich
## Note that in these libraries you should not assume include.sh is loaded
## So do not use log_verbose etc.
##

## Note the if makes sure we only source once which is more efficient


# create a variable that is just the filename without an extension
lib_name="$(basename ${BASH_SOURCE%.*})"
# dashes are not legal in bash names
lib_name=${lib_name//-/_}
#echo trying $lib_name
# This is how to create a pointer by reference in bash so
# it checks for the existance of the variable named in $lib_name
# not how we use the escaped $ to get the reference
#echo eval [[ -z \${$lib_name-} ]] returns
#eval [[ -z \${$lib_name-} ]]
#echo $?
if eval [[ -z \${$lib_name-} ]]
then
    # how to do an indirect reference
    eval $lib_name=true

    # usage: util_sudo [-u user ] [files to be accessed]
    # return the text "sudo" if any of the files are not writeable
    # example: eval $(util_sudo_if /Volumes) mkdir -p /Volumes/<ext>
    util_sudo_if() {
      # https://www.cyberciti.biz/faq/unix-linux-shell-scripting-test-if-filewritable/
      user=root
      if [[ $1 == -u ]]
      then
        shift
        user="$1"
        shift
      fi

      for file in "$@"
      do
        if [[ ! -w $file ]]
        then
          echo sudo -u "$user"
          break
        fi
      done
      }

    # usage: util_group file
    # returns on stdout the
    # https://superuser.com/questions/581989/bash-find-directory-group-owner
    util_group() {
        if (( $# == 0 )); then return 1;fi
	if [[ $OSTYPE =~ darwin && $(command -v stat) =~ /usr/bin/stat ]]
        then
            local flags="-f %Sg"
        else
            local flags="-c %G"
        fi
        stat $flags $@
    }

    # backup a file keep iterating until you find a free name
    # usage: util_backup files..
    util_backup() {
        for file in $@
        do
            if [[ ! -e $file ]]
            then
                continue
            fi
            i=""
            while :
            do
                backup="$file$i.bak"
                if [[ ! -e $backup ]]
                then
                    cp "$file" "$backup"
                    break
                fi
                # if diff is true then the files are the same we do not need to
                # backup
                if diff "$file" "$backup" >/dev/null
                then
                    break
                fi
                ((++i))
            done
        done
    }

    # Get the profiles loaded into this script
    # needed when updating paths and want to immediately use the new
    # commands in the running script
    source_profile() {
        pushd ${1:-"$HOME"} >/dev/null
        for file in .profile .bash_profile .bashrc
        do
            if [[ -e "$file" ]]
            then
                # turn off undefined variable checking because
                # scripts like bash completion reference undefined
                # And ignore errors in profiles
                set +u
                source "$file" || true
                set -u
            fi
        done
        popd
        # rehash in case the path changes changes the execution order
        hash -r
    }

    # check if a directory is empty
    # usage: dirempty [directory list...]
    # returns: 0 if all are empty, error code is number of subdirectory entries
    dir_empty() {
        if (( $# == 0 )); then return 0; fi
        local dirs="$1"
        count=$(ls -A $dirs | wc -l)
        return $count
    }

    # takes the standard input and adds pretty spaces
    # and an indent
    # usage: indent_output amount_of_indent
    # https://unix.stackexchange.com/questions/148109/shifting-command-output-to-the-right
    indent_output() {
        local indent=${1:-8}
        tr "[:blank:] " "\n" | nl -bn -w $indent
    }


    # usage: in_ssh returns 0 if in an ssh session
    # need the the - syntax to prevent -u from calling SSH_CLIENT unbounded
    in_ssh() {
        if [[ -n ${SSH_CLIENT-} || -n ${SSH_TTY-} ]]
        then
            return 0
        else
            return 1
        fi
    }

    # usage: promot_user questions bash_command
    prompt_user() {
        if (( $# < 2 )); then return 1; fi
        local question="$1"
        local cmd="$2"
        # https://stackoverflow.com/questions/2642585/read-a-variable-in-bash-with-a-default-value
        # http://wiki.bash-hackers.org/commands/builtin/read
        # -e means if stdin from a terminal use readline so more features on input
        # -i sets default requires -e
        # -t times out so this still works in batch mode
        # -r disables escapes
        read -re -t 5 -i Yes -p "$question? " response
        # the ,, makes it lower case
        if [[ ${response,,} =~ ^y ]]
        then
            # https://unix.stackexchange.com/questions/296838/whats-the-difference-between-eval-and-exec
            eval $cmd
        fi
    }

    has_nvidia() {
        if [[ $OSTYPE =~ linux ]] && lspci | grep -q 'VGA.*NVIDIA'
        then
            return 0
        else
            return 1
        fi
    }

    # use the test to avoid set -e problems
    in_vmware_fusion() {
        if [[ $OSTYPE =~ linux ]] && lspci | grep -q VMware
        then
        return 0
        else
            return 1
        fi
    }

    service_start() {
        local svc=${1:-docker}
        local state=$(sudo service "$svc" status)
        case "$state" in
            *running*)
                # Try upstart first, if it fails try systemd
                if ! sudo restart "$svc"
                then
                    sudo systemctl restart "$svc"
                fi
                ;;
            *stop*)
                if ! sudo start "$svc"
                then
                    sudo systemctl start "$svc"
                fi
                ;;
            *)
                # strange state $svc for $state just return
                ;;
        esac
    }

    linux_distribution() {
        if [[ $(uname) =~ Linux ]]
        then
            echo $(lsb_release -i | awk '{print $3}' | tr '[:upper:]' '[:lower:]')
        fi
    }

    # usage: in_linux [ ubuntu | debian ]
    in_linux() {
        if (( $# < 1 ))
        then
            return 0
        fi
        if [[ $(linux_distribution) =~ $1 ]]
        then
            return 0
        else
            return 1
        fi
    }

    # usage: linux_version
    linux_version() {
        lsb_release -r | cut -f 2
    }

    # usage: linux_codename
    linux_codename() {
	    # echo $(linux_distribution)
        case $(linux_distribution) in
            ubuntu)
		  # echo ubuntu
		  # echo $(linux_version)
                case $(linux_version) in
		19.10*)
			echo eoan
			;;
		19.04*)
			echo disco
			;;
		18.10*)
			echo cosmic
			;;
	    	18.04*)
			echo bionic
			;;
                    17.10*)
                        echo artful
                        ;;
                    17.04*)
                        echo zesty
                        ;;
                    16.10*)
                        echo yakkety
                        ;;
                    16.04*)
                        echo xenial
                        ;;
                    15.10*)
                        echo wily
                        ;;
                    15.04*)
                        echo vivid
                        ;;
                    14.10*)
                        echo utopic
                        ;;
                    14.04*)
                        echo trusty
                        ;;
                    13.10*)
                        echo saucy
                        ;;
                    13.04*)
                        echo raring
                        ;;
                    12.10*)
                        echo quantal
                        ;;
                    12.04*)
                        echo precise
                        ;;
                    *)
			 # echo not found
                        return 1
                        ;;
                esac
                ;;
            debian)
		    # echo debian
                # https://en.wikipedia.org/wiki/Debian_version_history
                case $(linux_version) in
                    10*)
                        echo buster
                        ;;
                    9*)
                        echo stretch
                        ;;
                    8*)
                        echo jessie
                        ;;
                    7*)
                        echo wheezy
                        ;;
                    6*)
                        echo squeeze
                        ;;
                    *)
		 	# echo not found
                        return 1
                esac
        esac


    }


    # usage desktop_environment
    # returns [[ xfce || gnome || ubuntu ]]
    # https://unix.stackexchange.com/questions/116539/how-to-detect-the-desktop-environment-in-a-bash-script
    desktop_environment() {
        if [[ ! $OSTYPE =~ linux ]]
        then
            return
        # need the {-} construction so that when XDG is unbound we do not generate
        # an error
        elif in_ssh
        then
            return
        elif [[ -n ${XDG_CURRENT_DESKTOP-} ]]
        then
            echo "$XDG_CURRENT_DESKTOP" | tr '[:upper:]' '[:lower:]'
        else
            echo "${XDG_DATA_DIRS-}" | grep -Eo 'xfce|kde|gnome|unity'
        fi
    }

    util_os() {
        case $OSTYPE in
            darwin*)
                echo mac
                ;;
            linux*)
		if [[ -n $WSL_DISTRO_NAME ]]
		then
			echo windows
		else
			echo linux
		fi
                ;;
        esac
    }

    # Usage: in_os [ mac | windows | linux ]
    in_os() {
        if (( $# < 1 ))
        then
            return 0
        fi
	    if [[ ! $(util_os) =~ $1 ]]
	    then
		    return 1
	    fi
    }

    # determine the location of the stow subdirectory
    # usage: util_full_version
    # stdout returns the normalized full name os.major.minor...
    util_full_version() {
        case $OSTYPE in
            darwin*)
                # darwin version is simpler than the Macos version
                # https://en.wikipedia.org/wiki/MacOS
                # Note that 16 = Sierra, 15=El Capitan,...
                # https://stackoverflow.com/questions/9913942/check-version-of-os-then-issue-a-command-if-the-correct-version
                # But we use the user visible version
                echo macos.$(sw_vers -productVersion)
                ;;
            linux*)
                echo linux.$(linux_distribution).$(linux_version)
                ;;
            *)
                return 1
        esac
    }

    # run a file if it exists
    run_if() {
        if [[ $# < 1 ]]
        then
            return 1
        fi
        if [[ -r $1 ]]
        then
            "$SHELL" $@
            fi
    }

fi
