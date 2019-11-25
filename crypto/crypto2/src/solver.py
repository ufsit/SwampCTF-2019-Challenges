#!/usr/bin/env python2
from IPython import embed
import fractions
import base64
from primefac import factorint
from Crypto.PublicKey import RSA
from binascii import hexlify, unhexlify

f = open("./challenge/public0.pem", "r")
key = RSA.importKey(f.read())

print(key.n)
print(key.e)

def egcd(a,b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
        gcd = b
    return gcd, x, y

def totient(n):
    totient = n
    for factor in factorint(n):
        totient -= totient // factor
    return totient

print("computing totient n...")
phi = totient(key.n)

gcd, a, b = egcd(key.e, phi)
d = a

print("n = {}".format(str(d)))
with open("challenge/c0.txt") as f:
    ct1 = int(base64.b64decode(f.read()))
with open("challenge/c44.txt") as f:
    ct2 = int(base64.b64decode(f.read()))
with open("challenge/c50.txt") as f:
    ct3 = int(base64.b64decode(f.read()))
with open("challenge/c55.txt") as f:
    ct4 = int(base64.b64decode(f.read()))

print("ciphertext = {}".format(ct1))
pt1 = pow(ct1, d, key.n)
print("pt1: {}".format(str(pt1)))
print(hex(pt1)[2:-1])

print("ciphertext = {}".format(ct2))
pt2 = pow(ct2, d, key.n)
print("pt2: {}".format(str(pt2)))
print(hex(pt2)[2:-1])

print("ciphertext = {}".format(ct3))
pt3 = pow(ct3, d, key.n)
print("pt3: {}".format(str(pt3)))
print(hex(pt3)[2:-1])

print("ciphertext = {}".format(ct4))
pt4 = pow(ct4, d, key.n)
print("pt4: {}".format(str(pt4)))
print(hex(pt4)[2:-1])

print(unhexlify(hex(pt1)[2:-1]))
print(unhexlify(hex(pt2)[2:-1]))
print(unhexlify(hex(pt3)[2:-1]))
print(unhexlify(hex(pt4)[2:-1]))
embed(banner1='')
