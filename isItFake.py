import pandas as pd

data_clean = pd.read_pickle('data_clean.pkl')
data = pd.read_pickle('corpus.pkl')


print("Want fact do you want to verify?")
fact= input()
fact=fact.lower()

def isItFake(fact):
    fakefacts= data_clean[data_clean['fakenews'].str.contains(fact)]

    if fakefacts.empty is True:
        print('No already verified fake news contains the mentioned fact!')
        return 0
    else:
        print("The following fake news contains the mentioned fact! Be aware!")
        print(fakefacts)
        return fakefacts

a=isItFake(fact)
print(a)