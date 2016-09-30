def smallest(n):

    result = [n, 0, 0]

    for x in range(len(str(n))):
        backup_list = list(str(n))
        temp = backup_list.pop(x)
        for y in range(len(str(n))):
            backup_list.insert(y,temp)
            test = int(''.join(map(str, backup_list)))
            if test < result[0]:
                result = [test, x, y]
            backup_list.pop(y)
    return result
