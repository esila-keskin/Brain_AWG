"""
STEP 2 is the detailed view of the normalised map (the insula one).
Saves axial + sagittal + coronal slices to figures/.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from nilearn import plotting

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(DATA_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

normalised_map = os.path.join(DATA_DIR, "spmT_0001_2.nii.gz")

print("Plotting normalised map (bilateral insula)...")

#Axial slices: z from -10 to +35 to catch insula
fig, ax = plt.subplots(figsize=(18, 5))
plotting.plot_stat_map(
    normalised_map,
    threshold=2.5,
    display_mode="z",
    cut_coords=[-10, -2, 5, 12, 20, 28, 35],
    colorbar=True,
    title="Normalised connectivity (recovers post-flight) Axial [insula is ~z=0 to +15]",
    cmap="RdBu_r",
    axes=ax,
)
out = os.path.join(FIG_DIR, "normalised_axial.png")
plt.savefig(out, dpi=200, bbox_inches="tight")
plt.close()
print(f"Saved: {out}")

#Coronal slices
fig, ax = plt.subplots(figsize=(18, 5))
plotting.plot_stat_map(
    normalised_map,
    threshold=2.5,
    display_mode="y",
    cut_coords=[-10, 0, 8, 16, 24, 32],
    colorbar=True,
    title="Normalised connectivity Coronal",
    cmap="RdBu_r",
    axes=ax,
)
out = os.path.join(FIG_DIR, "normalised_coronal.png")
plt.savefig(out, dpi=200, bbox_inches="tight")
plt.close()
print(f"Saved: {out}")

# Glass brain (all 3 views at once) 
fig, ax = plt.subplots(figsize=(12, 5))
plotting.plot_glass_brain(
    normalised_map,
    threshold=2.5,
    colorbar=True,
    plot_abs=False,
    title="Normalised connectivity Glass brain (L/R/top/back)",
    axes=ax,
    display_mode="lyrz",
    cmap="RdBu_r",
)
out = os.path.join(FIG_DIR, "normalised_glass.png")
plt.savefig(out, dpi=200, bbox_inches="tight")
plt.close()
print(f"  Saved: {out}")

print("\nOpen these in figures/:")
print("normalised_axial.png <- axial slices, look for bilateral blobs on sides of brain")
print("normalised_coronal.png <- coronal view")
print("normalised_glass.png <- all 3 views overlaid")
print("\nThe insula appears as bilateral symmetric blobs on the LEFT and RIGHT sides of the brain")
print("in axial slices around z = 0 to +15 mm.")
