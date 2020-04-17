import random as rd

from quantize_reconcile_amplify_privacy import dichot, quant_chunks

_n = 0
_passes = 4
_permutations = list()
_current_init = list()
_current_resp = list()

MAX_FRAC_FOR_BLOCKSIZE = 4
_basicBlockSize = 10
_blocksize = list()

_errors = list()
_allErrors = 0
_fixedPositions = list()
_disclosed = 0
_passDisclosed = list()

##  Compute the number of mismatches between bits_init & bits_resp
def find_mismatch_num(bits_init, bits_resp):
    mismatch_num = 0
    for i in range(len(bits_resp)):
        if (bits_init[i] != bits_resp[i]):
            mismatch_num += 1
    return mismatch_num


##	Returns the observed error-rate [bit error probability (mismatch)]
#   @return the number of errors found divided by the plain key length
def bit_error_rate(bits_init, bits_resp):
    mismatch_num = find_mismatch_num(bits_init, bits_resp)
    Pe = mismatch_num / len(bits_resp)
    return Pe


##  Allows to set the default initial block size given an estimate on the
#   probability of errors for each bit.
#   @param p is the probility of error for each bit that will be corrected.
#   For that method to work, p must be a such that 0<p<1/2.
#   @return the computed default initial block size. The value -1 is returned
#   if the value of p was not appropriate.
def setBasicBlockSize(Pe):
    s = -1
    if (Pe < 0.5) and (Pe > 0):
        s = round(1.5 / Pe)
        # s = round(0.73 / Pe)
        # s = round(0.14 / Pe)
    return s


##	Returns the observed error-rate [bit error probability (mismatch)]
#   @return the number of errors found divided by the plain key length
def obsErrorRate():
    Pe = errorsFound() / _n
    return Pe

##  Sets the starting paramaters for next Cascade execution.
#   @param bits      are the bits to which Cascade is applied.
#   @param passes    is the number of passes.
#   @param blocksize is the initial block size.
def setParam(bits_init, bits_resp, blocksize, passes):
    global _n
    _n = len(bits_init)
    global _current_init
    _current_init = bits_init
    global _current_resp
    _current_resp = bits_resp
    global _passes
    _passes = passes
    global _errors
    _errors = [0 for i in range(passes)]
    global _allErrors
    _allErrors = 0
    global _basicBlockSize
    _basicBlockSize = blocksize
    global _blocksize
    _blocksize.append(blocksize)
    for i in range(1, _passes):
        if (_blocksize[i - 1] < (len(bits_init) / MAX_FRAC_FOR_BLOCKSIZE)):
            _blocksize.append(2 * _blocksize[i - 1])
        else:
            _blocksize.append(_blocksize[i - 1])
    global _fixedPositions
    _fixedPositions = list()
    global _disclosed
    _disclosed = 0
    global _passDisclosed
    _passDisclosed = [0 for i in range(passes)]
    return _n, _current_init, _current_resp, _passes, _errors, _allErrors, \
            _blocksize, _fixedPositions, _disclosed, _passDisclosed


##  Generates a new random permutation of the integers between [0..n-1].
#   @param n is such that a random permutation between the numbers
#   in [0..n-1] will be generated.
#   @return an array p[] such that p[0],p[1],...,p[n-1] is the new permutation.
def newPermutation(n):
    v = list(range(n))
    perm = list()
    for i in range(0, n):
        rp = rd.randint(0, len(v) - 1)
        rim = v.pop(rp)
        perm.append(rim)
    return perm


##  Returns the number of blocks in a pass involving n bits using blocks of given size.
#   @param n         is the number of bits.
#   @param blockSize is the blocksize.
#   @return the number of blocks for that pass.
def numberOfBlocks(n, blockSize):
    res = n / blockSize
    if ((n % blockSize) != 0):
        res += 1
    return int(res)


##  Extracts and returns a block of consecutive bits in the current bit string
#   for a given pass. The block indices start at 0. The behaviour is not
#   guaranteed when the index given exceeds the upper bound of the bit string.
#   @param i    is the index of the block starting at 0.
#   @param pass is the pass for which the block is computed
#   @return the i-th block of length k based on the bits in _current at his point.
def getBlocks(i, passe):
    blknumber = numberOfBlocks(_n, _blocksize[passe])
    size = _blocksize[passe]
    if ((i < blknumber - 1) or (_n % _blocksize[passe] == 0)):
        bk_init = [0] * size
        bk_resp = [0] * size
    else:
        bk_init = [0] * (_n % size)
        bk_resp = [0] * (_n % size)
    for j in range(0, _n):
        x = _permutations[passe]
        y = x[j]
        if (whichBlock(y, size) == i):
            bk_init[y % size] = _current_init[j]
            bk_resp[y % size] = _current_resp[j]
    return bk_init, bk_resp


