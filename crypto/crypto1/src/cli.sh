#!/bin/bash

echo "GET /api/login?key=6c4140ab014a9c8babf2e3dc734d83e7c3e8657eecb58883ea469083eb629cd4 HTTP/1.0" | \
  $PWD/portable/build/apps/openssl/openssl s_client \
    -cipher DHE-RSA-AES128-GCM-SHA256 \
    -ign_eof
