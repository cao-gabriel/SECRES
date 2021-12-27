#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 10:18:58 2021

@author: gabriel
"""

from math import gcd
from random import randint
import sympy

class FoundFactor(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
def division(x, y, n):
    if y % n == 0:
        raise ZeroDivisionError
    my_gcd = gcd(y, n)
    if my_gcd != 1:
        raise FoundFactor(my_gcd)
    return x // y

def addition(p, q, my_curve):
    a, b, n = my_curve
    xp, yp = p
    xq, yq = q
    if p != q:
        slope = (yq - yp) // (xq - xp)
        xr = pow(slope, 2) - xp - xq
        yr = -yp + slope * (xp - xr)
        return xr, yr
    else:
        slope = division((3 * pow(xp, 2) + a), (2 * yp), n)
        xr = pow(slope, 2) - 2 * xp
        yr = -yp + slope * (xp - xr)
        return xr, yr

def multiplication(p, my_lambda, my_curve):
    if my_lambda == 0:
        return (0, 1)
    if my_lambda == 1:
        return p
    if my_lambda % 2 == 0:
        return multiplication(addition(p, p, my_curve), my_lambda // 2, my_curve)
    else:
        return addition(p, multiplication(addition(p, p, my_curve), (my_lambda - 1) // 2, my_curve), my_curve)
    
def lenstra(n, borne, count):
    for i in range(count):
        g = n
        while g > 1:
            a, x0, y0 = [randint(0, n - 1) for tmp in range(3)]
            b = pow(y0, 2) - pow(x0, 3) - a * x0
            g = gcd(4 * pow(a, 3) + 27 * pow(b, 2), n)
            if g > 1 and g < n:
                return g
        my_curve = a, b, n
        p = x0, y0
        primes = list(sympy.sieve.primerange(0, borne))
        for prime in primes:
            exposant = 0
            while pow(prime, exposant) <= borne:
                exposant += 1
            exposant -= 1
            try:
                p = multiplication(p, pow(prime, exposant), my_curve)
            except FoundFactor as e:
                return int(str(e))
            except ZeroDivisionError as e:
                raise e

    raise Exception()
def main(n):
    factors = []
    #n = int(input("Entrez un nombre : "))
    my_gcd = None
    while my_gcd != 1:
        my_gcd = gcd(n, 6)
        factors.append(my_gcd)
        n = n // my_gcd
    
    while not sympy.isprime(n):
        try:
            factor = lenstra(n, 10000, 100)
            n = n // factor
            factors.append(factor)
        except Exception as e:
            print(factors)
            return e
    factors.append(n)
    return factors