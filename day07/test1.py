from dataclasses import dataclass
from itertools import product

@dataclass
class Data:
    valeur: int
    nombres: list[int]


@dataclass
class Resultat:
    valeur: int
    nombres: list[int]
    operateurs: list[str]


def lecture(fichier) -> list[Data]:
    res = []
    with open(fichier, 'r') as file:
        # Read each line in the file
        for line in file:
            # Print each line
            s = line.strip()
            t = s.split(':')
            t2 = t[1].split()
            tab = []
            for x in t2:
                tab.append(int(x))
            d = Data(int(t[0]), tab)
            # print(line.strip())
            # print(d)
            res.append(d)

    return res


def cherche_operateurs(data: Data) -> Resultat | None:
    liste_operateurs = ['+', '*']

    longueur = len(data.nombres) - 1
    combinaisons = [''.join(p) for p in product(liste_operateurs, repeat=longueur)]

    for combinaison in combinaisons:
        valeur = 0
        for i in range(len(data.nombres)):
            if i == 0:
                valeur = data.nombres[i]
            else:
                op2 = combinaison[i - 1]
                v = data.nombres[i]
                if op2 == '+':
                    valeur = valeur + v
                elif op2 == '*':
                    valeur = valeur * v
        if valeur == data.valeur:
            return Resultat(valeur, data.nombres, combinaison.split())

    return None

def parcourt(data: Data, liste_operateurs: list[str],no:int,val:int, operateurs_selectionnee:list[str]) -> Resultat | None:

    if no<0:
        raise IndexError("no="+str(no))
    elif no>=len(data.nombres):
        raise IndexError("no="+str(no)+",len(data.nombres)="+str(len(data.nombres)))
    res=-1
    if no == 0:
        v=data.nombres[no]
        return parcourt(data, liste_operateurs, no+1, v,[])
    else:
        for operateur in liste_operateurs:
            if operateur == '+':
                v2=val+data.nombres[no]
            elif operateur == '*':
                v2=val*data.nombres[no]
            else:
                raise Exception("Erreur")
            if no>=len(data.nombres)-1:
                if v2 == data.valeur:
                    liste2=operateurs_selectionnee.copy()
                    liste2.append(operateur)
                    return Resultat(data.valeur, data.nombres, liste2)
            else:
                liste2=operateurs_selectionnee.copy()
                liste2.append(operateur)
                res2=parcourt(data, liste_operateurs, no+1, v2, liste2)
                if res2 is not None:
                    return res2
    return None

def cherche_operateurs2(data: Data) -> Resultat | None:
    liste_operateurs = ['+', '*']

    return parcourt(data,liste_operateurs,0,0,[])

def cherche_operateurs_choix(data: Data, no: int) -> Resultat | None:
    if no == 0:
        return cherche_operateurs(data)
    elif no == 1:
        return cherche_operateurs2(data)
    else:
        raise Exception("Erreur")

def recherche(no:int):

    liste1 = lecture('test1.txt')
    print(liste1)

    for x in liste1:
        op = cherche_operateurs_choix(x, no)
        if op is not None:
            print('trouve:', x, op)
        else:
            print('non trouve:', x)

no=0
no=1

recherche(no)

