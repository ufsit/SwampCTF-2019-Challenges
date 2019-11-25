# Building the problem

The following are the steps taken to generate the challenge TLS transcript. The
product is a packet capture (recorded with Wireshark) of the handshake and
application data of one run of the protocol using weak, custom DH parameters.
The solution to the problem is the string contained in
`src/api/login?key=<HASH>`, where `<HASH>` is the SHA256 hash of `hella\n`.

These instructions have been tested on Ubuntu 18.04.


## Getting the code

This challenge will involve a vulnerable implementation of TLS. We will build
the source of LibreSSL v2.6.5:

    git clone https://github.com/libressl-portable/portable.git
    cd portable && git checkout tags/v2.6.5

Follow the build instructions in `./README.md`. I assume that you've used
`cmake` for building.


## Generating certificates

The set up will use an end-entity certificate for "vapecoin.io" signed by a CA
whose secret key is on your system. The `mkcert` tool (written in Go) makes this
super easy.

    go get github.com/FiloSottile/mkcert
    go install github.com/FiloSottile/mkcert
    mkcert   # Generates root cert and key and saves to ~/.local/share/mkcert
    mkcert -install   # Install root cert


## Generating (weak) DH parameters

From `src/` in the root project directory:

    alias myssl="$PWD/portable/build/apps/openssl/openssl"
    myssl dhparam 32 -out weak.pem
    myssl dhparam 2048 -out strong.pem

Generating the "weak" parameters will be nearly instantaneous; finding the
"strong" parameters will take some time. The former uses a 32-bit prime to
define the finite field, while the latter uses a 2048-bit prime.


## Patching the code to permit weak parameters

We can now perform a handshake with our end-entity certificate and custom DH
parameters. To do so, run `./srv.sh strong` in the current directory and
`./cli.sh` in the same directory, but in a new terminal. This performs the TLS
handshake with the strong DH parameters. The client then sends

    GET /api/login?key=<HASH> HTTP/1.0

and the server responds with the contents of `./api/login?key=<HASH>`.

To run with the weak parameters, execute the server with `./srv.sh weak`. The
client should abort the handshake and output an error. The reason is that
LibreSSL clients reject DH parameters whose prime is less than 1024 bits in
length. To enable our attack, we modify the client by commenting out the
following check at `portable/ssl/ssl_clnt.c:1147`:

  	if (DH_size(dh) < 1024 / 8) {
      SSLerror(s, SSL_R_BAD_DH_P_LENGTH);
      goto err;
  	}

After rebuilding the code, re-running the handshake with weak parameters should
succeed. The client's output should contain the following line:

    Server Temp Key: DH, 32 bits 


## Recording the transcript

Run wireshark and listen on loopback. In `src/` in the root project directory,
run `./srv.sh weak` and `./cli.sh`. Save the packet capture to
`attachments/transcript.pcapng`.
