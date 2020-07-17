#!/usr/bin/env bash
##
##Dockerfile libraries
##
# correctly set rpi as the swarm master because docker-machine does
# not currently work against hypriot swarms
# This is for clusterlab swarms
set_docker_consul_master() {
    export SWARM_MASTER=${1:-${SWARM_MASTER:-"${USER}0"}}
    local full_hostname=$(add_local "$SWARM_MASTER")
    local swarm_master_ip=$(get_ip "$full_hostname")
    export DOCKER_HOST=${DOCKER_HOST:-"$swarm_master_ip:2378"}
    log_verbose using swarm  at DOCKER_HOST
    log_verbose turn off TLS verify for raspbian as TLS is not compatible with hypriot
    export DOCKER_TLS_VERIFY=
}

# detect the machine architecture and version if arm
# note only works with hypriot and does not work
# for clusters with different versions of the raspberry Pi
# as we do not know where a container will run
# The hypriot.arch is only for hypriot cluster lab
#
# This is more complicated now that Docker for Mac can run
# ARM containers
# http://blog.hypriot.com/post/first-touch-down-with-docker-for-mac/
# You just need to make sure /usr/bin/qemu-arm-static is in the container
docker_architecture() {
    local info=$(docker info)
    if [[ $info =~ "Architecture: x86_64" ]]
    then
        echo intel
    elif [[ $info =~ "hypriot.arch=armv6" ]]
    then
        echo rpi1
    elif [[ $info =~ "hypriot.arch=armv7l" ]]
    then
        echo rpi2
    elif [[ $info =~ "hypriot.arch=armv8" ]]
    then
        echo rpi3
    elif [[ $info =~ "Architecture: arm" ]]
    then
        echo rpi
    else
        exit 1
    fi
}

