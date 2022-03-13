import random
countries = ['Uruguay','Russia','Saudi Arabia','Egypt','Spain','Portugal', 'Iran','Morocco', 'France','Denmark','Peru', 'Australia', 'Croatia','Argentina', 'Nigeria', 'Iceland','Brazil',\
             'Switzerland', 'Serbia', 'Costa Rica','Sweden','Mexico', 'Korea Republic', 'Germany', 'Belgium','England', 'Tunisia', 'Panama','Colombia','Japan', 'Senegal', 'Poland']
random.shuffle(countries)
print(countries)

#def create_list_with_one_random_country() -> list[str]:
    #return
A = [countries[random.randint(0,len(countries)-1)]]
B = [countries[random.randint(0,len(countries)-1)]]
C = [countries[random.randint(0,len(countries)-1)]]
D = [countries[random.randint(0,len(countries)-1)]]
E = [countries[random.randint(0,len(countries)-1)]]
F = [countries[random.randint(0,len(countries)-1)]]
G = [countries[random.randint(0,len(countries)-1)]]
H = [countries[random.randint(0,len(countries)-1)]]

print('''\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}'''.format(A,B,C,D,E,F,G,H))