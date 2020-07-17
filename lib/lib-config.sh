#!/usr/bin/env/bash
## configuration editing
## inspired by raspiconfig
##
## There are three kinds of functions here:
#
# Marker and many lines
# ---------
# the first set just looks for a marker line and then adds a bunch of lines
# it does not examine the specific contents of the lines added.
# This is most useful for large scale configurations where you are really
# adding say lines ot a bash script. The marker line is used (usually Added by

# - config_mark: Looks for a marker line and adds one if not already there
# - config_add: reads from the stdin and splats to the file without # comparing
# - config_add_var: Adds a string to a particular bash variable checking first to see if it is already there
#
# The second does whole line replacement.
# -------
# This looks for entire lines with a PREFIX and replaces them. This is most
# useful for smaller edits at the line level.
# - config_add_once: Add a line in a file if it does not exist
# - config_replace: Looks for a specific line and replaces it with a new one
#
# The final type deals with replacing setting variables
# ------
# This is the most specific, it uses lua to actually replace variables. It
# assumes the format is variable=expression and can actually parse the line.
# This is most useful for config flies like /etc/default/zfs and other sysrtemn
# - get_config_var : read out a variabvle
# - set_config_var : writes one
# - change_config_var: removes an item from the value of a config var
# - clear_config_var : removes it
#
# Utility functions
# -------
# There are some useful functions
# config_sudo: based on the file ownership decide where to use sudo or not
# config_lines_to_line: handles multiple lines additions when doing whole lines
# (obsolete use config_to_sed which also does quotes)
# and make it ready for sed by backquoting special characters

# config_backup takes a set of files and backs them up
# usage: config_backup [files...]
config_backup() {
    for target in $@
    do
        # https://unix.stackexchange.com/questions/67898/using-the-not-equal-operator-for-string-comparison
        if [[ $target =~ ^(.|..)$ ]]
        then
            # ignore $file if it is the CWD or the parent
            continue
        fi
        if [[ -e $target ]]
        then
            log_verbose found $target exists copying it to $target.bak
            n=0
            backup="$target.bak"
            while [[ -e $backup ]]
            do
                # $backup exists
                backup="${backup%.bak*}.bak.$((++n))"
                # try the next file down $backup
            done
        fi
    done
}

# https://stackoverflow.com/questions/29613304/is-it-possible-to-escape-regex-metacharacters-reliably-with-sed
# magical oneliner that handles multiline sed replacement.
# Use for finding and replacing multiple lines in a config file
# does need gnu sed and not mac sed
#
# Changed from stdin to stdout because of One bug is that is always adds a new line if there is just one line
# So you can use set_config_var instead for instance if there is just one line
# usage: to_sed_regex
# stdin: input lines does not work for single lines
# returns: 0 on success
# stdout: the properly escaped string (make sure to quote may have spaces
config_to_sed() {
  # IFS= read -d '' -r < <(sed -e ':a' -e '$!{N;ba' -e '}' -e 's/[&/\]/\\&/g; s/\n/\\&/g' <<<"$1")
  # https://www.cyberciti.biz/faq/unix-howto-read-line-by-line-from-file/
  # IFS=_space_ means that you should read the stdin separated by a space
  # -d '' means the delimiate is a null
  IFS= read -d '' -r < <(sed -e ':a' -e '$!{N;ba' -e '}' -e 's/[&/\]/\\&/g; s/\n/\\&/g' )
  # removes the newline that the redirect put in
  # printf %s "${REPLY%$'\n'}"
  # if a single line, remove another so we will have two extras
  printf %s "${REPLY%$'\n\n'}"
}

# https://stackoverflow.com/questions/40573839/how-to-use-printf-q-in-bash
# arguments: all arguments, so you want your text file to be in a bash variable
# stdout: the escaped string suitable for sed
config_to_sed_printf() {
  printf %q $@
}

#  works correct using only sed for multiple lines
config_to_sed_multiline() {
  # IFS= read -d '' -r < <(sed -e ':a' -e '$!{N;ba' -e '}' -e 's/[&/\]/\\&/g; s/\n/\\&/g' <<<"$1")
  IFS= read -d '' -r < <(sed -e ':a' -e '$!{N;ba' -e '}' -e 's/[&/\]/\\&/g; s/\n/\\&/g' )
  # removes the newline that the redirect put in
  printf %s "${REPLY%$'\n'}"
}


# returns sudo if you need it you need to force evaluation with
# $(config_sudo) which cause sudo to run
# usage: config_sudo files
config_sudo()
{
    # use find instead of stat since it works on Mac
    # stat -c '$U' only available with gnu stat
    # if [[ $(stat -c '%U' "$config") != $USER ]]
    # note we do not quote $@ so we can search them all
    # Note that this test does fail because the directory must also be writeable
    # and owned by you so this does not work with `mv` but does with tee
    # if there is no util sudo then make our own because we do not want to
    # depend on lib-util.sh as this system does not allow cascading library
    # dependencies
    for file in $@
    do
        # get the canonical form or the name assumes you are using the gnu
        file=$(readlink -f $file)
        # work up the path of the file until we find a file that exists
        while [[ ! -e $file ]]
        do
            file=$(dirname "$file")
        done
        if [[ ! -w $file ]]
        then
            echo sudo
        fi
    done
}

