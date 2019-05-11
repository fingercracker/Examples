#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 11 11:20:47 2019

@author: johnmartin
"""

#find largest power of 2 smaller than n
#ret_val = value 2^count
#count = the largest exponent
def largest_less(n):
    if n<2:
        return n, 0
    ret_val = 1
    count = 0
    while ret_val <= n:
        if 2*ret_val > n:
            return ret_val, count
        else:
            ret_val *= 2
            count += 1
    return ret_val, count

#compute the binary expnansion of n
def bin_exp(n):
    if n<=2:
        return n
    
    ret_arr = []
    l=0
    ind = 0
    inds = []
    m=n
    while m>2:
        l, ind = largest_less(m)
        m = m - l
        ret_arr.append(l)
        inds.append(ind)
    ret_arr.append(m)
    if m==2:
        inds.append(1)
    else:
        inds.append(0)
    return ret_arr, inds

#compute n^exp[i] for each i in range log_2(max(exp))
def succ_square(n,m,exp):
    if n > m:
        n = n%m
    
    ret_arr = [n]
    max_val = max(exp)
    i = 1
    while 2**i <= max_val:
        ret_arr.append((ret_arr[i-1]**2)%m)
        i += 1
    return ret_arr

#compute n^p(mod m)
def mod_square(n, p, m):
    exp, inds = bin_exp(p)
    arr = succ_square(n,m,exp)
    print(exp, inds, arr)
    N = len(exp)
    ret_val = 1
    for i in range(N):
        if exp[i] !=0:
            ret_val = (ret_val*arr[inds[i]])%m
    return ret_val
