import math
import time
from projectq import MainEngine
from projectq.ops import H, CNOT, Measure, Toffoli, X, All, T, Tdag, Swap
from projectq.backends import CircuitDrawer, ResourceCounter, ClassicalSimulator
from projectq.meta import Loop, Compute, Uncompute, Control

def Round_constant_XOR(eng, k, rc, bit):
    for i in range(bit):
        if (rc >> i & 1):
            X | k[i]

def left_rotation_a_b(eng, s, a_b):
    for i in range(5):
        print(i)
        with Control(eng, a_b[i]):
            for j in range(2 ** i):
                left_rotation_1bit(eng, s)

def left_rotation_1bit(eng, s):
    for i in range(31):
        Swap | (s[31 - i], s[30 - i])

def rotation_test(eng):
    s = eng.allocate_qureg(32)
    a_b = eng.allocate_qureg(32)

    Round_constant_XOR(eng, s, 0xff, 32)
    Round_constant_XOR(eng, a_b, 0b100000, 32)

    left_rotation_a_b(eng, s, a_b)

    All(Measure) | s
    All(Measure) | a_b

    for i in range(32):
        print(int(s[31 - i]), end='')

sim = ClassicalSimulator()
eng = MainEngine(sim)
rotation_test(eng)
eng.flush()
