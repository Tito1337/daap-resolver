#!/usr/bin/python
"""
 Copyright 2011 kenkeiras <kenkeiras@gmail.com>
 Bajo la licencia WTFPL

             DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO. 
"""
import struct

#Pasa un entero de 4 bytes a un array de 4 bytes
def uint4tochar(s):
    i=0
    t=[0,0,0,0]

    while i<4:
        aux=(s>>(8*i))&0xFF

        t[3-i]=int(aux)
        i+=1

    return t

#Devuelve un hexadecimal con 4 caracteres o mas
def myhex(a):
    r=hex(a)

    if (len(r)==3):
        r="0x0"+r[2]

    return r
#Funciones basicas
def F(x,y,z): # XY o no(X)Z
    return (x&y)|((~x&0xFFFFFFFF)&z)

def G(x,y,z): # XZ o no(Z)Y
    return (x&z)|(y&(~z&0xFFFFFFFF))

def H(x,y,z): # X xor Y xor Z
    return x^y^z

def I(x,y,z): # Y xor (X o no(Z))
    return y^(x|(~z&0xFFFFFFFF))

# Rotacion
def rotate_left(x,y):
    return ((x<<y)|(x>>(32-y)))


#Transformaciones
def FF(a, b, c, d, x, s, ac):

    a = (a + (F(b, c, d) + x + ac)) & 0xFFFFFFFF

    a = rotate_left(a, s) & 0xFFFFFFFF
    a = (a + b) & 0xFFFFFFFF

    return a

def GG(a, b, c, d, x, s, ac):

    a = (a + (G(b, c, d) + x + ac)) & 0xFFFFFFFF

    a = rotate_left(a, s) & 0xFFFFFFFF
    a = (a + b) & 0xFFFFFFFF

    return a

def HH(a, b, c, d, x, s, ac):

    a = (a + (H(b, c, d) + x + ac)) & 0xFFFFFFFF

    a = rotate_left(a, s) & 0xFFFFFFFF
    a = (a + b) & 0xFFFFFFFF

    return a

def II(a, b, c, d, x, s, ac):

    a = (a + (I(b, c, d) + x + ac)) & 0xFFFFFFFF

    a = rotate_left(a, s) & 0xFFFFFFFF
    a = (a + b) & 0xFFFFFFFF

    return a

#Tabla de valores utilizados en la funcion
S11 =  7
S12 = 12
S13 = 17
S14 = 22

S21 =  5
S22 =  9
S23 = 14
S24 = 20

S31 =  4
S32 = 11
S33 = 16
S34 = 23

S41 =  6
S42 = 10
S43 = 15
S44 = 21


