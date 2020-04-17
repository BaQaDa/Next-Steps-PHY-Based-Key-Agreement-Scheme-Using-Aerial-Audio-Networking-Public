import math

#  This class implements the interactive dichotomic search
#  of an error. This is the basic primitive for correcting
#  errors in Cascade. A public connection is required for
#  executing the protocol. Each instance of that class remember
#  the number of bits disclosed over the public channel. This
#  is usefull when privacy amplification takes place. For practical
#  reason, this class is not a subclass of quantum protocol since
#  it has no application by its own. It is rather a procedure
#  that can be called from quantum protocol.
class Dichot:

    def __init__(self, block_init, block_resp):
        self._block_init = block_init
        self.block_resp = block_resp
        self._disclose = 0


    ##  This returns the number of bits transmitted over the
    #   public channel about the original bit string. All those
    #   bits of information are parity bits. Knowing the number
    #   of parity bits disclosed to an eavesdropper allows to
    #   remove them during privacy amplification.
    #   @return the number of parity bits disclosed to a potential
    #   eavesdropper so far.
    def disclosed(self):
        return self._disclose


    ##  Returns the parity of the block between two indices.
    #   @param i is the left index
    #   @param j is the right index
    #   @return false iff the number of true in b_i+b_{i+1}+...+b_j is even.
    def parity1(self, i, j, block):
        ans = block[i]
        for h in range(i + 1, j + 1):
            ans ^= block[h]
        return ans


    ##  Returns the parity of the whole block.
    #   @return false iff the number of true is even
    def parity(self,block):
        return self.parity1(0, len(block) - 1, block)


    ##  Test whether or not the parity of this block is the same
    #   for both parties.
    #   @param initiator is true if the protocol on the initiator side.
    #   Otherwise initiator os false.
    #   @return true iff at least one error exists
    #   @exception TimeOutException is thrown as usual.
    def test(self, block_init, block_resp):
        p = self.parity(block_init)
        q = self.parity(block_resp)
        self._disclose += 1
        return (p != q)


    ##  This method search for an error in a odd-parity block.
    #   @param initiator is true if the protocol is run
    #   on initiator side and is false otherwise.
    #   @return the position in the block where the error
    #   has been found. If the method is called on an even-parity
    #   block then the outcome is unpredictable.
    #   @exception TimeOutException is thrown as usual.
    def search(self, block_init, block_resp):
        j = len(block_init) - 1
        i = 0
        while (i < j):
            mid = math.floor((i + j) / 2)
            p = self.parity1(i, mid, block_init)
            q = self.parity1(i, mid, block_resp)
            if (p == q):
                i = mid + 1
            else:
                j = mid
            global _disclosed
            self._disclose += 1
        return j






