import math

from projectq import MainEngine
from projectq.ops import H, CNOT, Measure, Toffoli, X, All, T, Tdag, S, Swap
from projectq.backends import CircuitDrawer, ResourceCounter, ClassicalSimulator
from projectq.meta import Loop, Compute, Uncompute, Control, Dagger

# w =32, r =12 ,b=16, t=26, c=4
# w =32, r =12 ,b=128bits    c =

def Round_constant_XOR(eng, k, rc, bit):
    for i in range(bit):
        if (rc >> i & 1):
            X | k[i]
    # print_state(eng,k,bit)

def print_state(eng, b, n):
    All(Measure) | b
    print('Result : ', end='')
    for i in range(n):
        print(int(b[n - 1 - i]), end='')
    print('\n')

def copy(eng, a, b, n):
    for i in range(n):
        CNOT | (a[i], b[i])

def Toffoli_gate(eng, a, b, c):
    if (resource_check):
        if (AND_check):
            ancilla = eng.allocate_qubit()
            H | c
            CNOT | (b, ancilla)
            CNOT | (c, a)
            CNOT | (c, b)
            CNOT | (a, ancilla)
            Tdag | a
            Tdag | b
            T | c
            T | ancilla
            CNOT | (a, ancilla)
            CNOT | (c, b)
            CNOT | (c, a)
            CNOT | (b, ancilla)
            H | c
            S | c

        else:
            Tdag | a
            Tdag | b
            H | c
            CNOT | (c, a)
            T | a
            CNOT | (b, c)
            CNOT | (b, a)
            T | c
            Tdag | a
            CNOT | (b, c)
            CNOT | (c, a)
            T | a
            Tdag | c
            CNOT | (b, a)
            H | c
    else:
        Toffoli | (a, b, c)

def CDKM(eng, a, b, c, n):
    for i in range(n - 2):
        CNOT | (a[i + 1], b[i + 1])

    CNOT | (a[1], c)
    Toffoli_gate(eng, a[0], b[0], c)
    CNOT | (a[2], a[1])
    Toffoli_gate(eng, c, b[1], a[1])
    CNOT | (a[3], a[2])

    for i in range(n - 5):
        Toffoli_gate(eng, a[i + 1], b[i + 2], a[i + 2])
        CNOT | (a[i + 4], a[i + 3])

    Toffoli_gate(eng, a[n - 4], b[n - 3], a[n - 3])
    CNOT | (a[n - 2], b[n - 1])
    CNOT | (a[n - 1], b[n - 1])
    Toffoli_gate(eng, a[n - 3], b[n - 2], b[n - 1])

    for i in range(n - 3):
        X | b[i + 1]

    CNOT | (c, b[1])

    for i in range(n - 3):
        CNOT | (a[i + 1], b[i + 2])

    Toffoli_gate(eng, a[n - 4], b[n - 3], a[n - 3])

    for i in range(n - 5):
        Toffoli_gate(eng, a[n - 5 - i], b[n - 4 - i], a[n - 4 - i])
        CNOT | (a[n - 2 - i], a[n - 3 - i])
        X | (b[n - 3 - i])

    Toffoli_gate(eng, c, b[1], a[1])
    CNOT | (a[3], a[2])
    X | b[2]
    Toffoli_gate(eng, a[0], b[0], c)
    CNOT | (a[2], a[1])
    X | b[1]
    CNOT | (a[1], c)

    for i in range(n-1):
        CNOT | (a[i], b[i])

def CDKM_minus(eng, a, b, c, n):
    with Dagger(eng):
        for i in range(n - 2):
            CNOT | (a[i + 1], b[i + 1])

        CNOT | (a[1], c)
        Toffoli_gate(eng, a[0], b[0], c)
        CNOT | (a[2], a[1])
        Toffoli_gate(eng, c, b[1], a[1])
        CNOT | (a[3], a[2])

        for i in range(n - 5):
            Toffoli_gate(eng, a[i + 1], b[i + 2], a[i + 2])
            CNOT | (a[i + 4], a[i + 3])

        Toffoli_gate(eng, a[n - 4], b[n - 3], a[n - 3])
        CNOT | (a[n - 2], b[n - 1])
        CNOT | (a[n - 1], b[n - 1])
        Toffoli_gate(eng, a[n - 3], b[n - 2], b[n - 1])

        for i in range(n - 3):
            X | b[i + 1]

        CNOT | (c, b[1])

        for i in range(n - 3):
            CNOT | (a[i + 1], b[i + 2])

        Toffoli_gate(eng, a[n - 4], b[n - 3], a[n - 3])

        for i in range(n - 5):
            Toffoli_gate(eng, a[n - 5 - i], b[n - 4 - i], a[n - 4 - i])
            CNOT | (a[n - 2 - i], a[n - 3 - i])
            X | (b[n - 3 - i])

        Toffoli_gate(eng, c, b[1], a[1])
        CNOT | (a[3], a[2])
        X | b[2]
        Toffoli_gate(eng, a[0], b[0], c)
        CNOT | (a[2], a[1])
        X | b[1]
        CNOT | (a[1], c)

        for i in range(n-1):
            CNOT | (a[i], b[i])

