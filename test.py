import math
counter = 0
date = 11242022
for i in range(2022,3022):
    
    if i % 400 == 0: 
        date -= 20000
    elif i % 100== 0:
        date -= 10000
    elif i % 4 == 0:
        date -= 20000
    else:
        date -= 10000

    if date < 11222022:
        date += 70000
    date += 1
    is_prime = True
    for x in range(2,int(math.sqrt(date))):
        if date % x == 0:
            is_prime = False
            break
    if is_prime:
        counter+=1
    

print(counter)

    

            
