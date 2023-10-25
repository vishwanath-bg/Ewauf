#!/bin/bash

apt_install() {
    local pkg=
    local pkgs=()
    local ok
    for pkg in "$@"; do
        ok=$(dpkg-query --showformat=\${Version} --show "$pkg" 2>/dev/null || true)
        if [[ -z "$ok" ]]; then pkgs+=( "$pkg" ); 
        else
            echo "${pkg} is already installed"
        fi
    done
    if (("${#pkgs[@]}")); then
        for i in ${pkgs[@]}; do 
            echo "###################################"
            echo "Installing $i..."
            echo "###################################"
            apt-get install -y $i
        done
        
    fi
    
}

pip_install() {

    local pkg=
    local pkgs=()
    local ok
    local count=1
    for pkg in "$@"; do

        if ok=$(pip3 show "$pkg"); then 
             echo "${pkg} is already installed"
        else
            pkgs+=( "$pkg" );
        fi
    done

    if (("${#pkgs[@]}")); then 
        for i in ${pkgs[@]}; do 
            echo "###################################"
            echo "Installing $i..."
            echo "###################################"
            pip3 install $i
        done
        # 
    fi

}


echo "################### Checking permissions ##############"
if [ "$(id -u)" -ne 0 ]; then
        echo 'This script must be run by root\nTry running as sudo' >&2
        exit 1
fi

echo "################### Installing python packages ##############"
apt_install python3-pip libxml2-dev libxslt1-dev python-dev-is-python3 python3-lxml python3-tk

echo "################### Installing pip packages ##############"
pip_install paramiko openpyxl matplotlib pandas requests xmltodict jinja2