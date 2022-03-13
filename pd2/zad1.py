import math

my_format = '''{0:16f}{1:16f}\n{2:16f}{3:16f}\n{4:16f}{5:16f}\n'''
full_circle = math.degrees(math.pi*2)
print(my_format.format(full_circle*math.pi/180, math.radians(full_circle), full_circle/4*math.pi/180, math.radians(full_circle/4), full_circle/8*math.pi/180,\
                       math.radians(full_circle/8)))