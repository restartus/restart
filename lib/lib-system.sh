#!/usr/bin/env bash
##
## library bash functions and debugging single stepping
## source these into your script
##

# starting and stoppping the surround.io system
run_web_server() {
    # Now run the system, first start the web server, then the app-host
    python "$WS_DIR/git/src/platform/http-server/api/__init__.py" &
    local web_server_pid=$!
    # subtle bug here, log_verbose echo will return false but the if does not
    log_verbose web server started at $web_server_pid
}
run_app_host() {
    # Need to run wscons with /dev/null to get it to run in the backgroun
    cd "$WS_DIR/git/src"
    wvrun app-host </dev/null &
    local app_host_pid=$!
    log_verbose echo app-host started at $app_host_pid
    cd -
}
kill_system() {
    # note we cannot use && as pgrep returns an error if not found
    if pgrep -u "$USER" python
    then
        pkill -u "$USER" python
    fi
    if pgrep -u "$USER" app-host
    then
        pkill -u "$USER" app-host
    fi
}
run_system() {
    # Run the test if not already there
    pgrep -u "$USER" python || run_web_server
    pgrep -u "$USER" app-host || run_app_host
}
