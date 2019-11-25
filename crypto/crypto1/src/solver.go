package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"hash"
	"math/big"
)

const (
	keyLen        = 16
	macLen        = 0
	ivLen         = 4
	headerLen     = 5
	explicitIVLen = 8
)

// solverData contains the hex-encoded handshake parameters and target
// ciphertext needed to recover the flag for this challenge.
type solverData struct {
	p, g   string // "p" and "g" in ServerKeyExchange
	X, Y   string // Client and server key shares
	cr, sr string // Client and server randoms

	// The server's first application-data flight. This includes the record
	// header, explicit nonce, and ciphertext.
	flag string
}

var Test *solverData = &solverData{
	p:    "c3e3", // In Wireshark, use "Copy as Hex stream"
	g:    "02",
	Y:    "a7af",
	X:    "4d3b",
	cr:   "30e0efaacb38064739fccc38e79e1d45b5d6dcde66dd8122ec776fbbd99a3818",
	sr:   "a9b4fde495de81ca24465c5d2c48e1abc4e52866166de6024efe42efdd26ac07",
	flag: `170303005b0000000000000001fa8b12ec51130c651e127a6c4cb374440d69f88b23139566e81511a65a5ca2140490d7dc832e592484637ea9f6de5686b01fdb9a0edf79f37167602fca5a71ceabd8a3db0d5ed4212a13c5edc4f8988c6a5f15`,
}

var Challenge32 *solverData = &solverData{
	p:    "f661398b",
	g:    "02",
	Y:    "916ddb94",
	X:    "42b2769b",
	cr:   "358970edf3544c1181cecf3369cd4c0e69be2c3605662ba1288b251161eba51e",
	sr:   "841663c5617109b9ed5d70cb8fe8ac8949c0611cf6c3803f59bf3bbc03481392",
	flag: "170303006a0000000000000001f2a88c49b033b81d345a60da5321b9b72f0182835ea5052b59fce15b242693aa8e0eb5d037ebc4ed9b219a7fafa8ec3d72b876348347102b549523fb93a804139e6389c8e2e24838cede0029ced6a4b0562015a848247df428b298dc0d7180250e78",
}

var Challenge64 *solverData = &solverData{
	p:    "a76fdbc78cce7c03",
	g:    "02",
	Y:    "a3cbbdf7d5e28789",
	X:    "3d31d2002d343a4f",
	cr:   "3c917e89533d328adb2f8883b6f98fbd254c3a564c79c53410f63ca69c98e827",
	sr:   "2dc41b262b1d6ce47694c3e2fb202a30752cc159ef32c1b641a68e029a20200a",
	flag: "170303005b0000000000000001b0c87b0773066203f63faa0b2c923c2328ff5909da2a06cd581ea1edef1a52a9ada3145a2ea2e7216be95b33b14af027deeae2927e21557cd7df857cf1d38d2a4e1db47531c7852895d9a62f6fdf62accff7ff",
}

func main() {
	P := Challenge32

	// Step 1: Compute the shared secret from the DH parameters and key shares
	// in the handshake.
	//
	// NOTE: This part will take a very very long time! This is because it
	// involves solving a discrete log, which is slow even for weak DH groups.
	Z := sharedSecret(P.p, P.g, P.X, P.Y)
	fmt.Println("pre-master secret:", hex.EncodeToString(Z.Bytes()))

	// Step 2: Compute the master secret from the shared secret and client and
	// server randoms.
	M := masterSecret(Z, P.cr, P.sr)
	fmt.Println("master secret:", hex.EncodeToString(M))

	// Step 3: The flag is contained in the server's first application-data
	// flight, so we will need to derive the server's key and IV.
	K, IV := serverWriteKeyAndIV(M, P.cr, P.sr)

	// Step 4: Decrypt the target ciphertext and return the contents.
	plain := decryptFirstFlight(P.flag, K, IV)
	fmt.Println(plain)
}

// sharedSecret computs the shared secret for the session by computing the
// discrete logarithm x of the client's share and computing Y^x (mod p), where Y
// is the server's share.
func sharedSecret(pHex, gHex, XHex, YHex string) (Z *big.Int) {
	Z = new(big.Int)  // The shared secret
	X := new(big.Int) // Client key share
	Y := new(big.Int) // Server key share
	p := new(big.Int) // DH group modulus
	g := new(big.Int) // DH group generator

	p.SetString(pHex, 16) // Interprets input as big endian.
	g.SetString(gHex, 16)
	X.SetString(XHex, 16)
	Y.SetString(YHex, 16)

	Z.Exp(Y, discreteLog(X, p, g), p)
	return
}

// discreteLog computes the discrete logarithm of X in the group specified by p
// and g. It does so by exhaustively trying g^x (mod p) for each 1 <= x <= q,
// where q is the order of the group.
func discreteLog(X, p, g *big.Int) (x *big.Int) {
	x = new(big.Int)
	one := new(big.Int)
	X0 := new(big.Int)

	x.SetUint64(1)
	one.SetUint64(1)
	X0.Set(g)
	for X0.Cmp(one) != 0 && X0.Cmp(X) != 0 {
		x.Add(x, one)
		X0.Mul(X0, g)
		X0.Mod(X0, p)
	}

	if X0.Cmp(one) == 0 {
		panic("bad group parameters?")
	}

	return
}

