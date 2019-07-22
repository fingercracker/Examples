import math

def merge(A, p, l, r):
    n1 = l-p
    n2 = r-l
    L = [A[i] for i in range(l)]
    R = [A[i] for i in range(l, r)]
    temp = []
    i = 0
    j = 0
    k = 0
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            A[k] = L[i]
            i += 1
            k += 1
        else:
            A[k] = R[j]
            j += 1
            k += 1
    while i < n1:
        A[k] = L[i]
        i+=1
        k+=1 
    while j < n2:
        A[k] = R[j]
        j+=1
        k+=1
    print(A)

def mergesort(A, p, r):
    if p < r:
        l = int((p+r)/2)
        mergesort(A, p, l)
        mergesort(A, l+1, r)
        merge(A, p, l, r)

A = [15, 2, 1, 3, 4, 10, 4]
mergesort(A, 0, len(A))
print(A)



    
