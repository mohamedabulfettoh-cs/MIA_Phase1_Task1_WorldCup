"""
MD5 implemented from scratch, no hashlib.

I chose to implement MD5 as my checksum method because I am a cybersecurity student
and I already once worked on a hashcracker that required implementing SHA256
from scratch for CUDA to run it on my GPU so implementing MD5 felt like a good step
to refresh my memory of hashing algorithms

MD5, message digest 5 is a cryptographic hash algorithm that takes in 512 bit chunks
and outputs a 128 bit hash through bit manipulation and modular arithmetic

It works by keeping a running state of 128 bits that gets split into 4 32 bit 'words' that are
constantly updated through each of the 64 rounds of algorithm
The initial state is hardcoded to specific values and are often called A, B, C & D

K is a hardcoded array of 64 values that are derived from the sine function 
and are used in each round of the algorithm to add non-linearity to the hash function
as the sine function is non-linear and non-repeating

The message is padded to ensure that its length is congruent to 448 mod 512,
which means that the message is extended to be 64 bits short of a multiple of 512
where the value of the original message length is appended to the end of the padded message
to reach the 512 bit multiple to ensure proper processing of the message

M is the message broken into 512 bit chunks and then split into 16 32 bit words
S is the rotation amount for each round of the algorithm, it is hardcoded values that 
are used to rotate the bits of the state variables A, B, C & D in each round

A, D & C are directly updated to different values from the previous round
and B is updated to the sum of the previous value of B and the result of the left rotation
of the function F, which is a non-linear function that takes in the current state variables
and the current message word from g to calculate M[g] and produces a new value for B 

after all 64 rounds are completed, the final state variables A, B, C & D are added to the initial state
to produce the final hash value, which is then converted to a hexadecimal string and returned as the
MD5 hash of the input message

In the implementation of the algorithm, 32 bits masks are used to ensure that
the state variables and message words are always 32 bits long, as Python's integers can grow
unbounded which would break the algorithm. The left rotation function is also implemented to ensure that
the bits are rotated correctly and the result is always 32 bits long

Though from a cybersecurity prespective, MD5 is considered broken
and insecure as attackers could engineer collision attacks to produce
the same hash from different input messages
"""

import struct
import math


def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF


def md5(message: bytes) -> str:
    K = [int(abs(math.sin(i + 1)) * 2**32) & 0xFFFFFFFF for i in range(64)]

    # Per-round left-rotate amounts (4 groups of 16, one group per quarter)
    S = [7, 12, 17, 22] * 4 + \
        [5, 9, 14, 20] * 4 + \
        [4, 11, 16, 23] * 4 + \
        [6, 10, 15, 21] * 4

    # Initial state
    a0 = 0x67452301
    b0 = 0xefcdab89
    c0 = 0x98badcfe
    d0 = 0x10325476

    # Step 1: Padding 
    original_length_bits = (8 * len(message)) & 0xFFFFFFFFFFFFFFFF
    message += b"\x80"  # append '1' bit (10000000)
    while (len(message) % 64) != 56: # append 0 bits until the length is 64 bits short of a multiple of 512
        message += b"\x00"
    message += struct.pack("<Q", original_length_bits)  # append length to reach a multiple of 512 bits

    # Step 2: Process in 64-byte chunks 
    for chunk_start in range(0, len(message), 64):
        chunk = message[chunk_start:chunk_start + 64]
        M = list(struct.unpack('<16I', chunk))


        A, B, C, D = a0, b0, c0, d0

        # Step 3: 64 rounds
        
        for i in range(64):
            if 0 <= i <= 15:
                F = (B & C) | (~B & D)
                g = i
            elif 16 <= i <= 31:
                F = (D & B) | (~D & C)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                F = (B ^ C ^ D)
                g = (3 * i + 5) % 16
            else:
                F = (C ^ (B | ~D))
                g = (7 * i) % 16

            F = (F + A + K[i] + M[g]) & 0xFFFFFFFF
            
            A = D
            D = C
            C = B
            B = ( B + left_rotate(F, S[i])) & 0xFFFFFFFF
         
        a0 = (a0 + A) & 0xFFFFFFFF
        b0 = (b0 + B) & 0xFFFFFFFF
        c0 = (c0 + C) & 0xFFFFFFFF
        d0 = (d0 + D) & 0xFFFFFFFF

     # Step 4: Output
    return ''.join(f'{x:02x}' for x in struct.pack('<4I', a0, b0, c0, d0))    


class TicketCodec:
    """
    Encodes/decodes stadium ticket IDs with MD5 checksum
    """

    def _checksum(self, ticket_id):
        full_hash = md5(ticket_id.encode())
        return full_hash[:4]

    def encode(self, ticket_id):
        checksum = self._checksum(ticket_id)
        return f"{ticket_id}-{checksum}"

    def decode(self, barcode):
        ticket_id, _, embedded_checksum = barcode.rpartition("-")
        if self._checksum(ticket_id) == embedded_checksum:
            return ticket_id
        return "CORRUPTED TICKET"


if __name__ == "__main__":
    codec = TicketCodec()

    sample_ids = ["MIA2026GATE7", "MIA2026VIP0042", "MATE2027GATE1"]

    for TicketID in sample_ids:
        barcode = codec.encode(TicketID)
        print(f"Encoded version of {TicketID} -> {barcode}")
        print(f"Decoded: {barcode} -> {codec.decode(barcode)}")

    # Corrupt one character to test corrupted ticket handling
    barcode = codec.encode("MIA2026GATE7")
    corrupted = barcode.replace("7-", "4-", 1)  # change ticket ID digit
    print(f"\nCorrupted barcode: {corrupted}")
    print(f"Decode the corrupted barcode: {corrupted}) -> {codec.decode(corrupted)}")