def ROTL3(eng,A,n):
    new_A=[]
    for i in range(32-n,32):
        new_A.append(A[i])

    for i in range(29):
        new_A.append(A[i])

    return new_A

def left_rotation_a_b(eng, s, a_b):
    for i in range(5):
        with Control(eng, a_b[i]):
            for j in range(2 ** i):
                left_rotation_1bit(eng, s)

def left_rotation_1bit(eng, s):
    for i in range(31):
        Swap | (s[31 - i], s[30 - i])

def CNOT32(eng,A,B):
    for i in range(32):
        CNOT | (A[i],B[i])

def RC5_SETUP(eng,key,S):
    A = eng.allocate_qureg(32)
    B = eng.allocate_qureg(32)
    c = eng.allocate_qubit()

    SS=[0]*26
    SS[0] = 0xb7e15163
    QQ = 0x9e3779b9
    for i in range(1,26):
        SS[i] = (SS[i-1]+ QQ) & 0xFFFFFFFF

    for i in range(26):
        Round_constant_XOR(eng, S[32 * i:32 * (i + 1)], SS[i], 32)

    new_B = eng.allocate_qureg(32)

    for i in range(78):
        CDKM(eng, B, S[(32 * (i % 26)):32 * ((i % 26) + 1)], c, 32)
        CDKM(eng, A, S[(32 * (i % 26)):32 * ((i % 26) + 1)], c, 32)
        A = S[(32 * (i % 26)):32 * ((i % 26) + 1)] = ROTL3(eng, S[(32 * (i % 26)):32 * ((i % 26) + 1)], 3)

        CDKM(eng, A, B, c, 32)
        CDKM(eng, B, key[32 * (i % 4): 32 * ((i % 4) + 1)], c, 32)
        left_rotation_a_b(eng,key[32 * (i % 4) : 32 * ((i % 4) + 1)], B)

        if(i==0):
            copy(eng, key[32 * (i % 4): 32 * ((i % 4) + 1)], new_B, 32)
        else:
            CDKM_minus(eng,A,new_B,c,32)
            copy(eng,key[32 * ((i - 1) % 4) : 32 * (((i - 1) % 4) + 1)],new_B,32)
            copy(eng,key[32 * (i % 4) : 32 * ((i % 4) + 1)],new_B,32)

        B = new_B


def RC5_Encrypt(eng,A,B,S):
    c = eng.allocate_qubit()

    CDKM(eng,S[0:32],A,c,32)
    CDKM(eng,S[32:64],B,c,32)

    for i in range(12): # (1,13):
        CNOT32(eng,B,A)
        left_rotation_a_b(eng,A,B)
        CDKM(eng,S[32*(2*i+2):32*(2*i+3)],A,c,32)
        CNOT32(eng,A,B)
        left_rotation_a_b(eng,B,A)
        CDKM(eng,S[32*(2*i+3):32*(2*i+4)],B,c,32)

    if(resource_check!=1):
        print_state(eng,A,32)
        print_state(eng,B,32)

def RC5(eng):
    pt = eng.allocate_qureg(32)
    pt2 = eng.allocate_qureg(32)
    key = eng.allocate_qureg(128)
    S = eng.allocate_qureg(832)

    RC5_SETUP(eng,key,S)
    RC5_Encrypt(eng,pt,pt2,S)




global resource_check
global AND_check
# print('Generate Ciphertext...')
# resource_check = 0
# classic = ClassicalSimulator()
# eng = MainEngine(classic)
# RC5(eng)
# eng.flush()
# print('\n')

print('Estimate cost...')
resource_check = 1
AND_check = 0
Resource = ResourceCounter()
eng = MainEngine(Resource)
RC5(eng)
print('\n')
print(Resource)
eng.flush()