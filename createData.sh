#!/bin/bash
pwd=''
user='username'
mysql << EOF
create database weather;
use weather;
EOF