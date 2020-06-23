#!/usr/bin/env bash
##
##Installation works on either Mac OS X (Darwin) or Ubuntu
## vi: se et ai sw=2 :
##

# create a variable that is just the filename without an extension
lib_name="$(basename ${BASH_SOURCE%.*})"
# dashes are not allowed in bash variable names so make them underscores
lib_name=${lib_name//-/_}
# This is how to create a pointer by reference in bash so
# it checks for the existance of the variable named in $lib_name
# not how we use the escaped $ to get the reference
if eval [[ -z \${$lib_name-} ]]
then
    # how to do an indirect reference
    eval $lib_name=true

    # add a directory to the path
    # usage path_add [ directories ]
    # deprecated and line_add_replace does not exist
    #path_add() {
    #    for bin in $@
    #    do
    #        if [[ -d $bin && ! $PATH =~ $bin ]]
    #        then
    #            line_add_or_replace "PATH.*$bin" "$PATH+=\"$bin:\""
    #        fi
    #    done
    #}

    # initialize package managers and update them all 
    # usage: package_update 
    package_update() {
        local output='> /dev/null'
        if $VERBOSE
        then
            output=""
        fi
        if [[ $OSTYPE =~ darwin ]]
        then
            # use eval to pipe if needed for verbosity
            if command -v brew > /dev/null
            then
                # Need eval because of the $output
                eval brew update $output
                # ignore upgrade errors
                eval brew upgrade $output || false
            fi
            if command -v port > /dev/null
            then
                # https://guide.macports.org
                # -N means noninteractive
                # Need eval because of the $output
                eval sudo port -N selfupdate $output
                # returns an error if nothing to upgrade ignore it
                eval sudo port -N upgrade outdated $output || true
            fi
            return
        fi
        eval sudo apt-get update $output
        eval sudo apt-get upgrade $output
    }

    # usage: tap_install [ taps... ]
    tap_install() {
        for tap in $@
        do
            if ! brew tap | grep -q "^$tap"
            then
                brew tap "$tap"
            fi
        done
    }
    
    # usage: cask_is_installed [ casks... ]
    # returns: 0 if installed, otherwise number of casks not installed
    cask_is_installed() {
        # https://askubuntu.com/questions/385528/how-to-increment-a-variable-in-bash
        # performance better if you declare an integer
        declare -i missing=0
        for cask in $@
        do
            if ! brew cask list "$cask"  > /dev/null 2>&1
            then
                # remember if the return value is a zero this fails or
                # preincrement
                ((++missing))
            fi
        done
        return $missing
    }

    # Mac Brew installations for full Mac applications called casks
    # Note if the cask is already installed it will upgrade it
    # this only works if the cask is already tapped
    # so names of the form 'user/tap/cask' will not work
    # usage: cask_install [ casks...]
    # returns: number of install errors
    cask_install() {
        local output=">/dev/null 2>&1"
        local errors=0
        if $VERBOSE
        then 
            output=""
        fi

        for cask in $@
        do
            local brew_cask="$(brew cask info "$cask" 2>&1)"
            # for some reason a here string fails maybe too long
            # Note we use the quoted variable so we can see the lines
            if ! echo "$brew_cask" | head -n 1 | grep -q "^$cask"
            then
                # this is not a cask so skip
                continue
            fi
            if cask_is_installed "$cask"
            then
                # found it already there make sure it is up to date
                brew cask upgrade $cask
                continue
            fi
            # assumes Artifacts are last and right after the Artifact word using
            # cut to get the 3rd word and on
            # Note we need to quote $brew_cask to get the actual new lines
            # https://stackoverflow.com/questions/613572/capturing-multiple-line-output-into-a-bash-variable
            # https://stackoverflow.com/questions/339483/how-can-i-remove-the-first-line-of-a-text-file-using-bash-sed-script
            # https://stackoverflow.com/questions/7103531/how-to-get-the-part-of-file-after-the-line-that-matches-grep-expression-first
            local artifacts="$(echo "$brew_cask" | sed -n '/^==> Artifacts/,$p' | tail -n +2)"
            log_verbose found artifacts "$artifacts"
            local exists=0

            # Now loop through all users turn off debug because the trap is not compatible
            # with the read loop. Annoying but single stepping doesn't work otherwise
            if $DEBUGGING; then trace_off; fi
            log_verbose running through "$artifacts" with a while loop
            while read artifact
            do
                log_verbose found $artifact removing \(type\) suffix
                # use a single % so it not greedy, just finds the first space in
                # the string
                artifact=${artifact% *(*)}
                log_verbose stripped $artifact processing
                case "$artifact" in
                    \(*\))
                        # skip things in parentheses these are type identifiers
                        log_verbose ignoring artifact
                        continue
                        ;;
                    \/*)
                        # a leading slash means a path
                        log_verbose checking for $artifact
                        if [[ -e $artifact ]]
                        then
                            ((++exists))
                            log_verbose $artifact exists and $exists so far
                        fi
                        ;;
                    *.app*)
                        log_verbose checking in /Applications
                        # remove the (app) that follows
                        if [[ -e /Applications/$artifact ]]
                        then
                            ((++exists))
                            log_verbose $artifact exists and $exists so far
                        fi
                        ;;
                esac
            done <<<"$artifacts"
            # Annoying but trace needs to be turned off
            if $DEBUGGING; then trace_on; fi

            # we found an existing artifact
            log_verbose checking to see how many $artifacts exists found $exists do
            if (( $exists > 0 ))
            then
                # existance is not an error 
                # ((++errors))
                log_verbose $cask has $exists artifacts already installed skipping
                continue
            fi
            # if there are artifacts already there from other installers
            # found a brew cask now see if it is installed
            log_verbose no artifacts exists seeing if $cask installed
            if grep -q "Not installed" <<<"$brew_cask"
            then
                log_verbose installing brew cask
                # if verbose we show all the install commands
                if ! eval brew cask install $cask $output
                then
                    ((++errors))
                    log_verbose $cask installed failed with $errors errors
                fi
            fi
        done
        return $errors
    }

    cask_uninstall() {
        for package in $@
        do
            # it is ok if it isn't actually there
            brew cask uninstall "$package" >/dev/null 2>&1 || true
        done
    }

    # swaps the first cask for the second
    # if you provide an odd number of casks then it will just do a cask_install
    # on the last one
    # usage: cask_swap [[ new_cask old_cask new_cask1 old_cask1... ]]
    cask_swap() {
        # note this works even if things are even because
        # cask_install and cask_uninstall can deal with zero arguments
        while (($# > 0 ))
        do
          cask_uninstall "$2"
          cask_install "$1"
          # note this shift won't work if $# is odd so if we have just a singleton
          # then we fail the loop, because shift 2 won't work
          # if there is only one argument and we are done
          # this has the effect of making cask_swap cask the same as
          # cask_install cask
          if (( $# == 1 ))
          then
            break
          fi
          # now get the next two casks to swap
          shift 2
        done
    }



    # https://unix.stackexchange.com/questions/265267/bash-converting-path-names-for-sed-so-they-escape
    # Uses bash substring replacement
    flags_to_grep() {
        echo "${1//-/\\-}"
    }
    # Mac Brew installations for simple packages called bottles
    # for things like grep, this disables adding g to it
    # usage: brew_install [flags] [bottles...]
    # some brew packages cannot be installed over each other
    # so check first
    brew_install() {
      for package in $@
      do
        if ! is_package_installed "$package"
        then
          # ignore errors
          brew install "$package" || true
        else
          # ignore errors
          brew upgrade "$package" || true
        fi
      done
    }

    brew_uninstall() {
        brew uninstall $@
    }

    # Mercurial install into the current working directory
    # hg_install url_of_repo [parent_dir_of_local_repo]
    hg_install() {
        if [[ $# < 1 ]]; then return 1; fi
        local url=$1
        local repo=$(basename "$url")
        local dir=${2:-"$WS_DIR/git"}
        mkdir -p "$dir"
        pushd "$dir" > /dev/null
        if [[ ! -d "$repo" ]]
        then
            hg clone "$url" "$repo"
        else
            pushd "$repo" > /dev/null
            hg pull
            hg update
            popd >/dev/null
        fi
        popd > /dev/null
    }

    # Apt repository install
    # usage: repository_install [ppa:team/repo | single_repo string]
    repository_install() {
        if [[ $# < 1 ]]
        then
            return 1
        fi
        if [[ ! $OSTYPE =~ linux ]]
        then
            return 2
        fi
        # note that apt-add-repository does not duplicate add entries so can apply
        # multiple times
        sudo apt-add-repository -y "$@"
        sudo apt-get update -y
    }

    # install a modprobe package
    mod_install() {
        if [[ $# < 1 ]] 
        then
            return 1
        fi
        if [[ ! $OSTYPE =~ linux ]]
        then
            return 2
        fi
        for mod in $@
        do
            if ! lsmod | grep -q "$mod"
            then
                sudo modprobe "$mod"
            fi
            if ! grep -q "^$mod" /etc/modules
            then
                sudo tee -a /etc/modules <<<"$mod"
            fi
        done
    }

    # returns success if all the packages are installed
    # otherwise returns how many packages were not installed
    # for mac look in brew first then mac ports
    # Some special logic here to make sure the thing is installed with the right
    # flags it will uninstall if the flags are wrong and return install needed
    is_package_installed() {
        local count=0
        # looks for the flags and makes sure they are installed, if not then do
        # assumes brew is up to date
        # just run overall brew so all flags can pass though
        local flags=""
        for item in $@
        do
            # add all the flags
            if [[ ! $item =~ ^- ]]
            then
                # break on the first non flag
                break
            fi
            flags+=" $item "
            shift
        done
        for package in $@
        do
            if [[ ! $OSTYPE =~ darwin ]]
            then 
                # do the linux check
                if  ! dpkg -s "$package" | grep -q "ok installed"
                then
                    ((++count))
                fi
                continue
            fi
            # look for Mac apps in a cask
            # Note that search only searches for default Mac apps
            # so need to use info and for some reason head -n 1
            # cause brew cask info to fail
            local brew_cask="$(brew cask info "$package" 2>&1)"
            # Need the semicolon in case there is an error
            # asking how many packages with similar names as with
            # brew cask info parallel
            if grep -q "^$package:" <<<"$brew_cask"
            then
                # found a brew cask now see if it is installed
                if grep -q "Not installed" <<<"$brew_cask"
                then
                    ((++count))
                fi
                continue
            fi

            # now do the Mac checks
            # see if the package is installed by homebrew 
            brew_info="$(brew info "$package" 2>&1)"
            # need the a quotes for the echo to retain the newlines
            if ((  $? != 0 )) || echo "$brew_info" | grep -q "^Not installed"
            then
                # no package see if it is available on brew
                if is_brew_package "$package" >/dev/null
                then
                    # it is available on brew so note it and continue
                    ((++count))
                elif command -v port && ! port installed "$package" >/dev/null 2>&1
                then
                    # this is not a brew package so try macports
                    ((++count))
                fi
                # not available so go to the next
                continue
            fi
            # if there are no required flags and it is installed the package
            # and we go on to the next package
            if [[ -z $flags ]]
            then
                continue
            fi
            # if there are require flags for the package, see if we have them
            # http://stackoverflow.com/questions/20802320/detect-if-homebrew-package-is-installed
            # https://stackoverflow.com/questions/8833230/how-do-i-find-a-list-of-homebrews-installable-packages
            # brew reinstall --options does not work however 
            # https://github.com/Homebrew/legacy-homebrew/issues/38259
            # if it is a valid flag for the $package and it is not installed
            # then force an uninstall to get it
            quoted_flags="$(flags_to_grep "$flags")"
            # if the package has the required flags go on to the next
            if grep -q "$quoted_flags" <<<"$brew_info"
            then
                continue
            fi
            # the package does not have the needed flags
            if brew list "$package" 2>&1 | grep -q "$quoted_flags"
            then
                # if they are then uninstall the package to get ready
                # for an install later
                package_uninstall "$package"
                ((++count))
                continue
            fi
            # if the flags are not valid ignore them and say we have it
            # and the package is installed so we can just go ont
        done
        return $count
    }


    # are all the packages brew packages
    # usage: is_brew_package [ items... ]
    # return 0 is all are package otherwise the number of casks or bottles not found
    # stdout return the type of package either cask or regular brew
    # Can be used to run install (eg $(is_brew_package)_install)
    is_brew_package() {
        # need extglob http://www.gnu.org/software/bash/manual/bashref.html#Pattern-Matching
        # remember current settings and flip back
        local extglob_setting=$(shopt extglob | awk '{print $2}')
        local not_found=0
        if [[ $extglob_setting == off ]]
        then
            shopt -s extglob >/dev/null
        fi
        for item in $@
        do
            # note a case statement does not work here because it cannot match
            # with variable expansion os caskroom*$item*) does not match
            # although  *$item*) does work for shell patterns even with shopt
            # extglob set
            local search=$(brew search $item 2>/dev/null)
            # So use if then and full regex
            if grep -q "^caskroom.*\/$item$" <<<"$search"
            then
                echo cask
                continue
            fi
            if [[ $search =~ $item ]]
            then
                # the search could return a list of packages that match
                echo brew
                continue
            fi
            ((++not_found))
        done
        if [[ $extglob_setting == off ]]
        then
            shopt -u extglob >/dev/null
        fi
        return $not_found
    }


    # mac_package installs or uninstalls depending on the package manager
    # usage: mac_package operation package [flags...]
    package_do() {
        if [[ ! $OSTYPE =~ darwin ]]; then return; fi
        if (($# < 2)); then return 1;fi
        local operation="$1"
        local package="$2"
        local type="$(is_brew_package "$2")"
        shift 2
        local flags="$@"
        if [[ -z $type ]]
        then
            sudo port uninstall "$package"
            return $?
        fi
        # need the braces to get the type variable
        # and we want flags at the end for brew
        if ! ${type}_$operation "$package" $flags
        then
            return $?
        fi
    }

    # install a package on Mac OS X (aka Darwin) or linux
    # Assums that any flags at the front are passed to the underlying package
    # manager
    # On brew assumes you've tapped the right cask (eg added the right repo
    # usage: package_install [flags] [packages...]
    # returns: 0 if all packages installed otherwise the error code of the 
    # first install that failed
    package_install() {
        # find all the flags at the start
        local flags=""
        while [[ $1 =~ ^- ]]
        do
            flags+="$1 "
            shift
        done
        for package in $@
            do
                # do not check flags
                if is_package_installed "$flags" "$package"
                then
                    continue
                fi

                if [[ $OSTYPE =~ darwin ]]
                then 
                    package_do install "$package" $flags
                    continue
                fi

                if ! sudo apt-get install -y "$package"
                then
                    return $?
                fi
        done
    }

    #  package_uninstall -flags.. [packages...]
    # Will also make sure that the right flags are installed for brew
    package_uninstall()  {
        # consume the flags to pass on
        local flags=""
        while [[ $1 =~ ^- ]]
        do
            flags+=" $1 "
            shift
        done
        for package in $@
        do
            if ! is_package_installed "$package"
            then
                continue
            fi
            if [[ $OSTYPE =~ darwin ]]
            then
                package_do uninstall "$package" $flags
                continue
            fi
            # must be linux
            if ! sudo apt-get remove -y $flags "$package"
            then
                continue
            fi
        done
        # need to rehash commands other current bash will see old paths
        hash -r
    }

    # install python packages passing on flags
    # we have one special flag -f which means run sudo and must be the first one
    # usage: pip_install -f [python flags..] [packages...]
    pip_install() {
        local flags=""
        local use_sudo=""
        while [[ $1 =~ ^- ]]
        do
            # one flag is for us to force use of sudo
            if [[ $1 == -f ]]
            then
                use_sudo=sudo
                shift
            fi
            # rest of flats we pass on to pip
            flags+=" $1 "
            shift
        done
        for package in $@
        do
            # note we pass flags unquoted  so each is a separate flag
            # conditionally run sudo if asked
            eval $use_sudo pip install $flags "$package"
        done
    }


    ## bundle_install org repo
    bundle_install() {
        if (( $# != 2 ))
        then
            return 1
        fi
        if [[ ! -e "$HOME/.vim/bundle/$2" ]]
        then
            cd "$HOME/.vim/bundle" && \
            git clone "git@github.com:$1/$2"
        fi
    }

    ## npm install first checks for existance always does a global
    ## usage npm_install [any flag that begins with - like -g] package1,...
    npm_install() {
        if (( $# < 1 ))
        then
            return 0
        fi
        local flags=""
        # Look for and add for all flags beginning with a dash
        while [[ $1 =~ ^- ]]
        do
            flags+=" $1"
            shift
        done

        for package in $@
        do
            # https://ponderingdeveloper.com/2013/09/03/listing-globally-installed-npm-packages-and-version/
            # do not quote $flags so that each flag becomes a separate argument
            # again
            if ! npm list $flags --depth=0 $1 >/dev/null 2>&1
            then
                # try this without sudo
                # sudo npm install $flags $1
                npm install $flags $1
            fi
            shift
        done
    }
    # take md5 if non zero and check for it
    # if md5 is zero then check a non-zero sha256
    # check_sum file [ md5_checksum [sha256_checksum]]
    check_sum() {
        local dest=${1:-/dev/null}
        local md5=${2:-0}
        local sha256=${3:-0}
        # if no sum then we just say it works
        if [[ $md5 == 0 && $sha256 == 0 ]]
        then
            return 0
        elif [[ $md5 != 0 && ( $(md5sum "$dest" | cut -f1 -d' ') == $md5 ) ]]
        then
            return 0
        elif [[ $sha256 != 0 && ( $(sha256sum "$dest" | cut -f1 -d' ') == $sha256) ]]
        then
            return 0
        fi
        return 1
    }


    # will always download unless the md5sum matches or sha256sum
    # To use sha256 add it as the last argument and it overrides
    # the md5 value
    # Also if we recognize the file type will process them
    # if it is a tar, will return the actual file(s) on stdout that
    # were extracted
    #
    # usage: download_url url [dest_file [dest_dir [md5 [sha256]]]]
    # returns: list of file extracted or downloaded
    download_url() {
        if (( $# < 1 )); then return 1; fi
        local url="$1"
        local dest_dir="${3:-"$WS_DIR/cache"}"
        local dest="${2:-$dest_dir/$(basename "$url")}"
        local md5="${4:-0}"
        local sha256="${5:-0}"
        mkdir -p "$dest_dir"
        # If file exists and there is md5 sum, we assume the file download worked
        if [[ -e $dest ]] 
        then
            # if no md5 or sha supplied assume it worked
            # check_md5 succeeds on a zero so last test is 
            # check_sha256
            if check_sum "$dest" "$md5" "$sha256"
            then
                return 0
            fi
        fi
        # Use the resume feature to make sure you got it by first trying and if
        # http://www.cyberciti.biz/faq/curl-command-resume-broken-download/
        if ! curl -C - -L "$url" -o "$dest" 
        then
            # if we fail see if the return code doesn't allow -C for resume and retry
            # Amazon AWS for instance doesn't allow resume and returns 31
            # Private Internet Access servers return 33 for same issue
            # but we cannot capture this return code because the if returns true
            # so we just do a retry without resume
            curl -L "$url" -o "$dest" 
        fi
        check_sum "$dest" "$md5"
    }


    # download file and then attach or open as appropriate
    # this was  in lib-mac.sh
    # Usage: download_url_open url [[file] [download_directory]]
    # But now is in lib-install.sh and uses download_url
    download_url_open () {
        if [[ ! $OSTYPE =~ darwin ]]; then return 0; fi
        if (( $# < 1 )); then return 1; fi
        local url="$1"
        # http://stackoverflow.com/questions/965053/extract-filename-and-extension-in-bash
        local file="${2:-${url##*/}}"
        local dest="${3:-"$WS_DIR/cache"}"
        local extension="${file##*.}"
        echo download_url_open file is $file dest is $dest and ext is $extension
        pushd "$dest" >/dev/null
        download_url "$url" "$file" "$dest"
        case "$extension" in
            deb)
                sudo dpkg -i "$file"
                ;;
            dmg)
                # do not mount if it has been already
                if ! hdiutil info | grep -q "$file"
                then
                    hdiutil attach "$file"
                fi
                ;;
            vbox-extpack)
                open "$file"
                ;;
            pkg)
                # packages can be batch installed
                sudo installer -pkg "$file" -target /
                ;;
            tar)
                tar xzf "$file"
                ;;
            gz)
                open "$file"
                ;;
            zip)
                # unpack the file
                unzip "$file"
                # If the file unpacked into an app move it
                local app="${file%.*}.app"
                if [[  -e $app ]]
                then
                    install_in_dir "$app"
                fi
                # try again trying to strip version numbers and junk from name
                app=${app%.*}.app
                if [[  -e $app ]]
                then
                    install_in_dir "$app"
                fi
                pref=${file%.*}.prefPane
                if [[ -e $pref ]]
                then
                    install_in_dir "$pref" "/Library/PreferencePanes"
                fi
                # try again trying to strip version numbers and junk from name
                pref=${pref%_*}.prefPane
                if [[ -e $pref ]]
                then
                    install_in_dir "$pref" "/Library/PreferencePanes"
                fi
                # check to see if this is a pkg
                # https://stackoverflow.com/questions/407184/how-to-check-the-extension-of-a-filename-in-a-bash-script
                # https://apple.stackexchange.com/questions/72226/installing-pkg-with-terminal
                # see if the zip file is a package
                pkg=${file%.*}
                if [[ -e $pkg ]]
                then
                  echo trying pkg install of $pkg
                  sudo installer -pkg "$pkg" -target /
                fi

                ;;
        esac
        popd >/dev/null
    }

    # usage: extract_tar tarfile
    # note tar returns to stdin all the files extract
    extract_tar() {
        if (( $# < 1 )); then return 1; fi
        local tar="$1"
        local files=$(tar -tf "$tar")
        for file in $files
        do
            # need to echo since the caller needs names of files
            # even if already extracted
            echo "$file"
            if [[ ! -e "$file" ]]
            then
                tar -xf "$tar" "$file"
            fi
        done
    } 

    # Downloads and checkes the pgp signature against the signer
    # https://www.gnupg.org/gph/en/manual/x135.html
    # usage: pgp_download $file_url $file_pgp_url $signer_url 
    download_url_pgp() {
        if (( $# < 3)); then return 1; fi
        local url="$(eval echo $1)"
        local signature_url="$(eval echo $2)"
        local signer_url="$(eval echo $3)"
        # does an eval if you have varible
        download_url "$url"
        download_url "$signature_url"
        download_url "$signer_url"
        file="$WS_DIR/cache/$(basename "$url")"
        signature="$WS_DIR/cache/$(basename "$signature_url")" 
        signer="$WS_DIR/cache/$(basename "$signer_url")"
        gpg --import "$signer"
        if ! gpg --verify "$signature" "$file" 2>&1 | grep -q "Good signature"
        then
            return 1
        fi
    }
    # install a debian package and check if it already exists
    # the last parameters are fed directly to download_url and must match
    # usage: deb_install debian-package-name url [dest_file [dest_dir [md5 [sha256]]]]
    # the rest of the parameters are passed onto download_url
    deb_install() {
        if (( $# < 2 )); then return 1; fi
        local package="$1"
        local url="$2"
        local dest="${3:-"$(basename "$url")"}"
        local dest_dir="${4:-"$WS_DIR/cache"}"
        if dpkg-query -l | awk '{print $2}' | grep -q "^$package"
        then
            return
        else
            shift
            download_url $@
        fi
        sudo dpkg -i "$dest_dir/$dest"
    }

fi
