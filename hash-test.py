import sha3
import struct

def getLargestPowOfTwo(number):
    approx = 2
    while(approx < number):
        approx = approx << 1
    return approx >> 1

def getParts(txlist):
    l = len(txlist)
    m = getLargestPowOfTwo(l)
    return txlist[0:2*m-l], txlist[2*m-l:l]

def hashTogether(secondpart):
    txhased = [_hash(tx) for tx in secondpart]
    l = len(txhased)
    pairhashed = []
    for i in range(0, l, 2):
        pair = txhased[i] + txhased[i + 1]
        pairhashed.append(_hash(pair))
    return pairhashed

def getMerkleRoot(hasheslist):
    l = len(hasheslist)
    if(l == 1):
        return hasheslist[0]

    newtxlist = []

    for i in range(0, l, 2):
        pair = hasheslist[i] + hasheslist[i + 1]
        newtxlist.append(_hash(pair))

    return getMerkleRoot(newtxlist)

def _hash(tx):
    txbin = tx.decode('hex')
    return sha3.keccak_256(txbin).hexdigest()

def getBlockHeader(major_v, minor_v, timestamp, prev_block, nonce):
    block_header = ''
    block_header += struct.pack('>B', major_v)
    block_header += struct.pack('>B', minor_v)
    block_header += struct.pack('>L', timestamp)
    block_header += prev_block.decode('hex')
    #block_header += struct.pack('>L', nonce)
    block_header += nonce.decode('hex')
    return block_header#.encode('hex')

def getSize(blob):
    return struct.pack('>B', len(blob.encode('hex')))

#hasheslist = [str(0) + str(i) for i in range(0,9)]

hasheslist = ['868e592290144e6a3b8bcc75adc7dd367ed5a1907d45fb2810b1a99c1cce29ba',
              '357f00c6c3e2996a62460f2f388cd68986a02c5cc4349c902f9856b21d2bc972',
              '3c1d934b7817d5fd625962e738e0efb706c964e5c786e40b3c549fc8d58134b2',
              '34ad7ee52ba99cd9f0db4401cef37be0c377a184d388e2f24636fed5cfb13d92']

firstpart, secondpart = getParts(hasheslist)

firstparthashed = [_hash(tx) for tx in firstpart]
secondparthased = hashTogether(secondpart)

prepared = firstparthashed + secondparthased
root = getMerkleRoot(prepared)

print 'Merkle root: %s' % root

# https://monerohash.com/explorer/block/1447804
# block header
major_v = 6
minor_v = 6
timestamp = 1511267661 #5a141d4d
prev_block = '1afae33a3523f8cbd453cf54c130b89d8dfdf42034e25eb6899b0b929f7f958f'
nonce = '054326'

block_header = getBlockHeader(major_v, minor_v, timestamp, prev_block, nonce)
block_size = getSize(block_header)
tx_in = 4

#blob = struct.pack('>b', block_size) + block_header + root.decode('hex')
blob = block_header + root.decode('hex') + struct.pack("<L", tx_in)
blob = getSize(blob) + blob

print 'blob: %s' % blob.encode('hex')

print _hash(blob.encode('hex'))
