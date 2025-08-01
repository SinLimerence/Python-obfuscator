![standard (1)](https://github.com/user-attachments/assets/63307f3d-b158-4a7c-a11f-9e97b8318c98)

# Python Code Obfuscator

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-red)

A simple Python code obfuscator tool that transforms your readable Python code into a protected version while maintaining original functionality. 


## Obfuscation Examples

### Non-Obfuscated Code 
```  
print("Hello World!") 
``` 
### Obfuscated output 
```   
import base64, zlib, marshal
#N\X\w=f(msRF?5&LNWz8
i4:~+=GY?JzwOfnl2VE/ 
def _d(s):
    return marshal.loads(zlib.decompress(base64.b64decode(s)))
#G
'd>54l04*NYWv_
exec(_d('eJx7zIAEmKH0ZxUgMZ0hhSGFMYchCkIzRjEyMaQypTCtZoQoYmSoZNRkfgli+lXxeKTm5OQrhOcX5aQoajLfYktKLE41M7nFUpWTmXSLtaAoM69kJcNnkOJfHDbFJUB+uh2QlZufUpqTalfECTaQgaFYGEh8YGZkZLzNwHubgfsmA2tD3lUG0SJ2oDgAhignIw=='))
#G#+Dxg^6!#yxP 1cN{D+I,&K\	D?p|

#LoV;Z46,Sg*<2(OhY{=-^L!k#Qa{]a
```
## Installation
1. Install the file
2. run setup.py

## Usage
python obfuscator.py your_file.py

