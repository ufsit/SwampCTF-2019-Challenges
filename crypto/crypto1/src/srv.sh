#!/bin/bash

$PWD/portable/build/apps/openssl/openssl s_server \
  -cert ~/.local/share/mkcert/rootCA.pem \
  -key ~/.local/share/mkcert/rootCA-key.pem \
  -dhparam $1.pem \
  -WWW
