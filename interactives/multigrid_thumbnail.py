# Regenerate with: python3 interactives/multigrid_thumbnail.py interactives/multigrid.png
# Thumbnail for the Interactives listing: error estimates on several grids
# from one V-cycle (k=10, nu=3), the same computation as the page.
import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
phi = lambda x: 20.* np.pi * x**3
f = lambda x: -20 + 0.5*120*np.pi*x * np.cos(phi(x)) - 0.5*(60*np.pi*x**2)**2 * np.sin(phi(x))
def coarsen(f): return f[1::2]
def interpolate(f,a,b):
    mc=len(f); out=np.zeros(2*mc+1); out[1::2]=f; out[2:-1:2]=0.5*(f[:-1]+f[1:]); out[0]=0.5*(out[1]+a); out[-1]=0.5*(out[-2]+b); return out
def Jacobi(U,f,a,b,m,nu,w=2/3):
    h=1/(m+1)
    for _ in range(nu):
        Up=np.concatenate([[a],U,[b]]); U=(1-w)*U+w*(0.5*(Up[:-2]+Up[2:])-0.5*h*h*f)
    Up=np.concatenate([[a],U,[b]]); return U, f-(Up[:-2]-2*U+Up[2:])/h**2
k,nu=10,3
m=2**k-1; rdep=k-1; x=np.linspace(0,1,m+2)[1:-1]; F=f(x); U=np.linspace(1,3,m)
r=[None]*(rdep+1); e=[None]*(rdep+1)
U,rr=Jacobi(U,F,1,3,m,nu)
for i in range(1,rdep+1):
    m=(m-1)//2; r[i]=coarsen(rr); e[i],rr=Jacobi(np.zeros(m),-r[i],0,0,m,nu)
for i in range(1,rdep):
    m=2*m+1; err=e[rdep-i]-interpolate(e[rdep+1-i],0,0); e[rdep-i],rr=Jacobi(err,-r[rdep-i],0,0,m,nu)
fig,ax=plt.subplots(figsize=(4,3),dpi=150)
fig.patch.set_facecolor("white")
levels=[5,4,3,2,1]
cmap=plt.get_cmap("viridis")
for j,l in enumerate(levels):
    y=np.concatenate([[0],e[l],[0]]); xx=np.linspace(0,1,len(y))
    ax.plot(xx,y,'-o' if len(y)<40 else '-',ms=3,lw=1.5,color=cmap(j/(len(levels)-1)*0.85),label=f"m = {len(e[l])}")
ax.axhline(0,color="0.6",lw=0.8)
ax.set_xlim(0,1)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_color("0.7")
fig.tight_layout()
fig.savefig(sys.argv[1])
print([float(np.abs(e[l]).max()) for l in levels])
