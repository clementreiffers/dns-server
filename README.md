# dns-server

The goal of this DNS server is to restrict the access to a list of a websites.
Moreover, this server will be used to restrict the access to a list of websites 
available on a mongoDB database, in order to prevent connections with bad servers
which send you malware and other.

## Overview

1. [Install the project](#install-the-project)
   1. [install using make](#install-using-make-command)
   2. [install using pip](#install-using-pip-command)
2. [Run the project](#run-the-project)
    1. [run using make](#run-using-make-command)
    2. [run without make](#run-without-make-command)


## Install the project

### install using `make` command

> **Warning**
> 
> this part works only with Linux based distro!

you just have to do `make install` it will install all necessary modules.

### install using `pip` command

> **Note**
> 
> this part works with Windows and Linux, depending on how you call python on your distro 

run `python3 -m pip install -r requirements.txt` your terminal

## Run the project

### Run using `make` command 

run `make run` command

### Run Without `make` command

run `python3 main.py`