##  Returns the block index containing the given bit position. All indices start
#   at position 0.
#   @param i is the position
#   @param k is the blocksize
#   @return the index of the block of length k containing position i.
def whichBlock(i, k):
    return int(i / k)

##  Returns the number of errors corrected during the execution of a given pass.
#   @param pass is the pass (starting at 0) to look for
#   @return the number of errors during the execution of the given pass.
def errorsFound1(passe):
    ans = 0
    if ((passe >= 0) and (passe < _passes)):
        ans = _errors[passe]
    return ans

##  Returns the total number of errors found during the execution of the protocol.
#   @return the total number of errors found and corrected.
def errorsFound():
    ans = 0
    for i in range(0, _passes):
        ans = ans + errorsFound1(i)
    return ans

##  Returns the original position of a position in the image of a given permutation.
#   @param i is the position after permutation
#   @param p is the permutation to invert
#   @return j such that p(j)=i or -1 if the inputs were faulty.
def invert(i, p):
    found = -1
    j = 0
    while ((found < 0) and (j < len(p))):
        if (p[j] == i):
            found = j
        j += 1
    return found

##  Returns the number of parity bits exchanged during the last execution of the
#   protocol. If this protocol is executed as a thread, make sure that this
#   method is called once the execution is resumed. Otherwise, the value returned
#   will be the current one in the execution.
#   @return the number of parity bits about the initial bitstring transmitted
#	through the public channel.
def disclosed():
    return _disclosed

##  Returns the number of patiry bits revealed at a given pass.
#   @param i is the pass number [0..maxpass-1]
#   @return the number of revealed parity bits for pass i.
def disclosed1(i):
    return _passDisclosed[i]

##  Produces an output for debugging purposes. The statistics are also indicated.
##  @returns the identical bit string resulting after applying cascade
def output():
    print("---Cascade Statistics---")
    print("There were ", errorsFound(), " errors found and corrected:")
    print("There obs Error Rate: ", obsErrorRate())
    # for i in range(0, _passes):
    #     print("       * ", errorsFound1(i), " in pass " , i)
    print("The total number of disclosed bits is ", disclosed())
    # print("The Resulting string is:")
    # for i in range(0, _n):
    #     print("bit #", i, " is ", _current_init[i])
    if (_current_init == _current_resp):
        print("They are equal now")
        return _current_init, disclosed()
    else:
        print("Not totally corrected")


##  bits_init of initiator, to be corrected to be = bits_resp
def cascade(bits_init, bits_resp, blocksize, passes):
    prev_disclosed = 0
    for i in range(0, passes):
        global _permutations
        _permutations.append(newPermutation(len(bits_init)))

    global _n, _current_init, _current_resp, _passes, _errors, _allErrors, \
        _blocksize, _fixedPositions, _disclosed, _passDisclosed

    _n, _current_init, _current_resp, _passes, _errors, _allErrors, \
    _blocksize, _fixedPositions, _disclosed, _passDisclosed = \
    setParam(bits_init, bits_resp, blocksize, passes)

    for passe in range(0, _passes):
        numberOfBlock = int(numberOfBlocks(_n, _blocksize[passe]))

        for blkindex in range(0, numberOfBlock):

            block_init, block_resp = getBlocks(blkindex, passe)
            d = dichot.Dichot(block_init, block_resp)

            if (d.test(block_init, block_resp)):
                errorpos = d.search(block_init, block_resp)
                realcurrentpos = errorpos + (blkindex * _blocksize[passe])
                basicPos = invert(realcurrentpos, _permutations[passe])
                # print(basicPos)
                _current_init[basicPos] = int(not(_current_init[basicPos]))
                _fixedPositions.append(basicPos)
                _errors[passe] = _errors[passe] + 1
                _allErrors += 1
                stack = BlockStack(passe, _permutations, _blocksize)
                stack.addBlocks(basicPos, passe, -1)
                #	We now empty the stack by finding new errors in the smallest blocks in the stack.
                while (not(stack.empty())):
                    smallerBlock = stack.getSmallestBlock()
                    block_init, block_resp = getBlocks(smallerBlock[0], smallerBlock[1])
                    newBadBlock = dichot.Dichot(block_init, block_resp)
                    errorpos = newBadBlock.search(block_init, block_resp)

                    _errors[passe] = _errors[passe] + 1
                    _allErrors += 1
                    if (errorpos >= 0):
                        realcurrentpos = errorpos + (smallerBlock[0] * _blocksize[smallerBlock[1]])
                        basicPos = invert(realcurrentpos, _permutations[smallerBlock[1]])
                        # print(basicPos)
                    else:
                        print("Cascade is running into troubles.")
                    _current_init[basicPos] = int(not(_current_init[basicPos]))
                    _fixedPositions.append(basicPos)
                    stack.addBlocks(basicPos, passe, blkindex)
                    _disclosed = _disclosed + newBadBlock.disclosed()
        _disclosed = _disclosed + d.disclosed()
        _passDisclosed.append(_disclosed - prev_disclosed)
        prev_disclosed = _disclosed
    _blocksize.clear()
    _passDisclosed.clear()
    _fixedPositions.clear()
    _permutations.clear()


