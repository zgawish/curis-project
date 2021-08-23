import random

nums = [0, 1]
code = str(random.choices(nums, weights=(30, 70), k=1)[0])
print(code+ "\n")
exit(code)