---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.19.5
kernelspec:
  name: python3
  display_name: Python 3 (ipykernel)
  language: python
---

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
%matplotlib ipympl
```

```{code-cell} ipython3
def mandelbrot(h=1000, w=1000, ite=50 ,xmin=-2, xmax=0.8,ymin=-1.4,ymax=1.4):
    grille = np.linspace(xmin,xmax,w) + 1j*np.array([np.linspace(ymax,ymin,h)]).T
    Z=grille.copy()
    for _ in range(ite):
        mask=abs(Z)<=2
        Z[mask] = Z[mask]**2 + grille[mask]
    return 2-abs(Z),[xmin,xmax,ymin,ymax]
```

```{code-cell} ipython3

def color(z):
    th = np.angle(z)
    a = abs(z)%2
    m=(2-a)/2
    R = m*np.cos(th/2)**2
    G = m*np.cos((th+ np.pi/3)/2)**2
    B = m*np.cos((th- np.pi/3)/2)**2
    return [R,G,B]

def joli_mandelbrot(h=1000, w=1000, ite=50 ,xmin=-2, xmax=0.8,ymin=-1.4,ymax=1.4):
    grille = np.linspace(xmin,xmax,w) + 1j*np.array([np.linspace(ymax,ymin,h)]).T
    Z=grille.copy()
    for _ in range(ite):
        mask=abs(Z)<=2
        Z[mask] = Z[mask]**2 + grille[mask]
    return np.array(color(Z)).T,[ymin,ymax,xmax,xmin]
```

```{code-cell} ipython3
#pour sauvegarder une figure:
#Img = mandelbrot()
#plt.imshow(Img[0], extent = Img[1])
#plt.savefig("mandelbrot.png") 
```

```{code-cell} ipython3
M = mandelbrot()
Mz = mandelbrot(w=2000, xmin=-1.27,xmax=-1.239,ymin=0.373,ymax=0.39)
jM = joli_mandelbrot( ite=20)
jMz = joli_mandelbrot(w=2000, xmin=-1.27,xmax=-1.239,ymin=0.373,ymax=0.39)
fig,axes = plt.subplots (2,2)
axes[0,0].imshow(M[0] , extent = M[1])
axes[1,0].imshow(Mz[0] , extent = Mz[1])
axes[0,1].imshow(jM[0] , extent = jM[1])
axes[1,1].imshow(jMz[0] , extent = jMz[1])
```

```{code-cell} ipython3

```

```{code-cell} ipython3

```
