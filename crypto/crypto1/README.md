# [SwampCTF 2019 Cryptography] Trust your Brainwallet to VapeCoinIO

## Flavor Text

* Flag: `VapeCoinIO_Should_Have_Used_13`
* Expected difficulty: medium/hard

Ever since their hella successful ICO, the crypto experts at VapeCoinIO have put
developers first with their simple, intuitive, and hella secure API. Once you've
created your account and set up your wallet, you can access it programatically
using your VapeID by sending a GET request to
    
    /api/login?key=<HASH>

where `<HASH>` is your VapeID. Your wallet is transferred to you over TLS, so
don't worry---it's really, really secure. In fact, it's so secure that Count
Rugen, the founder and CEO of VapeCoinIO, uses the API for his personal
Brainwallet.

But here's the thing. Your father made The Count a gleaming, gold-inlayed
rapier, and when your father came to demand payment, the Count slashed him
through the heart with the very same sword.

Yours is a story of vengeance.

Your goal is to steal The Count's crypto secrets and use them to bankrupt his
company. Your new friend, "The Man in Black", is a site-reliability engineer at
VapeCoinIO. He has obtained a PCAP of a TLS session with a client originating
from an IP he suspects to be used by The Count's personal laptop. Perhaps he
accessed his wallet! Can you find a way to recover its contents?


## Description

TLS is the most widely deployed crypto protocol, but also among the heaviest.
Its evolution is driven by both attacks and the operational requirements that
arise as its usage increases. Both factors have lead to lots of complexity and
some really bad designs.  The result---and, hopefully, the takeaway of this
challenge---is that merely the presence of TLS does not imply security of
communications.

The attacker is handed a transcript of a TLS session recorded with Wireshark.
It is apparent from the flavor text that the attacker's goal is to recover the
flag contained in the first flight of application data sent by the server. The
challenge is to find and exploit a weakness in the negotiated parameters that
makes the attack feasible.


## Challenge Solution

Open up `attachements/trancript.pcapng` and you'll see the transcript of a TLS
1.2 session between The Count (the client) and the VapeCoinIO API (the server).
The flag is contained in the server's first flight of application data, so
you're only hope is to decrypt it.

The ciphersuite is `TLS_DHE_RSA_WITH_AES_GCM_SHA256`, which is comprised of
strong primitives. Upon closer inspection of the ServerKeyExchange message,
you'll notice that the DH parameters are quite weak. The generator g is 2, which
is not a problem, but the prime modulus p is only 32 bits long. Thus, the
solution (implemented by `src/solver.go`) is to compute the discrete logarithm
(DL) of either the server or client's key share, use the result to compute the
pre-master secret, then derive the secret key (and IV) the server used to
encrypt its message.

**Background.** 
TLS allows for the negotiation of custom Diffie-Hellman (DH) parameters for a
very practical reason. It allows servers to provide resistance to the LogJam
attack, which affects any server using common (i.e., NIST-standardized) finite
fields for DH-based key exchange. To mitigate this attack, the server operator
would choose their own DH parameters (p and g). From the standpoint of the wire
protocol, this is no different than using a standardized group, and so this
mechanism is widely used.

Now, choosing sufficiently strong DH parameters is a probabilistic process that
takes some time --- usually hours or even days. Many TLS implementations allow
for negotiating very small groups; today, even a 1024-bit prime is considered
weak. (We use a *much* smaller prime (32 bits) to make this challenge feasible
and fun.) Therefore, it is incumbent on the TLS operator to make this
security-critical decision.

**Notes.**
Sounds easy enough. Two factors make this problem challenging.
  
  1. Let's start with the obvious one. The attacker needs to be able to compute
     DLs in the group in a reasonable amount of time. The naive solution is to
     simply compute g^1, g^2, g^3 (mod p) and so on until one finds x such that
     g^x (mod p) = Y, where Y is the client's (or server's) key share. We can do
     better by parallelizing the search, and their may be number theoretic
     tricks we can use that depend on Y, p, and q. As a last resort, there's
     also Pollard's "kangaroo method" for computing DLs in generic groups.

     **NOTE:** The parameters are tuned so the naive solution takes on the order
     of 10 minutes. (`src/solver.go` finds the solution in 2m36s on my
     machine.)

  2. Computing the pre-master secret is the necessary first step, but using it
     to decrypt the ciphertext requires an understanding of the internals (and
     intricacies) of TLS. I was unable to find a tool online that allowed for
     inspecting TLS traffic given the pre-master secret was computed using
     ephemeral DH; Wireshark only appears to work with KEM-based key exchange.

I wrote ~300loc of Go, drawing both from the spec (RFC 5246) and Go's
implementation (`crypto/tls`) of the protocol. To drive development, I generated
a test transcript that used a *16-bit* prime for the DH group. (Follow the
instructions in `src/README.md`.) Solving DLs in this group is virtually
instantaneous.
