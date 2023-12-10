#/usr/bin/env python3

"""furniture = ['table' , 'chair', 'desck' , 'door' , 'window' ]

for ele in furniture:
    print(f'i bought a new {ele} today')"""

list_3 = ['Accidental', '4daa7fe9', 'eM131Me', 'Y!.90']
secret = []

for x in list_3:
    secret.append(x[:2])

print(''.join(secret))