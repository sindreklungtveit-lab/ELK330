import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 24, 500)

A = 800
mu = 13

sigma_values = [2, 3, 4, 5]

for sigma in sigma_values:
    G = A * np.exp(-(t - mu)**2 / (2 * sigma**2))
    plt.plot(t, G, label=f"sigma = {sigma}")

plt.xlabel("Tid [timer]")
plt.ylabel("Solinnstråling [W/m²]")
plt.title("Sensitivitetsanalyse av sigma")
plt.grid()
plt.legend()

plt.show()