import random

first_round = []
second_round = []
value = 0
sum_1 = 0
sum_2 = 0
message = 'Sum of {} round is greater: {}'

for i in range(8):
    value = random.randint(1,6)
    if i < 4:
        first_round.append(value)
        sum_1 += value
    else:
        second_round.append(value)
        sum_2 += value
print('\n{}\n{}'.format(first_round, second_round))

if sum_1 == sum_2: print('The sum is egual: {}'.format(sum_1))
elif sum_2 > sum_1: print(message.format('second',sum_2))
else: print(message.format('first',sum_1))