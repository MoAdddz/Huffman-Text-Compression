# Huffman-Text-Compression
Lossless text compression using Huffman coding in Python.

---

## Features
- Computes **character frequencies** and **entropy**.
- Builds a **Huffman tree** and generates **prefix-free codes**.
- Encodes and decodes text files with **100% accuracy**.
- Measures **compression ratio** and **average bits per symbol**.
- Modular and reusable code for analysis and file I/O.

---
Example usage:
- Enter a text file name in the same repositary as the program with edcoding utf-8 when prompted
- The program will save the encoded text to compressed.huff
- The program will decode the encoded text and save it to decompressed.txt
- The program will display entropy, average bits used per symbol, compressed size of file and compression ratio to see how close to the entropy (theoretical limit) the program got to

### Compress a text file
```bash
python huffman.py compress Macbeth.txt compressed.huff
