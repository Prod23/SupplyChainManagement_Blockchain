import hashlib
import binascii


class MerkleTree(object):
    def __init__(self, hash_type):
        hash_type = "SHA256"
        hash_type = hash_type.lower()
        self.hash_function = getattr(hashlib, hash_type)
        self.reset_tree()

    def reset_tree(self):
        self.leaves = list()
        self.levels = None
        self.tree_ready = False    

    def _to_hex(self, x):
        try:  # python3
            return x.hex()
        except:  # python2
            return binascii.hexlify(x)

    def add_leaf(self, values, do_hash=False):#do hash mean - value should be hashed before adding them as leaf nodes.
        self.tree_ready = False
     
        if not isinstance(values, tuple) and not isinstance(values, list): # checks if it is a single leaf 
            values = [values]
        for v in values:
            if do_hash:
                v = v.encode('utf-8')
                v = self.hash_function(v).hexdigest()
            v = bytearray.fromhex(v) #transaction details should be visible in the block.
            self.leaves.append(v) #adding the leaf to the leaves

    def get_leaf(self, index):
        return self._to_hex(self.leaves[index])

    def get_leaf_count(self):
        return len(self.leaves)

    def get_tree_ready_state(self):
        return self.tree_ready

    def _calculate_next_level(self):
        solo_leaf = None

        N = len(self.levels[0])  # number of leaves on the level
        if N % 2 == 1:  # if odd number of leaves on the level
            solo_leaf = self.levels[0][-1]
            N -= 1

        new_level = []
        for l, r in zip(self.levels[0][0:N:2], self.levels[0][1:N:2]):#l and r child nodes.
            new_level.append(self.hash_function(l+r).digest())
        if solo_leaf is not None:
            new_level.append(self.hash_function(solo_leaf+solo_leaf).digest()) #hashing the solo node by duplicating it.
        self.levels = [new_level, ] + self.levels  # prepend new level

    def make_tree(self):
        self.tree_ready = False
        if self.get_leaf_count() > 0:
            self.levels = [self.leaves, ]
            while len(self.levels[0]) > 1:
                self._calculate_next_level()
        self.tree_ready = True

    def generate_merkle_root(self):
        if self.tree_ready:
            if self.levels is not None:
                return self._to_hex(self.levels[0][0])
            else:
                return None
        else:
            return None

