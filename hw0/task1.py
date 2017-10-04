def twoSum(nums, target):
    """
    :type nums: List[int]
    :type target: int
    :return type: List[int]
    """
    checked = {}
    for i,num in enumerate(nums):
        if target - num in checked:
            return [checked[target - num], i]
        checked[num] = i

if __name__ == "__main__":
    nums = [2, 7, 11, 15]
    ans = twoSum(nums, 17)
    print ans