# make sure the parent and file exist
# usage: config_touch files...
config_touch() {
    for file in $@
    do
        if [[ ! -e $file ]]
        then
            # cannot use readlink -f not the Mac so use this instead
            # local path=$(readlink -f "$file")
            #does not work if $dir not yet created so do not use
            #this canonical view
            #local dir="$(cd "$(dirname "$file")" && pwd -P)"
            dir="$(dirname "$file")"
            $(config_sudo "$dir") mkdir -p "$dir"
            $(config_sudo "$file") touch "$file"
        fi
    done
}

# converts a bash variable with multiline text
# to a single string with \n in it on stdout
# usage: config_lines_to_line
# stdin: lines that need to be converted
# stdout: single line with \n in them
config_lines_to_line(){
    # note we use quotes on lines to retain the newlines
    # tr then deletes the special character that is a new line
    # sed adds the characters '\' and 'n' not clear why
    # config_to_sed | sed 's/$/\\n/' | tr -d '\n'
    config_to_sed | tr -d '\n'
}

# replaces the original marker work and uses the config_add
# this marks a configuration file as being edited
# It searches the "marker" line and does not add more if it finds it
# and returns the state of the file.
# if the file dopes not exist we create all the parent directories and then the
# file
# usage: config__mark -f file [ comment-prefix [ marker ]]
# -f means force a new marker
# returns: 0 if marker was found
#          1 no marker found so we added and this is a fresh file
config_mark()
{
    if (( $# < 1)); then return 1; fi
    if [[ $1 == -f ]]
    then
        local force=true
        shift
    fi
    local file=${1:-"$HOME/.bashrc"}
    local comment_prefix="${2:-"#"}"
    local marker="${3:-"Added by $SCRIPTNAME"}"

    config_touch "$file"
    #
    if ${force:-false} || ! grep -q "$marker" "$file"
    then
      # do not quote config_sudo because it can return null
      # https://stackoverflow.com/questions/3005963/how-can-i-have-a-newline-in-a-string-in-sh
      $(config_sudo "$file") tee -a "$file" <<<$'\n'"$comment_prefix $marker on $(date)" >/dev/null
      return 1
    fi
}

#
#
# It adds to the stdin use with the redirection <<-EOF typically and then EOF
# usage: config_add file_to-change <<-EOF
#        some lines to add
#        EOF
#
# Use config_add_once if you want to replace just a sigle ilne
# this is normally used with config_mark
#
config_add() {
    if (( $# < 1 )); then return 1; fi
    local file="${1:-"$HOME/.bashrc"}"
    # by default the prefix is the entire line
    # so in the default case it just adds a line
    config_touch "$file"
    local need_sudo="$(config_sudo "$file")"
    # if output is null then do not put a parameter
    # need_sudo should also  be empty
    $need_sudo tee -a "$file" >/dev/null
}

#
# config_add file variable strings...
# adds a string to a bash variable at the beginning assuming the variable doesn'
config_add_var() {
  if (( $# < 2 )); then return 1; fi
  local file="${1:-"$HOME/.bash_profile"}"
  local variable="${2:-"PATH"}"
  shift 2
  for string in $@
  do
    config_add "$file" <<<-"[[ \$$variable =~ $string ]] || export $variable=\"$string\:\$$variable ]]"
  done
}

# Adds a line if it is not already there
# It looks for a prefix and then slams a new line in if it findds it
# forces a replacement if it already exists
# the replacement can be multiple lines
# usage: config_replace file prefix-of-of-the-line-to-be-replaced lines-to-add
config_replace() {
    if (( $# < 3 )); then return 1; fi
    local file="${1:-"$HOME/.bashrc"}"
    local target="${2:-""}"
    local lines="${3:-""}"

    # shold not need to touch assume file existrs
    config_touch "$file"
    need_sudo="$(config_sudo "$file")"
    # not sure but $ means an exact match
    # so if we want to majhc then need to do
    # usage: config_add_lines [-f] [file [ lines ]]
    echo grep -q "^$target" "$file"
    if ! grep -q "^$target" "$file"
    then
      # did not find the target so just add the entire line
      #echo no line so add with tee
      # do not quote need_sudo as it can be null if not needed
      $need_sudo tee -a "$file" <<<"$lines" >/dev/null
    else
        # note this requires gnu sed running on a Mac
        # fails with the installed sed
        # to make change work we need to convert
        # $new with real new lines into something with \n in
        # a single string
        # local new_sed="$(config_to_line <<<"$lines")"
        local new_sed="$(config_to_sed <<<"$lines")"
        echo new=$new_sed
        local target_sed="$(config_to_sed <<<"$target")"
        echo target=$target_sed
        # do not quote need_sudo in case it is null
        # echo $need_sudo sed -i "/^$target_sed/c\\$new_sed" "$file"
        if [[ $(command -v sed) =~ /usr/bin/sed ]]
        then
          # this means we do not have gsed and -i will not work
          brew install gnu-sed
          PATH="/usr/local/opt/gnu-sed/libexec/gnubin:$PATH"
        fi
        echo $need_sudo sed -i "/^$target_sed/c\\$new_sed" "$file"
        $need_sudo sed -i "/^$target_sed/c\\$new_sed" "$file"
        return
    fi

}

# used config_replace but adds a line only if not present
# usage: config_add_once file line-to-add
config_add_once() {
    if (( $# < 2 )); then return 1; fi
    local file="${1:-"$HOME/.bashrc"}"
    shift
    local line="$@"
    if ! grep -q "$line" "$file"
    then
      echo adding line $line to $file
      $(config_sudo "$file") tee -a "$file" <<<"$line" >/dev/null
    fi
    # do not use config replace much simpler to do the check here
    # config_replace "$file" "$lines" "$lines"
}

# params file variable value
# usage: set_config_var [-f] key value file [marker]
set_config_var() {
    if (( $# < 3 )); then return 1;fi
    local force=false
    if [[ $1 == -f ]]
    then
        force=true
        shift
    fi
    local key="$1"
    local value="$2"
    local file="$3"
    local marker="${4:-"Added by $SCRIPTNAME"}"
    if ! $force && grep "$marker" "$file"
    then
       return
    fi
    local temp="$(mktemp)"
    lua - "$key" "$value" "$file" <<EOF > "$temp"
local key=assert(arg[1])
local value=assert(arg[2])
local fn=assert(arg[3])
local file=assert(io.open(fn))
local made_change=false
for line in file:lines() do
  if line:match("^#?%s*"..key.."=.*$") then
    line=key.."="..value
    made_change=true
  end
  print(line)
end
if not made_change then
  print(key.."="..value)
end
EOF

# note you should not move the file but tee into it
$(config_sudo $file) tee "$file" <"$temp" > /dev/null
}

# change part of a  configuration variable
# most useful when there is a long string and you just want to delete one item
# GRUB_CMGLINE is an example where you just want to remove the variable QUIET in
# the string
# usage: modify_config_var key old_value new_value file [marker]
modify_config_var()
{
    if (($# < 4)); then return 1; fi
    local key="$1"
    local current_value="$2"
    local new_value="$3"
    local file="$4"
    local marker="${5:-"Added by $SCRIPTNAME"}"
    local current_line=$(get_config_var "$key" "$file")
    # do not need eval because you can use variables in bash substitutions
    log_verbose current $current_line change from $current_value to \"$new_value\"
    local new_line="${current_line/$current_value/$new_value}"
    log_verbose new_line is $new_line
    set_config_var "$key" "$new_line" "$file" "$marker"
}

# change part of a  configuration variable
# most useful when there is a long string and you just want to delete one item
# GRUB_CMGLINE is an example where you just want to remove the variable QUIET in
# the string
# usage: modify_config_var key old_value new_value file [marker]
modify_config_var()
{
    if (($# < 4)); then return 1; fi
    local key="$1"
    local current_value="$2"
    local new_value="$3"
    local file="$4"
    local marker="${$:-"Added by $SCRIPTNAME"}"
    local current_line=$(get_config_var "$key" "$file")
    # do not need eval because you can use variables in bash substitutions
    local new_line=${current_line/$current_value/$new_value}
    set_config_var "$key" "$new_line" "$file"
}

# clears teh config variable
# usage: clear_config_var [-f] key file [marker]
clear_config_var() {
    if (( $# < 2 )); then return 1; fi
    local force=false
    if [[ $1 == -f ]]
    then
        force=true
        shift
    fi
    local key="$1"
    local file="$2"
    local marker="${3:-"Added by $SCRIPTNAME"}"
    if ! $force && grep "$marker" "$file"
    then
        return
    fi
    local temp="$(mktemp)"
  lua - "$key" "$file" <<EOF > "$temp"
local key=assert(arg[1])
local fn=assert(arg[2])
local file=assert(io.open(fn))
for line in file:lines() do
  if line:match("^%s*"..key.."=.*$") then
    line="#"..line
  end
  print(line)
end
EOF
$(config_sudo "$file") mv "$temp" "$file"
rm "$temp"
}

# get the state of the config variable after the equal sign
# usage: get_config_var key file
get_config_var() {
    if (( $# < 2 )); then return 1l; fi
    local key="$1"
    local file="$2"
  lua - "$key" "$file" <<EOF
local key=assert(arg[1])
local fn=assert(arg[2])
local file=assert(io.open(fn))
local found=false
for line in file:lines() do
  local val = line:match("^%s*"..key.."=(.*)$")
  if (val ~= nil) then
    print(val)
    found=true
    break
  end
end
if not found then
   print(0)
end
EOF
}
