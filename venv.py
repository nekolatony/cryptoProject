class DH_Endpoint(object):
    def __init__(self, public_key1, public_key2, private_key):
        self.public_key1 = public_key1
        self.public_key2 = public_key2
        self.private_key = private_key
        self.full_key = None

    def generate_partial_key(self):
        partial_key = self.public_key1 ** self.private_key
        partial_key = partial_key % self.public_key2
        return partial_key

    def generate_full_key(self, partial_key_r):
        full_key = partial_key_r ** self.private_key
        full_key = full_key % self.public_key2
        self.full_key = full_key
        return full_key

sharedBase = 197
privateKeyAlice = 199
sharedPrime = 151
privateKeyBob = 157

Alice = DH_Endpoint(sharedBase, sharedPrime, privateKeyAlice)
Bob = DH_Endpoint(sharedBase, sharedPrime, privateKeyBob)
alicePartialKey=Alice.generate_partial_key()
print(alicePartialKey) #147
bobPartialKey=Bob.generate_partial_key()
print(bobPartialKey)
aliceFullKey=Alice.generate_full_key(bobPartialKey)
print(aliceFullKey) #75
bobFullKey=Bob.generate_full_key(alicePartialKey)
print(bobFullKey) #75
