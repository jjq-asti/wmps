#!/usr/bin/sh

sudo python3 ~/wpms/rfc6349.py --reverse 50000000 202.90.158.6 202.90.158.6 && \
sudo python3 ~/wpms/rfc6349.py --forward 50000000 202.90.158.6 202.90.158.6
