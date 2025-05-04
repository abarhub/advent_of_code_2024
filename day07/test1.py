from dataclasses import dataclass
from itertools import product

print('hello world')

@dataclass
class Data:
    valeur: int
    nombres: list[int]
    # def __init__(self, valeur, nombres):
    #     self.valeur = valeur
    #     self.nombres = nombres


@dataclass
class Resultat:
    valeur: int
    nombres: list[int]
    operateurs: list[str]


def lecture(fichier)-> list[Data]:
    res=[]
    with open(fichier, 'r') as file:
        # Read each line in the file
        for line in file:
            # Print each line
            s=line.strip()
            t=s.split(':')
            t2=t[1].split()
            tab=[]
            for x in t2:
                tab.append(int(x))
            d=Data(int(t[0]),tab)
            #print(line.strip())
            #print(d)
            res.append(d)

    return res

def cherche_operateurs(data:Data)->Resultat|None:

    liste_operateurs=['+','*']

    longueur = len(data.nombres)-1
    combinaisons = [''.join(p) for p in product(liste_operateurs, repeat=longueur)]

    for combinaison in combinaisons:
        valeur = 0
        for i in range(len(data.nombres)):
            if i==0:
                valeur=data.nombres[i]
            else:
                op2=combinaison[i-1]
                v=data.nombres[i]
                if op2=='+':
                    valeur=valeur+v
                elif op2=='*':
                    valeur=valeur*v
        if valeur==data.valeur:
            return Resultat(valeur,data.nombres,combinaison.split())

    return None


liste1=lecture('test1.txt')
print(liste1)

for x in liste1:
    op=cherche_operateurs(x)
    if op is not None:
        print('trouve:',x,op)
    else:
        print('non trouve:',x)
