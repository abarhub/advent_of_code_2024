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

class Algo1:
    def __init__(self, data: Data, nb_op: NbOperations) -> None:
        self.data = data
        self.nb_op = nb_op

    def cherche_operateurs(self) -> Resultat | None:
        liste_operateurs = ['+', '*']

        longueur = len(self.data.nombres) - 1
        combinaisons = [''.join(p) for p in product(liste_operateurs, repeat=longueur)]

        for combinaison in combinaisons:
            valeur = 0
            for i in range(len(self.data.nombres)):
                if i == 0:
                    valeur = self.data.nombres[i]
                else:
                    op2 = combinaison[i - 1]
                    v = self.data.nombres[i]
                    if op2 == '+':
                        valeur = valeur + v
                        self.nb_op.nb+=1
                    elif op2 == '*':
                        valeur = valeur * v
                        self.nb_op.nb+=1
            if valeur == self.data.valeur:
                self.nb_op.nbFeuilles+=1
                return Resultat(valeur, self.data.nombres, combinaison.split())

        return None

class Algo2:

    def __init__(self, data: Data, nb_op: NbOperations) -> None:
        self.data = data
        self.nb_op = nb_op

    def parcourt(self, liste_operateurs: list[str],no:int,val:int,
                 operateurs_selectionnee:list[str]) -> Resultat | None:

        if no<0:
            raise IndexError("no="+str(no))
        elif no>=len(self.data.nombres):
            raise IndexError("no="+str(no)+",len(data.nombres)="+str(len(self.data.nombres)))
        res=-1
        if no == 0:
            v=self.data.nombres[no]
            return self.parcourt(liste_operateurs, no+1, v,[])
        else:
            for operateur in liste_operateurs:
                if operateur == '+':
                    v2=val+self.data.nombres[no]
                    self.nb_op.nb+=1
                elif operateur == '*':
                    v2=val*self.data.nombres[no]
                    self.nb_op.nb+=1
                else:
                    raise Exception("Erreur")
                if no>=len(self.data.nombres)-1:
                    if v2 == self.data.valeur:
                        liste2=operateurs_selectionnee.copy()
                        liste2.append(operateur)
                        self.nb_op.nbFeuilles+=1
                        return Resultat(self.data.valeur, self.data.nombres, liste2)
                else:
                    liste2=operateurs_selectionnee.copy()
                    liste2.append(operateur)
                    res2=self.parcourt(self.data, liste_operateurs, no+1, v2, liste2, self.nb_op)
                    if res2 is not None:
                        return res2
        return None

    def parcourt2(self, liste_operateurs: list[str],no:int,val:int,
                  operateurs_selectionnee:list[str]) -> Resultat | None:

        if no<0:
            raise IndexError("no="+str(no))
        elif no>=len(self.data.nombres):
            raise IndexError("no="+str(no)+",len(data.nombres)="+str(len(self.data.nombres)))
        if no == 0:
            v=self.data.nombres[no]
            return self.parcourt2(liste_operateurs, no+1, v,[])
        else:
            for operateur in liste_operateurs:
                if operateur == '+':
                    v2=val+self.data.nombres[no]
                    self.nb_op.nb+=1
                elif operateur == '*':
                    v2=val*self.data.nombres[no]
                    self.nb_op.nb+=1
                else:
                    raise Exception("Erreur")
                if v2>self.data.valeur:
                    self.nb_op.abandon+=1
                    continue
                if no>=len(self.data.nombres)-1:
                    if v2 == self.data.valeur:
                        liste2=operateurs_selectionnee.copy()
                        liste2.append(operateur)
                        self.nb_op.nbFeuilles+=1
                        return Resultat(self.data.valeur, self.data.nombres, liste2)
                else:
                    liste2=operateurs_selectionnee.copy()
                    liste2.append(operateur)
                    res2=self.parcourt2(liste_operateurs, no+1, v2, liste2)
                    if res2 is not None:
                        return res2
        return None

    def cherche_operateurs2(self) -> Resultat | None:
        liste_operateurs = ['+', '*']

        return self.parcourt2(liste_operateurs, 0, 0, [])


class Algo3:

    def __init__(self, data: Data, nb_op: NbOperations) -> None:
        self.data = data
        self.nb_op = nb_op

    def parcourt3(self, liste_operateurs: list[str],no:int,val:int,
                  operateurs_selectionnee:list[str], reste:int) -> Resultat | None:

        if no<0:
            raise IndexError("no="+str(no))
        elif no>=len(self.data.nombres):
            raise IndexError("no="+str(no)+",len(data.nombres)="+str(len(self.data.nombres)))
        res=-1
        if no == 0:
            v=self.data.nombres[no]
            total=0
            for n in self.data.nombres:
                total+=n
            if total>self.data.valeur:
                return None
            reste=total-v
            return self.parcourt3(liste_operateurs, no+1, v,[], reste)
        else:
            for operateur in liste_operateurs:
                if operateur == '+':
                    v2=val+self.data.nombres[no]
                elif operateur == '*':
                    v2=val*self.data.nombres[no]
                else:
                    raise Exception("Erreur")
                self.nb_op.nb+=1
                reste2 = reste-self.data.nombres[no]
                if v2>self.data.valeur:
                    self.nb_op.abandon+=1
                    continue
                elif v2+reste2>self.data.valeur:
                    self.nb_op.abandon+=1
                    continue
                if no>=len(self.data.nombres)-1:
                    if v2 == self.data.valeur:
                        liste2=operateurs_selectionnee.copy()
                        liste2.append(operateur)
                        self.nb_op.nbFeuilles+=1
                        return Resultat(self.data.valeur, self.data.nombres, liste2)
                else:
                    liste2=operateurs_selectionnee.copy()
                    liste2.append(operateur)
                    res2=self.parcourt3(liste_operateurs, no+1, v2, liste2, reste2)
                    if res2 is not None:
                        return res2
        return None

    def cherche_operateurs3(self) -> Resultat | None:
        liste_operateurs = ['+', '*']

        return self.parcourt3(liste_operateurs, 0, 0, [], 0)

def cherche_operateurs_choix(data: Data, no: int, nb_op: NbOperations) -> Resultat | None:
    if no == 0:
        return Algo1(data, nb_op).cherche_operateurs()
    elif no == 1:
        return Algo2(data, nb_op).cherche_operateurs2()
    elif no == 2:
        return Algo3(data, nb_op).cherche_operateurs3()
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
    #no=1
    #no = 2

    recherche(no)
else:
    no=0
    no = 1
    print(timeit(lambda :recherche(no),number=500))

