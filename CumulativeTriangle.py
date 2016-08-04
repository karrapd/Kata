def numbers_gen(n):
    while True:
        n += 1
        yield n

def cumulative_triangle(n):
    final_sum = 0
    start_number = ((n-1)*(n))/2
    numbers_list = numbers_gen(start_number)
    for i in range(n):
        final_sum + =numbers_list.next()
    return final_sum
