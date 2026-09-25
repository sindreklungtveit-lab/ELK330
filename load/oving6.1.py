import numpy as np
import matplotlib.pyplot as plt

# 1. Tidsakse fra kl. 00 til kl. 24
t = np.linspace(0, 24, 500)

# 2. Maksimal solinnstråling
A = 800

# 3. Tidspunkt for maksimal solinnstråling
mu = 13

# 4. Bredde på Gauss-kurven
sigma = 3

# Beregn solinnstrålingen
G = A * np.exp(-(t - mu)**2 / (2 * sigma**2))

# 5. Plot Gauss-kurven
plt.plot(t, G)

plt.xlabel("Tid [timer]")
plt.ylabel("Solinnstråling [W/m²]")
plt.title("Gauss-modell for solinnstråling")
plt.grid()

plt.show()