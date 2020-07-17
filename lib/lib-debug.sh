#!/usr/bin/env bash
##
## library bash functions and debugging single stepping
## source these into your script
##
## This will export the DEBUGGING and VERBOSE LOG_FLAGS and set them if not already
## done. You should run this before set -u and after you run getopts
##
# comparison tools


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

    # Debug tools
    export DEBUG_SUSPEND=${DEBUG_SUSPEND:-false}
    export DEBUGGING=${DEBUGGING:-false}
    export VERBOSE=${VERBOSE:-false}
    export LOG_FLAGS=${LOGFLAGS:-""}


    log_message() {
        # if localization exists use it
        if command -v gettext >/dev/null
        then
            echo $(gettext -s $SCRIPTNAME): $(gettext -s "$@")
        else
            echo $SCRIPTNAME: $@
        fi
    }

    # usage: log_file [ files... ] > stdout
    log_file() {
        for file in $@
        do
            log_message $file:
            cat "$file"
            echo
        done
    }

    # gettext does localization but can not depend on it always being theree
    log_verbose() {
        if $VERBOSE
        then
            # bashism to redirect to stderr (fd 2)
            >&2 log_message $@
        fi
    }

    # only dump files if VERBOSE set
    log_verbose_file() {
        if $VERBOSE
        then
            >&2 log_file $@
        fi
    }

    log_debug() {
        if $DEBUGGING
        then
            >&2 log_message $@
        fi
    }

    log_debug_file() {
        if $DEBUGGING
        then
            >&2 log_file $@
        fi
    }

    log_warning() {
        >&2 log_message $@
    }

    # log_error code "error message"
    log_error() {
        local code=${1:-1}
        shift
        >&2 log_message $@
        exit $code
    }

    # on success: log_exit "message"
    log_exit() {
        log_verbose $*
        exit
    }

    # note the bash expression for test should look like [[ expression ]]
    # and for statements like ! command -v node
    # usage: assert "bash expression"  ["assertion comment"]
    log_assert() {
        if (( $# < 1 )); then return; fi
        local assertion=${2:-$1}
        if ! eval $1 > /dev/null
        then
            log_warning "Failed $1: no $assertion"
            return 1
        fi
    }

    # When trace is off we temporarily stop debugging but remember so trace off
    # works
    trace_on() {
        # -x is x-ray or detailed trace, -v is verbose, trap DEBUG single steps
        if $DEBUG_SUSPEND
        then
            DEBUG_SUSPEND=false
            DEBUGGING=true
        fi
        if $DEBUGGING
        then
            if [[ ! $LOG_FLAGS =~ -d ]]
            then
                LOG_FLAGS+=" -d"
            fi
            set -vx -o functrace
            trap '(read -p "[$BASH_SOURCE:$LINENO] $BASH_COMMAND?")' DEBUG
        fi
    }

    trace_off() {
        if $DEBUGGING
        then
            DEBUG_SUSPEND=true
            DEBUGGING=false
            if [[ $LOG_FLAGS =~ -d ]]
            then
                LOG_FLAGS=${LOG_FLAGS//d/}
            fi
            trap - DEBUG
        fi
    }

    if "$DEBUGGING"
    then
        trace_on
    fi


    if "$VERBOSE"
    then
        if [[ ! $LOG_FLAGS =~ -v ]]
        then
            LOG_FLAGS+=" -v"
        fi
    fi

    log_verbose "LOG_FLAGS set to $LOG_FLAGS"
fi
