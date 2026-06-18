def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

def test_linear_search():
    arr = [1, 2, 3, 4, 5]
    target = 3
    assert linear_search(arr, target) == 2