// masterSecret computes the master secret from the shared secret (i.e., the
// pre-master secret) according to the TLS 1.2 spec.
//
//  master_secret = PRF(pre_master_secret, "master secret",
//                      ClientHello.random + ServerHello.random)
//	                    [0..47];
func masterSecret(Z *big.Int, crHex, srHex string) []byte {
	M := make([]byte, 48)
	seed := bytesFromHexString(crHex)
	seed = append(seed, bytesFromHexString(srHex)...)
	prf12(sha256.New)(M, Z.Bytes(), []byte("master secret"), seed)
	return M
}

// serverWriteKey derives the server's encryption key from the master secret.
func serverWriteKeyAndIV(M []byte, crHex, srHex string) ([]byte, []byte) {
	cr := bytesFromHexString(crHex)
	sr := bytesFromHexString(srHex)
	_, _, _, serverKey, _, serverIV := keysFromMasterSecret(M, cr, sr)
	return serverKey, serverIV
}

// decryptFirstFlight deciphers the first flight of application data.
//
// The associated data is computed as per Sec. 6.2.3.3:
//
//       additional_data = seq_num + TLSCompressed.type +
//                         TLSCompressed.version + TLSCompressed.length
//
// The connection uses no compression.
func decryptFirstFlight(flag string, K, IV []byte) string {
	E, err := aes.NewCipher(K)
	if err != nil {
		panic(err)
	}

	ciph, err := cipher.NewGCM(E)
	if err != nil {
		panic(err)
	}

	payloadLen := hex.DecodedLen(len(flag))
	payload := make([]byte, payloadLen)
	if _, err = hex.Decode(payload, []byte(flag)); err != nil {
		panic(err)
	}

	C := []byte(payload[headerLen+explicitIVLen:])
	CLen := len(C) - ciph.Overhead()

	N := append(IV, payload[headerLen:headerLen+explicitIVLen]...)

	A := make([]byte, 8) // Initial sequence number is 1.
	A[7] = 1

	A = append(A, payload[:headerLen]...)
	A[11] = byte(CLen >> 8) // Overwrite the length
	A[12] = byte(CLen)

	plain, err := ciph.Open(nil, N, C, A)
	if err != nil {
		panic(err)
	}

	return string(plain)
}

// pHash implements the P_hash function, as defined in RFC 4346, section 5.
//
// NOTE: This was stolen from crypto/tls.
func pHash(result, secret, seed []byte, hash func() hash.Hash) {
	h := hmac.New(hash, secret)
	h.Write(seed)
	a := h.Sum(nil)

	j := 0
	for j < len(result) {
		h.Reset()
		h.Write(a)
		h.Write(seed)
		b := h.Sum(nil)
		copy(result[j:], b)
		j += len(b)

		h.Reset()
		h.Write(a)
		a = h.Sum(nil)
	}
}

// prf12 implements the TLS 1.2 pseudo-random function, as defined in RFC 5246,
// section 5.
//
// NOTE: This was stolen from crypto/tls.
func prf12(hashFunc func() hash.Hash) func(result, secret, label, seed []byte) {
	return func(result, secret, label, seed []byte) {
		labelAndSeed := make([]byte, len(label)+len(seed))
		copy(labelAndSeed, label)
		copy(labelAndSeed[len(label):], seed)

		pHash(result, secret, labelAndSeed, hashFunc)
	}
}

// keysFromMasterSecret generates the connection keys from the master
// secret, given the lengths of the MAC key, cipher key and IV, as defined in
// RFC 2246, section 6.3.
//
// NOTE: This is stolen from crypto/tls
func keysFromMasterSecret(masterSecret, clientRandom, serverRandom []byte) (clientMAC, serverMAC, clientKey, serverKey, clientIV, serverIV []byte) {
	seed := make([]byte, 0, len(serverRandom)+len(clientRandom))
	seed = append(seed, serverRandom...)
	seed = append(seed, clientRandom...)

	n := 2*macLen + 2*keyLen + 2*ivLen
	keyMaterial := make([]byte, n)
	prf12(sha256.New)(keyMaterial, masterSecret, []byte("key expansion"), seed)
	clientMAC = keyMaterial[:macLen]
	keyMaterial = keyMaterial[macLen:]
	serverMAC = keyMaterial[:macLen]
	keyMaterial = keyMaterial[macLen:]
	clientKey = keyMaterial[:keyLen]
	keyMaterial = keyMaterial[keyLen:]
	serverKey = keyMaterial[:keyLen]
	keyMaterial = keyMaterial[keyLen:]
	clientIV = keyMaterial[:ivLen]
	keyMaterial = keyMaterial[ivLen:]
	serverIV = keyMaterial[:ivLen]
	return
}

func bytesFromHexString(xHex string) []byte {
	var err error
	xLen := hex.DecodedLen(len(xHex))
	x := make([]byte, xLen)
	if _, err = hex.Decode(x, []byte(xHex)); err != nil {
		panic(err)
	}
	return x
}
