#!/bin/bash 

IN=$1


# Remove empty lines
sed -i -e "/^$/d" $IN

# Remove timestamp lines
sed -i -e "/^[0-9][0-9]:[0-9][0-9]/d" $IN

# And replace the number lines with blank lines
sed -i -e "s/^[0-9]*$//" $IN
