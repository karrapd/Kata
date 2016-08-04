def numbers_gen(n):
    while True:
        n+=1
        yield n

def cumulative_triangle(n):
    sum=0
    p=((n-1)*(n))/2
    f=numbers_gen(p)
    for i in range(0,n):
        sum+=f.next()
    return sum