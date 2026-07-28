import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from nilearn import plotting

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(DATA_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

maps = [
    ("spmT_0001.nii.gz", "Post vs Pre: all changes (N=15)"),
    ("spmT_0001_1.nii.gz", "Sustained: still different at 8 months (N=11)"),
    ("spmT_0001_2.nii.gz", "*** NORMALISED: recovers - BILATERAL INSULA *** (N=11)"),
    ("spmT_0001_3.nii.gz", "Insula seed connectivity (normalised)"),
    ("spmT_0001_4.nii.gz", "Thalamus seed connectivity (sustained)"),
    ("spmT_0001_5.nii.gz", "Right angular gyrus seed connectivity (sustained)"),
]

fig, axes = plt.subplots(3, 2, figsize=(18, 20))
axes = axes.flatten()

for idx, (fname, title) in enumerate(maps):
    path = os.path.join(DATA_DIR, fname)
    plotting.plot_glass_brain(
        path,
        threshold=2.0,
        colorbar=True,
        plot_abs=False,
        title=title,
        axes=axes[idx],
        display_mode="lyrz",
        cmap="RdBu_r",
    )
    print(f" Plotted [{idx+1}/6]: {fname}")

plt.tight_layout()
out = os.path.join(FIG_DIR, "all_6_maps.png")
plt.savefig(out, dpi=150, bbox_inches="tight")
plt.close()
print(f"\nSaved: {out}")
print("Open figures/all_6_maps.png to see all 6 brain maps.")
