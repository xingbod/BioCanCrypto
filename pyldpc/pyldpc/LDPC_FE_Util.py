'''
Copyright © 2020 by Xingbo Dong
xingbod@gmail.com
Monash University

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


'''

# Author: Hicham Janati (hicham.janati@inria.fr)
#
# License: BSD (3-clause)


import numpy as np
from pyldpc import make_ldpc, encode, decode, get_message


class LDPC_FE_Util(object):
    """The most basic non-interactive fuzzy extractor"""

    def __init__(self, n, d_v, d_c, **locker_args):
        """Initializes a LDPC_FE_Util

        """

        ### LDPC init
        self.n = n  # code length, should be 2^i
        self.d_v = d_v  # ones per row
        self.d_c = d_c
        self.snr = 100
        # First we create a small LDPC code i.e a pair of decoding and
        # coding matrices H and G. H is a regular parity-check matrix with d_v ones per row and d_c ones per column
        self.H, self.G = make_ldpc(n, d_v, d_c, systematic=True, sparse=True)
        self.k = self.G.shape[1]  # message length
        # print(self.k)

    def binary_to_decimal(self,binary):
        i, integer = 0, 0
        size = len(binary)
        while i < len(binary):
            integer += int(binary[size - 1 - i]) * pow(2, i)
            i += 1
        return integer

    def bin_array(self,num, m):
        """Convert a positive integer num into an m-bit bit vector"""
        return np.array(list(np.binary_repr(num).zfill(m))).astype(np.int8)

    def genKey(self):
        keys = np.random.randint(2, size=self.k)# here we leave 2*8 bits, we need to padding it as null
        keys_int = np.array([self.binary_to_decimal(keys[i * 8:(i + 1) * 8]) for i in range(int(len(keys) / 8))])
        return (keys,keys_int)

    def encode(self,value):
        ec = encode(self.G, value)  # polr code,encode into code with length n
        # print(len(ec))
        if len(ec) % 8 != 0:
            print("warning,dimension not agree")
        ec[ec==-1] = 0
        ec_int = np.array([self.binary_to_decimal(ec[i * 8:(i + 1) * 8]) for i in range(int(len(ec) / 8))])
        return (ec,ec_int)
    def decode(self,codes):
        d = decode(self.H, codes, self.snr, maxiter=1000)
        x = get_message(self.G, d)
        x_int = np.array([self.binary_to_decimal(x[i * 8:(i + 1) * 8]) for i in range(int(len(x) / 8))])
        return (x,x_int)


# LDPC_FE_Util = LDPC_FE_Util(144,3,16)# message 418 bits, encode into 512 bits
# # d_c must divide n for a regular LDPC matrix H
# # fuzzy vault 18 ints as key, 16bit + 2 bit error
# # 18*8=144 bits key length LDPC_FE_Util(119,3,16)
# keys,keys_int = LDPC_FE_Util.genKey()
# # print(np.shape(keys))
# # print(np.shape(keys_int))
# ec,ec_int = LDPC_FE_Util.encode(keys)
# # print(len(ec))
# # print(len(ec_int))
# # print(ec_int)
# decode_key, de_key_int = LDPC_FE_Util.decode(ec)
# # print(decode_key)
# assert abs(keys - decode_key).sum() == 0