class md5daap:

    #Paso 1, se anhade un bit '1' al mensaje
    # Y despues se hace que sea igual a 448, modulo 512 (ambos en bits)
    # ,que se traducen en 56 y 64 bytes respectivamente
    def padd(self,s):
        self.stream=s+"\x80"
        while ((len(self.stream)%64)!=56):
            self.stream+="\x00"


    #Paso 2, se anhade al mensaje el numero (de 64 bits-8 bytes)
    # de bits antes de la primera adicion
    def attach_len(self,ln):
        ln%=1<<64
        self.stream += struct.pack("q", ln)     

    #Paso 3, se inicializa un bufer
    def buff_init(self):
        self.a = 0x67452301
        self.b = 0xefcdab89
        self.c = 0x98badcfe
        self.d = 0x10325476


    # Paso 4, se procesa el objeto    
    def transform(self,x):

        AA = self.a
        BB = self.b
        CC = self.c
        DD = self.d

        #Ronda 1
        AA = FF(AA, BB, CC, DD, x[ 0], S11, 0xd76aa478) # 1
        DD = FF(DD, AA, BB, CC, x[ 1], S12, 0xe8c7b756) # 2
        CC = FF(CC, DD, AA, BB, x[ 2], S13, 0x242070db) # 3
        BB = FF(BB, CC, DD, AA, x[ 3], S14, 0xc1bdceee) # 4

        AA = FF(AA, BB, CC, DD, x[ 4], S11, 0xf57c0faf) # 5
        DD = FF(DD, AA, BB, CC, x[ 5], S12, 0x4787c62a) # 6
        CC = FF(CC, DD, AA, BB, x[ 6], S13, 0xa8304613) # 7
        BB = FF(BB, CC, DD, AA, x[ 7], S14, 0xfd469501) # 8

        AA = FF(AA, BB, CC, DD, x[ 8], S11, 0x698098d8) # 9
        DD = FF(DD, AA, BB, CC, x[ 9], S12, 0x8b44f7af) # 10
        CC = FF(CC, DD, AA, BB, x[10], S13, 0xffff5bb1) # 11
        BB = FF(BB, CC, DD, AA, x[11], S14, 0x895cd7be) # 12

 
        AA = FF(AA, BB, CC, DD, x[12], S11, 0x6b901122) # 13
        DD = FF(DD, AA, BB, CC, x[13], S12, 0xfd987193) # 14
        CC = FF(CC, DD, AA, BB, x[14], S13, 0xa679438e) # 15
        BB = FF(BB, CC, DD, AA, x[15], S14, 0x49b40821) # 16

        # Round 2
        AA = GG(AA, BB, CC, DD, x[ 1], S21, 0xf61e2562) # 17
        DD = GG(DD, AA, BB, CC, x[ 6], S22, 0xc040b340) # 18
        CC = GG(CC, DD, AA, BB, x[11], S23, 0x265e5a51) # 19
        BB = GG(BB, CC, DD, AA, x[ 0], S24, 0xe9b6c7aa) # 20

        AA = GG(AA, BB, CC, DD, x[ 5], S21, 0xd62f105d) # 21
        DD = GG(DD, AA, BB, CC, x[10], S22, 0x2441453 ) # 22
        CC = GG(CC, DD, AA, BB, x[15], S23, 0xd8a1e681) # 23
        BB = GG(BB, CC, DD, AA, x[ 4], S24, 0xe7d3fbc8) # 24

        AA = GG(AA, BB, CC, DD, x[ 9], S21, 0x21e1cde6) # 25
        DD = GG(DD, AA, BB, CC, x[14], S22, 0xc33707d6) # 26
        CC = GG(CC, DD, AA, BB, x[ 3], S23, 0xf4d50d87) # 27
        # BB = GG(BB, CC, DD, AA, x[ 8], S24, 0x455a14ed) # 28  # REAL MD5
        BB = GG(BB, CC, DD, AA, x[ 8], S24, 0x445a14ed) # 28    # APPLE MD5

        AA = GG(AA, BB, CC, DD, x[13], S21, 0xa9e3e905) # 29
        DD = GG(DD, AA, BB, CC, x[ 2], S22, 0xfcefa3f8) # 30
        CC = GG(CC, DD, AA, BB, x[ 7], S23, 0x676f02d9) # 31
        BB = GG(BB, CC, DD, AA, x[12], S24, 0x8d2a4c8a) # 32


        # Round 3
        AA = HH(AA, BB, CC, DD, x[ 5], S31, 0xfffa3942) # 33
        DD = HH(DD, AA, BB, CC, x[ 8], S32, 0x8771f681) # 34
        CC = HH(CC, DD, AA, BB, x[11], S33, 0x6d9d6122) # 35
        BB = HH(BB, CC, DD, AA, x[14], S34, 0xfde5380c) # 36

        
        AA = HH(AA, BB, CC, DD, x[ 1], S31, 0xa4beea44) # 37
        DD = HH(DD, AA, BB, CC, x[ 4], S32, 0x4bdecfa9) # 38
        CC = HH(CC, DD, AA, BB, x[ 7], S33, 0xf6bb4b60) # 39
        BB = HH(BB, CC, DD, AA, x[10], S34, 0xbebfbc70) # 40

        AA = HH(AA, BB, CC, DD, x[13], S31, 0x289b7ec6) # 41
        DD = HH(DD, AA, BB, CC, x[ 0], S32, 0xeaa127fa) # 42
        CC = HH(CC, DD, AA, BB, x[ 3], S33, 0xd4ef3085) # 43
        BB = HH(BB, CC, DD, AA, x[ 6], S34, 0x4881d05 ) # 44

        AA = HH(AA, BB, CC, DD, x[ 9], S31, 0xd9d4d039) # 45
        DD = HH(DD, AA, BB, CC, x[12], S32, 0xe6db99e5) # 46
        CC = HH(CC, DD, AA, BB, x[15], S33, 0x1fa27cf8) # 47
        BB = HH(BB, CC, DD, AA, x[ 2], S34, 0xc4ac5665) # 48


        # Round 4
        AA = II(AA, BB, CC, DD, x[ 0], S41, 0xf4292244) # 49
        DD = II(DD, AA, BB, CC, x[ 7], S42, 0x432aff97) # 50
        CC = II(CC, DD, AA, BB, x[14], S43, 0xab9423a7) # 51
        BB = II(BB, CC, DD, AA, x[ 5], S44, 0xfc93a039) # 52

        AA = II(AA, BB, CC, DD, x[12], S41, 0x655b59c3) # 53
        DD = II(DD, AA, BB, CC, x[ 3], S42, 0x8f0ccc92) # 54
        CC = II(CC, DD, AA, BB, x[10], S43, 0xffeff47d) # 55
        BB = II(BB, CC, DD, AA, x[ 1], S44, 0x85845dd1) # 56

        AA = II(AA, BB, CC, DD, x[ 8], S41, 0x6fa87e4f) # 57
        DD = II(DD, AA, BB, CC, x[15], S42, 0xfe2ce6e0) # 58
        CC = II(CC, DD, AA, BB, x[ 6], S43, 0xa3014314) # 59
        BB = II(BB, CC, DD, AA, x[13], S44, 0x4e0811a1) # 60

        AA = II(AA, BB, CC, DD, x[ 4], S41, 0xf7537e82) # 61
        DD = II(DD, AA, BB, CC, x[11], S42, 0xbd3af235) # 62
        CC = II(CC, DD, AA, BB, x[ 2], S43, 0x2ad7d2bb) # 63
        BB = II(BB, CC, DD, AA, x[ 9], S44, 0xeb86d391) # 64 

        self.a = (self.a + AA) & 0xFFFFFFFF
        self.b = (self.b + BB) & 0xFFFFFFFF
        self.c = (self.c + CC) & 0xFFFFFFFF
        self.d = (self.d + DD) & 0xFFFFFFFF

    def update(self):
        for i in xrange (len(self.stream) / 64):

            x=[]

            for j in xrange(16):

                t = ((ord(self.stream[(i*64)+(j*4)+0]))|
                  (ord(self.stream[(i*64)+(j*4)+1])<< 8)|
                  (ord(self.stream[(i*64)+(j*4)+2])<< 16)|
                  (ord(self.stream[(i*64)+(j*4)+3])<< 24))

                x.append(t)

            self.transform(x)


    # Paso 5, finalizacion y salida
    def final(self):

        self.digest=[]
        for buff in [self.a,self.b,self.c,self.d]:

            t = uint4tochar(buff)
            while len(t)>0:

                byte = t.pop()
                self.digest.append(myhex(byte)[2:4])

    def hexdigest(self):
        return ''.join(self.digest)
        
    # Punto de inicio 
    def __init__(self,s):
        ln=len(s)*8
        self.padd(s)
        self.attach_len(ln)
        self.buff_init()
        self.update()
        self.final()

if __name__=="__main__":
    import hashlib
    tests=["","1234","The quick brown fox jumps over the lazy dog","The quick brown fox jumps over the lazy dog.","qwertyuiopasdfghjklzxcvbnm,.+'-.,!\"$%&/()=?!~|@#{[]}"]
    for s in tests:
        chksum=md5daap(s)
        a=chksum.hexdigest()
        print a,'=',
        b=hashlib.md5(s).hexdigest()
        print b,a==b