# start docker on a remote machine this only works for non-generic
# So do not use for rpi's or other machines that use the generic driver
# If you do not supply host then if docker-machine is active or DOCKER_HOST is
# active use docker-machine otherwise use the local docker command
# usage: docker_start [host [remote_account]]
docker_start() {
    if ! command -v docker > /dev/null
    then
        return 1
    fi

    # if no arguments then start what is default active
    if (( $# == 0 ))
    then
        # There is no docker daemon at all
        if ! docker info >/dev/null
        then
            return 1
        fi

        # start using docker-machine commands
        if docker-machine active
        then
            host=$(docker-machine active)
            docker-machine $host restart
            return
        fi

        # this is local so figure out if we are using systemd or upstart
        # Use command -v to look for the right module
        ctl=$(command -v systemctl || command -v service)

        # do not know how to start
        if [[ -z $ctl ]]
        then
            return 1
        fi

        if ! sudo "$ctl" docker status | grep -q running
        then
            eval sudo "$ctl" docker restart
            if ! sudo "$ctl" service docker status | grep -q running
            then
                return 1
            fi
        elif ! groups | grep -q docker
        then
            return 1
        fi
        return
    fi

    # we are using a remote system if non exists use default
    local host=${1:-default}
    local remote=${2:-localhost}

    # we must use ssh directly no docker machine available
    if ! docker-machine ls | grep "$host"
    then
        ssh "$remote" 'sudo $(command -v systemctl || command -v service) restart docker'
        return $?
    fi

    # there is docker machine but it is generic so must manually restart it
    if docker-machine ls | grep "$host.*generic"
    then
        # assume if not systemd using systemctl then it is upstart
        # using service command
        docker-machine ssh "$host" 'sudo $(command -v systemctl || command -v service) restart docker'
        return $?
    fi

    # otherwise all is working and we can use the docker-machine command
    docker-machine restart "$host"
    return $?

}

# check to see if docker is properly running
# defaults to local machine
docker_available() {
    if ! docker ps >/dev/null 2>&1
    then
        if [[ $OSTYPE =~ linux ]]
        then
            if sudo service docker status | grep -q running && ! groups | grep -q docker
            then
                log_verbose docker running but not in docker group use sudo or usermod -G docker
            fi
        fi
        return 1
    fi
}


# docker-machine machine-to-run true-if-you-want-to-force
# note that macs always use docker machine
# and the defaults are the machine is ml and we do not force
# usage: use_docker_machine machine [true|false]
use_docker_machine() {
    local machine=${1:-default}
    local force=${2:-false}
    if [[ $OSTYPE =~ darwin ]] || $force
    then
        if ! docker-machine status "$machine" | grep -q Running
        then
            docker-machine restart "$machine"
        elif ! docker-machine active >/dev/null 2>&1
        then
            eval $(docker-machine env "$machine")
        fi
    fi
}

# remove docker machine if needed
# rm_docker_machine [-f] machine,...
rm_docker_machine() {
    local flags=${1:-default}
    local force
    if [[ $flags =~ -f ]]
    then
        force="-f"
        shift
    else
        force=""
    fi
    local machines=${@:-default}
    for machine in $machines
    do
        if docker-machine status "$machine" 2>&1 >/dev/null
        then
            if docker-machine status "$machine" 2>/dev/null | grep -q Running
            then
                # the stop will not work if it is a generic as we use for the rpi
                docker-machine stop "$machine" || true
            fi
            docker-machine rm $force "$machine"
        fi
    done
}

# remove the container if it is already there so you do not get an error on
# docker run on a local machine
# docker_remove_container container-name
# This could be replaced by rm_docker_container localhost $@
# assuming ssh exists on the machine
# remove the container if it is already there so you do not get an error on
# docker run
# docker_remove_container container-name
docker_remove_container() {
    # note this will not run on a Mac properly because docker is not found
    # rm_docker_container localhost $@
    for container in $@
    do
        if ! docker_find_container "$container"
        then
            # http://container-solutions.com/understanding-volumes-docker/
            # -v means remove data volumes too
            docker stop "$container" || true
            docker rm -vf "$container"
        fi
    done
}

docker_find_container() {
    # local version does not run on a mac because docker is not visible via ssh
    # ps_docker_container localhost $@
    for container in $@
    do
        docker ps -a --filter name="$container" | grep -q "$container"
    done
}


# Find docker container somewhere
# Uses http://stackoverflow.com/questions/22107610/shell-script-run-function-from-script-over-ssh
# To copy a function over for ssh by printing all functions with typeset
# http://stackoverflow.com/questions/23264657/how-to-run-a-bash-function-in-a-remote-host-in-ubuntu
# show how to do with declear -f and call with parameters
ps_docker_container() {
    if (($# < 2)) ;then return 1; fi
    local remote="$1"
    local container="$2"
    ssh "$remote" ""$(declere -f docker_find_container)"; docker_find_container "$container""
}

# usage: rm_docker_container remote machine container
# note machine is right now unused
# usage: rm_docker_container remote [containers...]
rm_docker_container() {
    if (( $# < 2 )); then return 1; fi
    local remote="$1"
    shift
    for container in $@
    do
        log_verbose see if there was already a swarm process started if so stop
        if ps_docker_container "$remote" "$container"
        then
            # swarm-agent present stop and rm on $remote
            # switch to docker update --restart=unless-stopped when available on rpi
            ssh "$remote" ""$(declare -f docker_remove_container)"; docker_remove_container "$container""
        fi
    done
}

exec_output() {
    if [[ $# < 1 ]]; then return; fi
    if "$DOCKER_OUTPUT"
    then
        echo RUN $@
    else
        eval $@
    fi
}


package_output() {
    if [[ $# < 1 ]]; then return; fi

    # put each on a line and sort for uniqueness
    if $DOCKER_OUTPUT
    then
        printf "RUN apt-get update && apt-get install -y"
        printf ' \\\n    %s' $(echo $@ | xargs -n1 | sort -u )
        echo
    else
        sudo apt-get -y $NO_EXEC install $@
    fi
}


# create_hypriot_swarm_machine token hostname [additional flags...]
# creates a hypriot swarm member for the rpi set --swarm-master for one of them
# usage docker_machine_create_machine remote force-removal discovery_url [additional-docker-create-flags...]
docker_machine_create_swarm() {
    if (( $# < 3 )); then return 1; fi
    local remote="$1"
    local force="$2"
    local discovery="$3"
    shift 3
    local flags="$@"
    local ip=$(get_ip "$remote")
    local user=$(get_user "$remote")
    local host=$(get_host "$remote")
    local machine=$(remove_local "$host")

    if ! docker_machine_create \
        $remote \
        $force \
        --swarm \
        --swarm-discovery="$discovery" \
        --swarm-image hypriot/rpi-swarm:latest \
        $flags
    then
        if ssh "$remote" docker ps --filter "name=swarm-agent" | grep swarm-agent
        then
            log_warning swarm is already running so create worked
        else
            log_warning docker-machine could not be create for $machine
            return 1
        fi
    fi
}

# The underlying function called by the swarm using token or swarm using consul
# docker_machine_create remote force flags
docker_machine_create() {
    if (( $# < 2 )); then return 1; fi
    local remote="$1"
    local force="$2"
    shift 2
    local flags="$@"
    local ip=$(get_ip "$remote")
    local user=$(get_user "$remote")
    local host=$(get_host "$remote")
    local machine=$(remove_local "$host")
    log_verbose creating hypriot swarm at ip $ip for host $host with user $user as machine $machine
    if ! host_alive "$host"
    then
        log_warning could not find $host running on network skipping
        return
    fi
    remove_from_authorized_hosts "$host"
    if ! "$SCRIPT_DIR/is-rpi.sh" "$remote"
    then
        log_warning $remote is not a Raspberry Pi but will add to cluster anyway
    fi
    log_verbose stop and remove the containers to prevent error in docker-machine create $machine
    rm_docker_container "$remote" swarm-agent
    rm_docker_container "$remote" swarm-agent-master
    log_verbose remove existing docker machine $machine if necessary
    if $force
    then
        local force_flag=-f
    else
        local force_flag=""
    fi
    rm_docker_machine $force_flag "$machine"
    if $force && ssh "$remote" [[ -e /etc/docker/daemon.json ]]
    then
        log_warning before hypriot version 0.5.15 daemon.json had to be removed
        log_warning disabling /etc/docker/daemon.json on $remote not compatible with docker-machine
        ssh "$remote" "sudo systemctl stop docker &&
                       sudo mv /etc/docker/daemon.json /etc/docker/daemon.$$.json &&
                       sudo systemctl start docker"
    fi
    log_verbose  make sure docker is running on the machine
    docker_start "$machine" "$remote"
    log_verbose creating $machine
    if ! docker-machine create \
        --driver generic \
        --generic-ip-address="$ip" \
        --generic-ssh-user="$user" \
        --engine-storage-driver=overlay \
        $flags \
        "$machine"
    then
        return !?
    fi
}
