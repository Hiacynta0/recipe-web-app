import random

numbers = set()
while len(numbers) < 6:
    numbers.add(random.randint(1,49))
print('\nWinning numbers: {}'.format(numbers))