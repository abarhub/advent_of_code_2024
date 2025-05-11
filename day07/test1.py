from dataclasses import dataclass
from itertools import product
from timeit import timeit


@dataclass
class Data:
    valeur: int
    nombres: list[int]


@dataclass
class Resultat:
    valeur: int
    nombres: list[int]
    operateurs: list[str]

@dataclass
class NbOperations:
    nb: int
    nbFeuilles: int
    abandon: int

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


def cherche_operateurs(data: Data, nb_op: NbOperations) -> Resultat | None:
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
                    nb_op.nb+=1
                elif op2 == '*':
                    valeur = valeur * v
                    nb_op.nb+=1
        if valeur == data.valeur:
            nb_op.nbFeuilles+=1
            return Resultat(valeur, data.nombres, combinaison.split())

    return None

def parcourt(data: Data, liste_operateurs: list[str],no:int,val:int,
             operateurs_selectionnee:list[str], nb_op: NbOperations) -> Resultat | None:

    if no<0:
        raise IndexError("no="+str(no))
    elif no>=len(data.nombres):
        raise IndexError("no="+str(no)+",len(data.nombres)="+str(len(data.nombres)))
    res=-1
    if no == 0:
        v=data.nombres[no]
        return parcourt(data, liste_operateurs, no+1, v,[], nb_op)
    else:
        for operateur in liste_operateurs:
            if operateur == '+':
                v2=val+data.nombres[no]
                nb_op.nb+=1
            elif operateur == '*':
                v2=val*data.nombres[no]
                nb_op.nb+=1
            else:
                raise Exception("Erreur")
            if no>=len(data.nombres)-1:
                if v2 == data.valeur:
                    liste2=operateurs_selectionnee.copy()
                    liste2.append(operateur)
                    nb_op.nbFeuilles+=1
                    return Resultat(data.valeur, data.nombres, liste2)
            else:
                liste2=operateurs_selectionnee.copy()
                liste2.append(operateur)
                res2=parcourt(data, liste_operateurs, no+1, v2, liste2, nb_op)
                if res2 is not None:
                    return res2
    return None


def parcourt2(data: Data, liste_operateurs: list[str],no:int,val:int,
              operateurs_selectionnee:list[str], nb_op: NbOperations) -> Resultat | None:

    if no<0:
        raise IndexError("no="+str(no))
    elif no>=len(data.nombres):
        raise IndexError("no="+str(no)+",len(data.nombres)="+str(len(data.nombres)))
    res=-1
    if no == 0:
        v=data.nombres[no]
        return parcourt2(data, liste_operateurs, no+1, v,[],nb_op)
    else:
        for operateur in liste_operateurs:
            if operateur == '+':
                v2=val+data.nombres[no]
                nb_op.nb+=1
            elif operateur == '*':
                v2=val*data.nombres[no]
                nb_op.nb+=1
            else:
                raise Exception("Erreur")
            if v2>data.valeur:
                nb_op.abandon+=1
                continue
            if no>=len(data.nombres)-1:
                if v2 == data.valeur:
                    liste2=operateurs_selectionnee.copy()
                    liste2.append(operateur)
                    nb_op.nbFeuilles+=1
                    return Resultat(data.valeur, data.nombres, liste2)
            else:
                liste2=operateurs_selectionnee.copy()
                liste2.append(operateur)
                res2=parcourt2(data, liste_operateurs, no+1, v2, liste2, nb_op)
                if res2 is not None:
                    return res2
    return None

def cherche_operateurs2(data: Data, nb_op: NbOperations) -> Resultat | None:
    liste_operateurs = ['+', '*']

    return parcourt2(data, liste_operateurs, 0, 0, [], nb_op)

def parcourt3(data: Data, liste_operateurs: list[str],no:int,val:int,
              operateurs_selectionnee:list[str], nb_op: NbOperations, reste:int) -> Resultat | None:

    if no<0:
        raise IndexError("no="+str(no))
    elif no>=len(data.nombres):
        raise IndexError("no="+str(no)+",len(data.nombres)="+str(len(data.nombres)))
    res=-1
    if no == 0:
        v=data.nombres[no]
        total=0
        for n in data.nombres:
            total+=n
        if total>data.valeur:
            return None
        reste=total-v
        return parcourt3(data, liste_operateurs, no+1, v,[],nb_op, reste)
    else:
        for operateur in liste_operateurs:
            if operateur == '+':
                v2=val+data.nombres[no]
            elif operateur == '*':
                v2=val*data.nombres[no]
            else:
                raise Exception("Erreur")
            nb_op.nb+=1
            reste2 = reste-data.nombres[no]
            if v2>data.valeur:
                nb_op.abandon+=1
                continue
            elif v2+reste2>data.valeur:
                nb_op.abandon+=1
                continue
            if no>=len(data.nombres)-1:
                if v2 == data.valeur:
                    liste2=operateurs_selectionnee.copy()
                    liste2.append(operateur)
                    nb_op.nbFeuilles+=1
                    return Resultat(data.valeur, data.nombres, liste2)
            else:
                liste2=operateurs_selectionnee.copy()
                liste2.append(operateur)
                res2=parcourt3(data, liste_operateurs, no+1, v2, liste2, nb_op, reste2)
                if res2 is not None:
                    return res2
    return None

def cherche_operateurs3(data: Data, nb_op: NbOperations) -> Resultat | None:
    liste_operateurs = ['+', '*']

    return parcourt3(data, liste_operateurs, 0, 0, [], nb_op,0)

def cherche_operateurs_choix(data: Data, no: int, nb_op: NbOperations) -> Resultat | None:
    if no == 0:
        return cherche_operateurs(data,nb_op)
    elif no == 1:
        return cherche_operateurs2(data,nb_op)
    elif no == 2:
        return cherche_operateurs3(data, nb_op)
    else:
        raise Exception("Erreur")

def recherche(no:int):

    #liste1 = lecture('test1.txt')
    liste1 = lecture('input.txt')
    print(liste1)

    total=0
    nb=0
    nbOp=NbOperations(0,0,0)
    for x in liste1:
        op = cherche_operateurs_choix(x, no, nbOp)
        if op is not None:
            print('trouve:', x, op)
            nb+=1
            total+=x.valeur
        else:
            print('non trouve:', x)
    print('nb:', nb)
    print('total:', total)
    print('nb op:', nbOp)

if True:
    no=0
    no=1
    no = 2

    recherche(no)
else:
    no=0
    no = 1
    print(timeit(lambda :recherche(no),number=500))

