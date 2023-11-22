#Determine if a given integer is prime. return "Not prime" if the number is
#composite, and return "Prime" if the number is prime.
def isPrime(n):
    #flag will be set to -1 if n is composite
    if n == 1:
        print("Not prime")
    else:
        flag = 1
        for i in range(2,int((3/2)*n**(1/2))):
            if  n%i == 0:
                print("Not Prime")
                flag = -1
                break
        if flag == 1:
            print("Prime")

#N is the numer of queries
N = int(input().strip())
#ns will hold the N numbers 
ns = []
#get and store the N numbers in ns
for i in range(N):
    ns.append(int(input().strip()))

#check if each n in ns is prime.
for n in ns:
    isPrime(n)
