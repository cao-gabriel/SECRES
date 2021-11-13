#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 11:23:27 2021

@author: gabriel
"""

import math
import argparse
from time import time
from sympy import isprime
from random import randrange

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271 ]

def extended_gcd(a, b):
    '''
    Compute the greatest common divisor of a and b

    Parameters
    ----------
    a : int
        Non negative number whose gcd has to be computed
    b : int
        Non negative number whose gcd has to be computed

    Returns
    -------
    This method will return an absolute/positive integer value
    after calculating the GCD of given parameters a and b.

    '''
    x, y, lastx, lasty, = 0, 1, 1,0
    while b != 0:
        q = a // b
        a, b = b, a % b
        x, lastx = lastx - q * x, x
        y, lasty, = lasty - q * y, y
    return abs(a), abs(lastx), abs(lasty)

def random_curve(modulo):
    '''
    Return the coefficients of a randomn elliptic curve which modulo
    is equal to the given parameter 'modulo' and a point on this curve 

    Parameters
    ----------
    modulo : int
        Non negative number which is the modulo of the elliptic curve.

    Returns
    -------
    This method will return a list of size 2, the first element of this list
    is a triplet which are the coefficients of the elliptic curve and the second
    element of the list is a couple representing a point on the curve.
    '''
    a, u, v = randrange(modulo), randrange(modulo), randrange(modulo)
    b = (pow(v, 2) - pow(u, 3) - a * u) % modulo
    coeff = a, b, modulo
    point = u, v
    return [coeff, point]

def add_point(curve, point1, point2):
    '''
    Compute the sum of two given parameters points 'point1' and 'point2' located
    in the elliptic curve 'curve' given as a parameter.

    Parameters
    ----------
    curve : (int, int, int)
        A triplet of int which are the coefficients representing an elliptic curve.
    point1 : (int, int)
        A couple of int representing a point located in the curve given as parameter
    point2 : (int, int)
        A couple of int representing a point located in the curve given as parameter

    Returns
    -------
    This method will return a list of size 2. The first element of the list is a couple of int
    representing the point resul from the addition of 'point1' and 'point2'. The second element
    of the list is the greatest common divisor between...

    '''
    if point1 == "Identity": return [point2, 1]
    if point2 == "Identity": return [point1, 1]
    a, b, modulo = curve
    x1, y1 = point1 ; x2, y2 = point2
    x1 %= modulo; y1 %= modulo; x2 %= modulo; y2 %= modulo
    
    if x1 != x2:
        d, u, v = extended_gcd(x1 - x2, modulo)
        s = ((y1 - y2) * u) % modulo
    else:
        if (y1 + y2) % modulo == 0:
            return ["Identity", 1]
        else:
            d, u, v = extended_gcd(2 * y1, modulo)
            s = ((3 * pow(x1, 2) + a) * u) % modulo
    x3 = (pow(s, 2) - x1 - x2) % modulo
    y3 = (- y1 - s * (x3 - x1)) % modulo
    point3 = x3, y3
    return [point3, d]

def find_factor(curve, point, bound):
    '''
    Compute points in the elliptic curves using the given parameters 'point' and
    'bound' to find a non-invertible elements

    Parameters
    ----------
    curve : int, int, int
        A triplet which are the coefficients of an elliptic curve.
    point : int,int
        A point of the elliptic curve given as parameter.
    bound : int
        A number representing the amount of work on the curve.

    Returns
    -------
    list
        This method returns a list of size 2, either there were no non-invertible
        elements that were found the couple (neutral point, 1) is returned either
        a non-invertible element is found meaing a factor has been found so the 
        point where the element were found and the element are returned

    '''
    new_point = "Identity"
    my_factor = 1
    while bound != 0:
        if bound % 2 != 0:
            new_point, my_factor = add_point(curve, new_point, point)
        if my_factor != 1:
            return [new_point, my_factor]
        point, my_factor = add_point(curve, point, point)
        if my_factor != 1:
            return [new_point, my_factor]
        bound //=2
    return ["Identity", 1]
def ecm(my_number, bound, max_curves = 10):
    '''
    Find a factor of the given parameter 'my_number' using the elliptic curve method
    of Lenstra with the given parameter 'bound' and 'max_curves''

    Parameters
    ----------
    my_number : int
        Number whose factor has to be computed.
    bound : int
        Number representing the upper bound of the elliptic curve, a product of 
        primes smaller than the given parameter 'my_number'.
    max_curves : int, optional
        Number representing the maximum number of curves used to find
        a factor of the given parameter 'my_number'. The default is 10.

    Returns
    -------
    int
        This method return a factor of the given parameter 'my_number'
        or 'my_number' if no factor has been found.

    '''
    for i in range(max_curves):
        print("\tProcess curve", i)
        curve, point = random_curve(my_number)
        _, my_factor = find_factor(curve, point, bound)
        if my_factor != 1:
            return my_factor
    return my_number

def main(my_number, bound_param):
    #my_number = int(input("Please input the number to be factorized : "))
    print(f"Number to factorize : {my_number}")
    for prime in primes:
        while my_number % prime == 0:
            if my_number == prime:
                print("\t{} is prime".format(my_number))
            else:
                print(f"\t{prime} is a factor of {my_number}")
            my_number //= prime
            print(f"Number to factorize {my_number}")
    
    bound = int(math.factorial(bound_param)) # bound should be less than the number to be factorized
    while my_number != 1:
        if isprime(my_number):
            print(f"\t{my_number} is prime")
            break
        my_factor = int(ecm(my_number, bound, 1000))

        print(f"\t{prime} is a factor of {my_number}")
        my_number = int(my_number // my_factor)
        print(f"Number to factorize {my_number}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="lenstra_factor")
    parser.add_argument("prime1")
    parser.add_argument("prime2")
    parser.add_argument("bound_param")
    args = parser.parse_args()
    start_time = time()
    my_number = int(args.prime1) * int(args.prime2)
    main(my_number, int(args.bound_param))
    end_time = time()
    print("Time to factor {} : {} s".format(my_number, end_time - start_time))