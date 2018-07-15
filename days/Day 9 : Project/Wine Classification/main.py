# import necessary libraries
import pandas as pd
import sys

class wineclassification:
    def wineselect(self,name=None):
        self.name = name
        if self.name == 'redwine':
            self.data = pd.read_csv("winequality-red.csv",sep=';')
        elif self.name == 'whitewine':
            self.data = pd.read_csv("winequality-white.csv",sep=';')
        else:
            print("Not found")
            sys.exit()

    def pred(self,fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density, pH, suplhates, alcohol):
        self.X = self.data.iloc[:,:-1]
        self.y = self.data.iloc[:,-1:]
        from sklearn.ensemble import RandomForestClassifier
        classifier = RandomForestClassifier(n_estimators=len(self.X)//2,criterion='gini', n_jobs=-1)
        classifier.fit(self.X, self.y.values.ravel())
        self.quality = classifier.predict([[fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density, pH, suplhates, alcohol]])
        print("\n\nThe quality for {} is {}".format(self.name,self.quality[0]))


wine = wineclassification()
typewine = input("Redwine or whitewine\n")
typewine = typewine.lower()
wine.wineselect(typewine)

fixed_acidity = float(input("Enter the value for fixed_acidity :-\n"))
volatile_acidity = float(input("Enter the value for volatile_acidity :-\n"))
citric_acid = float(input("Enter the value for citric_acid :-\n"))
residual_sugar = float(input("Enter the value for residual_sugar :-\n"))
chlorides = float(input("Enter the value for chlorides :-\n"))
free_sulfur_dioxide  = float(input("Enter the value for free_sulfur_dioxide :-\n"))
total_sulfur_dioxide = float(input("Enter the value for total_sulfur_dioxide :-\n"))
density = float(input("Enter the value for density :-\n"))
pH = float(input("Enter the value for pH :-\n"))
suplhates = float(input("Enter the value for suplhates :-\n"))
alcohol = float(input("Enter the value for alcohol :-\n"))

wine.pred(fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density, pH, suplhates, alcohol)
