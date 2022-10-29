# For value of d * a mod n, will return d
def extendedEuclidean(a, n):
    a = a
    n = n
    q = 0
    u = 1
    v = 0 
    print("a\tn\tq\tu\tv")
    while (n != 1):
        print(a, "\t", n,"\t", q,"\t", u,"\t", v)
        n1 = a - (n * q)
        a = n
        n = n1
        v1 = u - (v * q)
        u = v
        v = v1
        q = int(a / n)
    print(a, "\t", n,"\t", q,"\t", u,"\t", v)
    return v

extendedEuclidean(73, 42*46)

#For equation like Y^X mod N
def squareAndMultiply(Y, X, N):
    X = bin(X)[2:]
    N = N
    Y = Y
    C = 1
    for i in range(len(X)):
        if i == 0:
            C = Y
        elif X[i] == '1':
            C = ((C * C) * Y) % N
        elif X[i] == '0':
            C = (C * C) % N
    return C
squareAndMultiply(1249, 71, 1517)