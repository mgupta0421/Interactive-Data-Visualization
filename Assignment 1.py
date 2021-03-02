import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colorbar
import numpy as np

# reading file
df = pd.read_csv("field2.irreg.txt",header=None,sep='\n')
df = df.drop([0,1,2,3,4,5])
df = df[0].str.split(' ', expand=True)
df = df.rename(columns={0:'x',1:'y',2:'z',3:'dx',4:'dy',5:'dz'})

# converting data values to float
x_values = df['x']
x_values = x_values.astype('float')
y_values = df['y']
y_values = y_values.astype('float')
dx_values = df['dx']
dx_values = dx_values.astype('float')
dy_values = df['dy']
dy_values = dy_values.astype('float')
M = np.hypot(dx_values, dy_values)

# creating image
fig, ax = plt.subplots(dpi=400)
plt.quiver(x_values, y_values, dx_values, dy_values, M, scale=15, pivot='mid', width=0.0015)
plt.title("Water Flow Visualization")
plt.xlabel("X Equivalent of Vector")
plt.ylabel("Y Equivalent of Vector")
cbar = plt.colorbar(ticks=[0, 0.5, 1], orientation='vertical')
cbar.ax.set_yticklabels(['Low', 'Medium', 'High'])
plt.show()

# saving image
fig.savefig('Water Flow Visualization.png')
