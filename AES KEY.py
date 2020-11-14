import binascii
import hashlib
import base64
from Crypto.Cipher import AES



#计算丢失的字符,使？可见



def visible():
    a = [1, 1, 1, 1, 1, 6]
    b = [7, 3, 1, 7, 3, 1]
    c = 0
    for i in range(0,6):
        c = c + a[i]*b[i]
    remainder = c% 10
    remainder = str(remainder)
    return(remainder)

MRZ = '12345678<81110182111116'+visible()
str = '12345678<8<<<1110182<111116'+visible()+'<<<<<<<<<<<<<<4'
print('The full str:',str)


def seed(MRZ):

    sha1_MRZ = hashlib.sha1(MRZ.encode('utf-8')).hexdigest()
    #print(sha1_MRZ)
    K_seed = sha1_MRZ[0:32]
    print('K_seed is:', K_seed)
    return(K_seed)

seed=seed(MRZ)
C = '00000001'
outcome = seed+C
c = binascii.a2b_hex(outcome) #转换成ASCii编码的字符串
keydata = hashlib.sha1(c).hexdigest()
print('output keydata:', keydata)

#生成KA,KB

K_A = keydata[0:16]
K_B = keydata[16:32]
#奇偶校验位的判断
def parity_check(x):
    k = []
    a = bin(int(x,16))[2:]
    for i in range(0,len(a),8):
        if (a[i:i+7].count("1"))%2 == 0:#1的个数为偶数，添加1
            k.append(a[i:i+7])
            k.append('1')
        else :
            k.append(a[i:i+7])#1的个数为奇数
            k.append('0')
    a1 = hex(int(''.join(k),2))
    print('parity check:'+ x + "-->" +a1)
    return a1[2:]
k_1 = parity_check(K_A)
k_2 = parity_check(K_B)
key = k_1 + k_2
print('key=',key)
#ea8645d97ff725a898942aa280c43179
s='9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9J\
xaa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI'
cipher = base64.b64decode(s.encode('utf-8'))
m = AES.new(binascii.unhexlify(key),AES.MODE_CBC,binascii.unhexlify('00000000000000000000000000000000'.encode()))
print('the base64-decoded message is:',cipher)
print('the plaintext is :',m.decrypt(cipher))





