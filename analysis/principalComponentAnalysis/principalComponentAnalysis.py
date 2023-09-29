from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')


data_frame = pd.read_csv(
    r"/home/ubuntu/Documents/file_to_work/yield_6x299.csv")
print(data_frame.tail(10))

scaler = StandardScaler()
# remove Y variable
df = data_frame.drop(['GRAIN_YIELD'], axis=1)
scaler.fit(df)
X_scaled = scaler.transform(df)

pca = PCA(n_components=6)
pca.fit(X_scaled)
X_pca = pca.transform(X_scaled)

print("shape of X_pca", X_pca.shape)
explication = pca.explained_variance_ratio_
print(explication)
print('suma:', sum(explication[0:2]))

weights = pca.components_[0]
# Las columnas más importantes son aquellas con los pesos más altos en valor absoluto
most_important_columns = np.abs(weights).argsort()[::-1]

plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('Numero de traits')
plt.ylabel('Acumulacion de varianza')
plt.show()
print("Finish")

# Xax = X_pca[:, 0]
# Yax = X_pca[:, 1]
# labels = data_frame['GRAIN_YIELD'].values
# cdict = {0: 'red', 1: 'green'}
# labl = {0: '1000_GRAIN_WEIGHT', 1: 'PLANT_HEIGHT'}
# marker = {0: '*', 1: 'o'}
# alpha = {0: .3, 1: .5}
# fig, ax = plt.subplots(figsize=(7, 5))
# fig.patch.set_facecolor('white')
# for l in np.unique(labels):
#     ix = np.where(labels == l)
#     ax.scatter(Xax[ix], Yax[ix], c=cdict[l], label=labl[l],
#                s=40, marker=marker[l], alpha=alpha[l])

# plt.xlabel("First Principal Component", fontsize=14)
# plt.ylabel("Second Principal Component", fontsize=14)
# plt.legend()
# plt.show()
