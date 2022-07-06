import random
import math
n = 0
s = 0
c = list()

##  Check if k-th bit of a given number is set or not
def testBit(n, k):
    if n & (1 << (k)):
        return True
    else:
        return False


##  Set the kth bit of the given number
def setBit(n, k):
    return ((1 << k) | n)


##  @returns a number that has all bits same as n
#   except the k'th bit which is made 0
def clearBit(n, k):
    if (k < 0):
        return n
    return (n & ~(1 << (k)))


##  @returns the number of bits in the binary representation of integer
def setBitCount(n):
    count = 0
    while (n):
        count += n & 1
        n >>= 1
    return count


# Function to count total bits in a number
def countTotalBits(number):
    # log function in base 2
    # take only integer part
    return int((math.log(number) /
                math.log(2)) + 1);

##  Transforms bitlist into integer representation
def bitListToInt(bitlist):
    out = 0
    for bit in bitlist:
        out = (out << 1) | bit
    return out

##  Transforms booleanList into bitList representation
def booleanListToBitList(boolList):
    bitList = list()
    for i in range(0, len(boolList)):
        if (boolList[i]):
            bitList.append(1)
        else:
            bitList.append(0)
    return bitList


##  initHash initializes the hash matrix with a hash function
#   given by a seedVector and a shift vector.
def initHash(ss, nn, shift_vect, seed_vect):
    global n
    n = nn
    global s
    s = ss
    global c
    c = [0 for i in range(s)]
    c[0] = seed_vect
    for column in range(1, s):
        seed_vect = seed_vect >> 1  # Leftmost bit is now 0. We need to put one of the
        # random bits from shift_bits in that position.
        if (testBit(shift_vect, column)):
            seed_vect = setBit(seed_vect, n - 1)
        else:
            seed_vect = clearBit(seed_vect, n - 1)
        c[column] = seed_vect
    print ("cc =", c)


##  newHash initializes the hash matrix randomly.
def newHash(s, n):
    seed_vect = random.getrandbits(n)
    shift_vect = random.getrandbits(s)
    initHash(s, n, shift_vect, seed_vect)

def doHashBitvector(bitvector):
    t_in = bitvector
    t_out = random.getrandbits(s)
    for column in range(0, s):
        andVect = t_in & c[column]
        numBits = setBitCount(andVect)
        ## If parity of numBits is even, we clear the bit, otherwise set it.
        if ((numBits & 1) == 1):
            t_out = setBit(t_out, column)
        else:
            t_out = clearBit(t_out, column)
    return t_out


##  doHash hashes a given boolean[] bitvector with the given hash function.
def doHash(boolvector):
    bitvector_in = random.getrandbits(len(boolvector))
    bitvector_out = random.getrandbits(len(boolvector))
    hashedboolvector = [False for i in range(s)]
    for i in range(0, len(boolvector)):
        if (boolvector[i]):
            bitvector_in = setBit(bitvector_in, i)
        else:
            bitvector_in = clearBit(bitvector_in, i)
    bitvector_out = doHashBitvector(bitvector_in)
    for i in range(0, s):
        hashedboolvector[i] = testBit(bitvector_out, i)
    return hashedboolvector


def amplify_privacy(bits, desired_size):
    # if (desired_size > len(bits)):
    #     print(" Failed, desired_size is larger than the inout length !!! ")
    # else:
    inBits = bits
    inBitsN = len(bits)
    outBitsN = desired_size
    # newHash includes initHash to prepare the parameters
    newHash(outBitsN, inBitsN)
    outBits = doHash(inBits)
    outBitsList = booleanListToBitList(outBits)
    return outBitsList


if __name__ == "__main__":
    INITIAL_KEY = [False, True, True, True, False, False]
    Final_Shared_Key = amplify_privacy(INITIAL_KEY, 3)
    print()
    print("----Privacy Amplification----")
    print("Final_Shared_Key --- of length", len(Final_Shared_Key), "is: ")
    print(Final_Shared_Key)


