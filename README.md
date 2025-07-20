![standard (1)](https://github.com/user-attachments/assets/63307f3d-b158-4a7c-a11f-9e97b8318c98)

# Python Code Obfuscator

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-red)

A simple Python code obfuscator tool that transforms your readable Python code into a protected version while maintaining original functionality.


## Obfuscation Examples

### Non-Obfuscated Code
print("Hello World!")

### Obfuscated output
import marshal, zlib, base64
exec(marshal.loads(zlib.decompress(base64.b64decode("eJx7zIAEWKH0ZycgMZUhmCGY0ZuhCEIzFjHKMcgxBDMFM1tFMDAkMjIAeTFMSgwxzEoMwSymjBCtMFqBIZ1Rk/UliOn3UhRIvrQAElW58fGZuQX5RSXx8RrqVTmZSeqaeimpyfm5BUWpxcUayLJJicWpZiZA+SQzE5CSlFQN9VSvqqpgX2OvyrBkz6pKfe/gMFdXR6cKLycXE1t1TYhRIHWlJWm6FkABlltsEGNusYAsu8VaUJSZV3KLJbUsMWclw2eQ625x2BSXAEXT7YCs3PyU0pxUuyIeoATII8WaQOIDMyMj420G3tsM3DcYBEGImbVDqNniBgvHTQbWxpQL3FWX2aqvMtQUcQFVAwBKWFWj"))))

##Installation
1. Install the file
2. run setup.py

## Usage
python obfuscator.py your_file.py

