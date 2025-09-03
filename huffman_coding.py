def create_freqs(text):  #freqs is a dictionary with characters as keys and their frequencies as values
    freqs = Counter(text)
    return freqs

def find_total(freqs):
    return sum(freqs.values())

def find_probs(freqs, total):
    probs = []
    for f in freqs.values():
        if f > 0:
            probs.append(f / total)
    return probs

def measure_entropy(probs):
    entropy = 0
    for p in probs:
        entropy += p * math.log2(p)
    entropy = -entropy
    return entropy

def push_nodes(freqs, heap, nodes):
    for symbol in freqs:
        node=Node(freq=freqs[symbol],symbol=symbol)
        heapq.heappush(heap, (node.freq,node))
        nodes.append(node)
def find_root(heap, nodes):
    while len(heap)>1:
        f1, n1 = heapq.heappop(heap)
        f2, n2 = heapq.heappop(heap)
        parent = Node(f1+f2,symbol=None, left=n1, right=n2)
        nodes.append(parent)
        heapq.heappush(heap,(parent.freq,parent))
    return heapq.heappop(heap)[1]

def make_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}
    if node is not None:
        # Leaf node: assign code
        if node.left is None and node.right is None:
            codebook[node.symbol] = prefix
        else:
            make_codes(node.left, prefix + "0", codebook)
            make_codes(node.right, prefix + "1", codebook)
    return codebook

def encode(text, codebook):
    encoded_text = ""
    for symbol in text:
        encoded_text += codebook[symbol]
    return encoded_text

def decode(encoded_text, root):
    decoded_text = ""
    node = root
    for bit in encoded_text:
        if bit == "0":
            node = node.left
        elif bit == "1":
            node = node.right
        if node.left is None and node.right is None:
            decoded_text += str(node.symbol)
            node = root
    return decoded_text

def encoded_bits_to_bytes(encoded_text):
    # Pad encoded_text to make its length a multiple of 8
    padding = 0
    while len(encoded_text) % 8 != 0:
        encoded_text += '0'  # padding with zeros
        padding += 1
    print(f"Added {padding} bits of padding")

    byte_array = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i+8]
        byte_array.append(int(byte, 2))
    return bytes(byte_array), padding

def compress_to_file(text, codebook, filename):
    encoded_text = encode(text, codebook)
    byte_data, padding = encoded_bits_to_bytes(encoded_text)
    
    with open(filename, 'wb') as f:
        # Save the codebook and padding info using pickle
        pickle.dump((codebook, padding), f)
        # Write the byte data
        f.write(byte_data)
    print(f"Compressed data written to {filename}")

def bytes_to_encoded_bits(byte_data):
    encoded_bits = ""
    for byte in byte_data:
        bits = bin(byte)[2:]
        while len(bits)<8: # get 8-bit binary representation
            bits = '0' + bits
        encoded_bits += bits
    return encoded_bits

def decompress_from_file(filename):
    with open(filename, 'rb') as f:
        codebook, padding = pickle.load(f)
        byte_data = f.read()
    
    encoded_bits = bytes_to_encoded_bits(byte_data)
    if padding > 0:
        encoded_bits = encoded_bits[:-padding]  # remove padding bits
    # Reconstruct the Huffman tree from the codebook
    root = Node()
    for symbol, code in codebook.items():
        current = root
        for bit in code:
            if bit == '0':
                if current.left is None:
                    current.left = Node()
                current = current.left
            else:  # bit == '1'
                if current.right is None:
                    current.right = Node()
                current = current.right
        current.symbol = symbol
    
    decoded_text = decode(encoded_bits, root)
    return decoded_text

def saved_symbol_bits():
    for symbol in freqs:
        original_bits = freqs[symbol] * 8  # assuming 8 bits per character
        compressed_bits = freqs[symbol] * len(codebook[symbol])
        print(f"Symbol: {symbol}, Original bits: {original_bits}, Compressed bits: {compressed_bits}")

def avg_bits_per_symbol(freqs, codebook):
    avg_bits_per_symbol = 0
    for symbol in freqs:
        avg_bits_per_symbol += (freqs[symbol]/total) * len(codebook[symbol])
    return avg_bits_per_symbol

class Node:
    def __init__(self, freq=0, symbol=None, left=None, right=None):
        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right

    def __repr__(self): # like a 2nd name
        return f"Node(freq={self.freq}, symbol={self.symbol})"
    
    def __lt__(self, other): # for comparing
        return self.freq < other.freq

import math
from collections import Counter
import heapq
import pickle
import os

og_file = input("Enter the name of the input text file (with .txt extension): ")

print(f"Reading from {og_file}")

with open(og_file, 'r') as f:
    text = f.read()
freqs = create_freqs(text) #freqs is a dictionary with characters as keys and their frequencies as values
total = find_total(freqs)
probs = find_probs(freqs, total)
entropy = measure_entropy(probs)

print("Entropy:", entropy)

heap = []
nodes = []

push_nodes(freqs, heap, nodes)
#print("Heap:", heap)
#print("Nodes: ", nodes)
root=find_root(heap, nodes)
#print("Heap:", heap)
#print("Nodes: ", nodes)
    #print("Root: ", root)

codebook = make_codes(root)
    #print("Codebook: ", codebook)

#encoded_text = encode(text, codebook)
#print("Encoded: ", encoded_text)

#decoded_text = decode(encoded_text, root)
#print("Decoded: ", decoded_text)

#saved_symbol_bits()

avg_bits_per_symbol = avg_bits_per_symbol(freqs, codebook)
print("Average bits per symbol:", avg_bits_per_symbol)

#print("Check bound: Entropy =", entropy, "≤ average codeword length =", avg_bits_per_symbol, "< entropy+1 =", entropy+1)
print("Check bound: H =", entropy, "≤ L =", avg_bits_per_symbol, "< H+1 =", entropy+1)

compress_to_file(text, codebook, 'compressed.huff')
decompressed_text = decompress_from_file('compressed.huff')
with open('decompressed.txt', 'w') as f:
    f.write(decompressed_text)

original_size = os.path.getsize('input.txt')

compressed_size = os.path.getsize('compressed.huff')
print(f"Original size: {original_size} bytes")
print(f"Compressed size: {compressed_size} bytes")
compression_ratio = compressed_size / original_size
print(f"Compression ratio: {compression_ratio}")

if text == decompressed_text:
    print("Decompression successful, texts match.")
else:
    print("Decompression failed, texts do not match.")
