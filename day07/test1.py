from dataclasses import dataclass

print('hello world')

@dataclass
class Data:
    valeur: int
    nombres: [int]
    # def __init__(self, valeur, nombres):
    #     self.valeur = valeur
    #     self.nombres = nombres

def lecture(fichier)-> [Data]:
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

liste1=lecture('test1.txt')
print(liste1)