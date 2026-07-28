"""
STEP 4 is for making the actual figures for my paper
Shows the normalised (insula) map with axial slices + glass brain side by side.
Output: figures/fig_cosmonaut_insula.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from nilearn import plotting

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(DATA_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

normalised_map = os.path.join(DATA_DIR, "spmT_0001_2.nii.gz")
insula_seed_map = os.path.join(DATA_DIR, "spmT_0001_3.nii.gz")

fig = plt.figure(figsize=(16, 9))
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.1)

#  Top row: Normalised ICC map (insula) 
ax1 = fig.add_subplot(gs[0, 0])
plotting.plot_glass_brain(
    normalised_map,
    threshold=2.5,
    colorbar=False,
    plot_abs=False,
    title="Normalised ICC bilateral insula",
    axes=ax1,
    display_mode="z",
    cmap="RdBu_r",
)

ax2 = fig.add_subplot(gs[0, 1])
plotting.plot_stat_map(
    normalised_map,
    threshold=2.5,
    display_mode="z",
    cut_coords=[-5, 5, 15, 25],
    colorbar=True,
    title="Axial slices (z = −5 to +25 mm)",
    cmap="RdBu_r",
    axes=ax2,
)

# Bottom row: Insula seed connectivity 
ax3 = fig.add_subplot(gs[1, 0])
plotting.plot_glass_brain(
    insula_seed_map,
    threshold=2.5,
    colorbar=False,
    plot_abs=False,
    title="Insula seed → whole-brain connectivity (normalised)",
    axes=ax3,
    display_mode="z",
    cmap="RdBu_r",
)

ax4 = fig.add_subplot(gs[1, 1])
plotting.plot_stat_map(
    insula_seed_map,
    threshold=2.5,
    display_mode="z",
    cut_coords=[-5, 5, 15, 25],
    colorbar=True,
    title="Insula seed — axial slices",
    cmap="RdBu_r",
    axes=ax4,
)

fig.text(0.5, 0.01,
    "Cosmonaut rsfMRI (Jillings et al. Commun Biol 2023; N=11). "
    "Top: ICC changes that normalise post-flight (bilateral insula highlighted). "
    "Bottom: Insula-seeded connectivity changes that normalise. "
    "Data: NeuroVault collection 12152.",
    ha="center", fontsize=9, color="gray", wrap=True)

out = os.path.join(FIG_DIR, "fig_cosmonaut_insula.png")
plt.savefig(out, dpi=200, bbox_inches="tight")
plt.close()
print(f"Saved: {out}")
