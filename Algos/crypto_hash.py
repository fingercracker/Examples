#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 19:49:38 2019

@author: johnmartin
"""

import string
import numpy as np

#Use a universal array, and dynamic programming techniques to produce the first N primes
def list_primes(N):
    primes = [0 for i in range(N)]
    primes[0] = 2
    num_primes = 1
    current_int = 3
    flag = 0
    while num_primes < N:
        for i in range(num_primes-1):
            if current_int%primes[i] == 0:
                flag = 1
                break
        if flag == 0:
            primes[num_primes] = current_int
            num_primes += 1
        flag = 0
        current_int += 1
    return primes

#represent n using b bytes in base 256 = 2^8
#this can thus be represented as an IPv4 address
def deconstruct(n):
    n_expansion = [0 for i in range(4)]
    power = 3
    dig = 0
    while power >= 0:
        while n >= 256**power:
            dig += 1
            n -= 256**power
        n_expansion[power] = dig
        power = power - 1
        dig = 0
    return n_expansion
        
#encode the input string s using the first 26 primes to encode the 26 letters
#of the alphabet. This will output unique encodings for distinct strings since 
#prime factorizations of integers are unique. The only issue is that collisions will
#occur when the same number of characters are used.
#Input:
    #s = string to be encoded
    #cypher = dictionary having the nth letter of the alphabet as the key for the nth prime
        #we will extend this to include uppercase as well
def encode_string(s, cypher):
    ret_arr = []
    esses = s.split()
    for ess in esses:
        for letter in ess:
            ret_arr.append(cypher[letter])
    return ret_arr

#n_vec is a length r expansion (usually IPv4 for example) of an integer n.
#the integer n can be an encoding of a string, or a hashing of some other 
#quantity
def universal_hash(n_vec, a):
    v = 0
    r = len(n_vec)
    for i in range(r):
        v += n_vec[i]*a[i]
    p = list_primes(1000)[999]
    return v%p
    
#we will, for the sake of this rather simple version of the code, use the 
#ascii letters to encode the strings. We will thus not allow special characters
#such as periods, numbers, hyphens, etc. 
letters = string.ascii_letters
vals = list_primes(len(letters))
cypher = {}
for i in range(len(letters)):
    cypher[letters[i]] = vals[i]
    
#run an example using the strings in 'esses', and hash each of them. We should
#expect to see minimal collisions. We even include some case snesitive anagrams
#to show that it is unlikely that two strings will get the same hash.
esses = [
    "whatever", "John Willis", "Hola", "I Am From earth", "nohJ silliW", "Liv Criddle", 
    "www giardiaband com", "www google com", "this is kind of fun all of the time when I"
    "get bored and continue to write code in the efforts of hopefully one day "
    "finding a job", "pbr is a wonderfully delicious treat on a warm evening I", 
    "ahhh ohhhh yeeeahhhhhh", "hhhhhhh big hhhhhhhhhh", "www kenaima com", 
    "www willistowerswatson com", "www bentknee com", "www github com"
]
tableau = {}
p = list_primes(10000)[9999]
#create the random vector that will be used in universal_hash
a = []
for i in range(4):
    a.append(np.random.randint(p))
for s in esses:
    temp = encode_string(s, cypher)
    n = 1
    for t in temp:
        n *= t
    n_expansion = deconstruct(n%p)
    hashed_string = universal_hash(n_expansion, a)
    tableau[hashed_string] = s
print(tableau)