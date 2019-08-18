#compute max sums of subsets of the input array "arr"
#for now, assume everything is >= 0 in arr
#input: an array arr of non-negative integers
#output: an array A of length N = len(arr) where A[n] = maximum sum of
#subset of arr of size n.
def subset_sum(arr):
    N = len(arr)
    temp_max, ind = get_max(arr)
    max_sums = [temp_max]
    temp_arr =  remove_entry(arr, ind)
    count = 0
    while len(temp_arr) != 0:
        temp_max, ind = get_max(temp_arr)
        max_sums.append(max_sums[count] + temp_max)
        count += 1
        temp_arr = remove_entry(temp_arr, ind)
    return max_sums
    


def get_max(arr):
    max_val = -1
    ind = -1
    for i in range(len(arr)):
        if arr[i] >= max_val:
            max_val = arr[i]
            ind = i
    return [max_val, ind]

def remove_entry(arr, ind):
    temp_arr = []
    for i in range(len(arr)):
        if i != ind:
            temp_arr.append(arr[i])
    return temp_arr

A = [10, 2, 1, 15, 2, 0, 20]
M = subset_sum(A)
print(M)
