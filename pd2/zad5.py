import random
colors = ['trefl','karo','kier','pik']
figures = ['As','król','królowa','joker','10','9']
all_cards = []

for color in colors:
    for figure in figures:
        all_cards.append('{} {}'.format(figure, color))
random.shuffle(all_cards)

player_1 = []
player_2 = []
all_cards_copy = all_cards.copy()
card = ''
mes = 'Player_{}: {}\n'

for i in range(10):
    card = all_cards_copy.pop(random.randint(0,len(all_cards_copy)-1))
    if i < 5:
        player_1.append(card)
    else:
        player_2.append(card)
print(mes.format(1,player_1) + mes.format(2,player_2))

my_list = []
card_strength = {'As':14,'król':13,'królowa':12,'joker':11,'10':10,'9':9}

def my_sort(e):
    return card_strength.get(e.split()[0]) , e.split()[1]

all_cards.sort(key= my_sort)

print(all_cards)

player_1.clear()
player_2.clear()
all_cards_copy = all_cards.copy()

for i in range(len(all_cards_copy)):
    card = all_cards_copy.pop(random.randint(0, len(all_cards_copy) - 1))
    if i < len(all_cards)/2:
        player_1.append(card)
    else:
        player_2.append(card)

print('\n' + mes.format(1, player_1) + mes.format(2, player_2))

card_1 = ''
card_2 = ''
message = 'Winner is {}'

while len(player_1) != 0 and len(player_2) != 0:
    card_1 = player_1.pop()
    card_2 = player_2.pop()
    card_1_strength = card_strength.get(card_1.split()[0])
    card_2_strength = card_strength.get(card_2.split()[0])
    if card_1_strength == card_2_strength:
        player_1.insert(0,card_1)
        player_2.insert(0,card_2)
    elif card_1_strength > card_2_strength:
        player_1.insert(0,card_1)
        player_1.insert(0,card_2)
    else:
        player_2.insert(0,card_1)
        player_2.insert(0,card_2)

if len(player_1) == 0:
    print(message.format('Player_2'))
else:
    print(message.format('Player_1'))
