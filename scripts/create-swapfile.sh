#!/bin/bash

dd if=/dev/zero of=/swapfile bs=1024 count=524288
chown root:root /swapfile
chmod 0600 /swapfile
mkswap /swapfile
swapon /swapfile