##  This class implements a stack of blocks where an
#   odd numbers of errors has been detected.
class BlockStack():
    def __init__(self, npasse, perms, blksize):
        self._perms = perms
        self._blksize = blksize
        self._stack = [[] for i in range(0,npasse+1)]


    #	This method adds in the stack the new blocks with odd parity resulting in a
    #   new error found in some position relative to the unpermuted bit string. It
    #   also removes all blocks already in the stack which contains the new
    #   position and therefore return to an even parity.
    #   @param pos    is the position of the new error relative to the unpermuted array
    #   @param pass   is the last pass to search for odd parity blocks
    #   @param maxblk is the max index of the last block in the last pass to look for
    #   odd parity blocks.
    def addBlocks(self, pos, passe, maxblk):
        for i in range(0, passe+1):
            posi = _permutations[i][pos]
            blocki = whichBlock(posi, _blocksize[i])
            if ((blocki <= maxblk) or (i < passe)):
                whereitis = self.alreadyThere(blocki, i)
                if (whereitis >= 0):
                    self._stack[i].pop(whereitis)
                else:
                    self._stack[i].append(blocki)


    #   Returns true if the given block index appears in the stack for a certain pass.
    #   @param blkindex is the index of the block
    #   @param pass     is the pass we are interested in
    #   @return the position in the stack where the block index is. The value -1 is
    #   returned if the block index does not appear in the stack.
    def alreadyThere(self, blkindex, passe):
        where = -1
        found = False
        i = 0
        if len(self._stack) > passe:
            while (i < len(self._stack[passe]) and not(found)):
                bindex = int(self._stack[passe][i])
                found = (bindex == blkindex)
                if (found):
                    where = i
                i += 1
        return where

    #	Gets the block of in the earlier pass that appears in the stack. These are
    #   the smallest blocks since the blocksize increases with the pass number. The
    # 	element is not removed from the stack since it is going to be removed in the
    # 	next call to addBlocks.
    # 	@return an array r[][] such that r[0] is the block index and r[1] is the pass
    # 	where the block has been found. Returns {-1,-1} if no block are left in the stack.
    def getSmallestBlock(self):
        out = [-1, -1]
        if (not (self.empty())):
            emptypasse = True
            i = 0
            while (i < len(self._stack) and (emptypasse)):
                emptypasse = (len(self._stack[i]) == 0)
                if (not (emptypasse)):
                    out[0] = int(self._stack[i][0])
                    out[1] = i
                i += 1
        return out

    #   Returns whether or not the stack is empty
    def empty(self):
        ans = True
        i = 0
        while (i < len(self._stack) and (ans)):
            if (len(self._stack[i]) > 0):
                ans = False
            i += 1
        return ans


