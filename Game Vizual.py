import pandas as pd
import numpy as np
import matplotlib.pyplot as pyplot
from matplotlib import style

data = pd.read_csv("export_dataframe.csv")
card = ["S2", "3", "4", "S5", "6", "7", "8", "S9", "S10", "11", "12", "13", "14"]

ammwin1 = data["Winner"].loc[data["Winner"] == 1].count()
ammwin2 = data["Winner"].loc[data["Winner"] == 2].count()

total = ammwin1 + ammwin2
ammwin1 = (ammwin1 / total) * 100
ammwin2 = (ammwin2 / total) * 100
pie_value = [ammwin1, ammwin2]
label = "Player 1 Win", "Player 2 Win"
style = "ggplot"
pyplot.pie(pie_value, labels=label, autopct='%1.1f%%',
           shadow=True, startangle=90, colors=("blue", "red"))
pyplot.show()


winning_card = []
    if data["Winner"].iloc[x] == 1:
        winning_card.append(data["Starting Hand Player 1.1"].iloc[x])
        winning_card.append(data["Starting Hand Player 1.2"].iloc[x])
        winning_card.append(data["Starting Hand Player 1.3"].iloc[x])
    if data["Winner"].iloc[x] == 2:
        winning_card.append(data["Starting Hand Player 2.1"].iloc[x])
        winning_card.append(data["Starting Hand Player 2.2"].iloc[x])
        winning_card.append(data["Starting Hand Player 2.3"].iloc[x])
best_card = []
for x in range(len(card)):
    best_card.append(winning_card.count(card[x]))

style = "ggplot"
pyplot.bar(card, best_card)
pyplot.show()

print(data["Biggest Add"].mean())

most_played = []
for x in range(len(data)):
    if data["Winner"].iloc[x] == 1:
        most_played.append(data["Most Played Card Player 1"].iloc[x])
    if data["Winner"].iloc[x] == 2:
        most_played.append(data["Most Played Card Player 2"].iloc[x])

mpb = []
for x in range(len(card)):
    mpb.append(most_played.count(card[x]))

style = "ggplot"
pyplot.bar(card, mpb)
pyplot.show()