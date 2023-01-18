import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

df = pd.read_csv("gasolina.csv")

plt.figure(figsize=(8,6))
sns.set_theme(style="darkgrid")
gas = sns.lineplot(data=df, x='dia', y='venda', color='red')
plt.savefig('gas.png', format='png')
plt.show()