if (__name__) == "__main__":

    ## NOTE:
    # Number of passes need to be set correctly and large enough to correct the error
    # parameters effect:
    # number of passes, basic block size, number of mismatches effect
    # the probability of achieving equal strings

    ## *  (Example_Tests)  Data generated randomly for test purpose:
    ##  Example_Test_1:
    # cleaned_qts_init = [1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1]
    # cleaned_qts_resp = [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1]

    ##  Example_Test_2:
    # cleaned_qts_init = [rd.getrandbits(1) for i in range(0, 256)]
    cleaned_qts_init = [0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0,\
     0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1,\
     1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0,\
     1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1,\
     0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1,\
     0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0,\
     0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1]
    cleaned_qts_resp = cleaned_qts_init.copy()
    cleaned_qts_resp [10] = int(not(cleaned_qts_init[10]))
    cleaned_qts_resp [25] = int(not(cleaned_qts_init[25]))
    cleaned_qts_resp [33] = int(not(cleaned_qts_init[33]))
    cleaned_qts_resp [55] = int(not(cleaned_qts_init[55]))
    cleaned_qts_resp [81] = int(not(cleaned_qts_init[81]))
    cleaned_qts_resp [74] = int(not(cleaned_qts_init[74]))
    cleaned_qts_resp [105] = int(not(cleaned_qts_init[105]))
    cleaned_qts_resp [145] = int(not(cleaned_qts_init[145]))
    cleaned_qts_resp [170] = int(not(cleaned_qts_init[170]))
    cleaned_qts_resp [200] = int(not(cleaned_qts_init[200]))

    ##------------------------------------------------------------------------------------------------------------------

    ##  @ 1_ ASBG  Method from paper:
    #   Premnath, S. N., S. Jana, J. Croft, P. L. Gowda, M. Clark, S. K. Kasera, N. Patwari,  and S. V. Krishnamurthy
    #   , 2013 May, “Secret key extraction from wireless signal strength in real environments,

    ##  @ 2_ Level Crossing  Method from paper:
    #     Mathur, Suhas,Wade Trappe, Narayan Mandayam, Chunxuan Ye, and Alex Reznik, 2008, “Radio-telepathy:
    #     Extracting a secret key from an unauthenticated wireless channel,”

    path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Amplitude Expers\\dtw exp\\my_dtw\\6_250_45"
    first_file_num = 0
    last_file_num = 10
    step_size = 1000

    method = "ASBG"                 # quantization method_1
    # method = "Level_Crossing"     # quantization method_2

# ----------------------------------------------------------------------------------------------------------------------
    if (method == "ASBG"):
        chunk_size = 25
        alpha = 0.8

        # #   1- equal to step_size:
        # #   @call:   quantization(path, range_start, range_end, alpha)
        # # cleaned_qts_resp, cleaned_qts_init = quant_stepsize.quantization(path, first_file_num, last_file_num, alpha)
        #
        # #   @call:   quantization(path, range_start, range_end, step_size, chunk_size, alpha)
        # #   if chunk_size = step_size you are doing as quant_stepsize.quantization
        cleaned_qts_resp, cleaned_qts_init = quant_chunks.quantization(path, first_file_num, last_file_num, 'init_', 'second_', step_size, chunk_size, alpha)

        # print(cleaned_qts_resp)
        print("Responder string length before reconciliation:" , len(cleaned_qts_resp))
        # print(cleaned_qts_init)
        print("Initiator string length before reconciliation:" , len(cleaned_qts_init))

        if (cleaned_qts_resp != cleaned_qts_init):
            print("Key stings are not equal and they need reconciliation (cascade)")

        print("Mismatches number = ", find_mismatch_num(cleaned_qts_init, cleaned_qts_resp))
        Pe = bit_error_rate(cleaned_qts_init, cleaned_qts_resp)
        print("bit error rate (probability) Pe: ", Pe)
        size = setBasicBlockSize(Pe)
        print("basic block size: ", size)
        print()
        cascade(cleaned_qts_init, cleaned_qts_resp, size,4)
        Initial_Shared_Key = output()
        print()
        print("----Cascade----")
        print("Initial_Shared_Key --- of length", len(Initial_Shared_Key), "is: ")
        print(Initial_Shared_Key)


# ----------------------------------------------------------------------------------------------------------------------
#     elif (method == "Level_Crossing"):
#         L_size = 150
#         m = 4
#         alpha = 0.4
#
#         k_resp, k_init = level_crossing.basic_level_algo(path, first_file_num, last_file_num, step_size, L_size, m, alpha)
#         # print(k_resp)
#         # print(len(k_resp))
#         # print(k_init)
#         # print(len(k_init))
#         if (k_resp == k_init):
#             print("Yes, keys are equal")
#         else:
#             print("No, keys are not equal need reconciliation step (cascade)")
#
#         print("mismatch_num = ", find_mismatch_num(k_init, k_resp))
#         Pe = bit_error_rate(k_init, k_resp)
#         print("bit error rate (probability) Pe: ", Pe)
#
#
#         size = setBasicBlockSize(Pe)
#         print("basic block size: ", size)
#         print()
#         cascade(k_init, k_resp, size, 40)
#         output()