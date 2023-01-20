from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv("gasolina.csv")


plt.figure(figsize=(8,6))
sns.set_theme(style="darkgrid")
gas = sns.lineplot(data=df, x='dia', y='venda', color='blue')
plt.savefig('gasolina_II.png', format='png')
plt.title("Preço Venda por dia")
plt.show()