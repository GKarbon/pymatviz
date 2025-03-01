"""Stats for the matbench_perovskites dataset.

Input: Pymatgen Structure of the material.
Target variable: Heat of formation of the entire 5-atom perovskite cell in eV
    as calculated by RPBE GGA-DFT. Note the reference state for oxygen was
    computed from oxygen's chemical potential in water vapor, not as oxygen
    molecules, to reflect the application which these perovskites were studied for.
Entries: 18,928

Matbench v0.1 dataset for predicting formation energy from crystal structure.
Adapted from an original dataset generated by Castelli et al.

https://ml.materialsproject.org/projects/matbench_perovskites
"""

# %%
from matminer.datasets import load_dataset
from tqdm import tqdm

import pymatviz as pmv
from pymatviz.enums import Key


# %%
df_perov = load_dataset("matbench_perovskites")

df_perov[[Key.spg_symbol, Key.spg_num]] = [
    struct.get_space_group_info() for struct in tqdm(df_perov[Key.structure])
]
df_perov[Key.volume] = df_perov[Key.structure].map(lambda struct: struct.volume)

df_perov[Key.formula] = df_perov[Key.structure].map(lambda cryst: cryst.formula)

df_perov[Key.crystal_system] = df_perov[Key.spg_num].map(pmv.utils.spg_to_crystal_sys)


# %%
fig = pmv.structure_2d_plotly(df_perov[Key.structure].iloc[:12])
fig.layout.title.update(text="Perovskite structures in Matbench Perovskites dataset")
fig.layout.paper_bgcolor = "white"
fig.show()
# pmv.save_fig(fig, "perovskite-structures-2d.pdf")


# %%
fig = df_perov["e_form"].hist(backend="plotly", nbins=100)
fig.layout.title.update(
    text="Formation energy histogram of Matbench Perovskites dataset"
)
fig.layout.showlegend = False
fig.show()
# pmv.save_fig(fig, "perovskites-e_form-hist.pdf")


# %%
fig = pmv.ptable_heatmap_plotly(df_perov[Key.formula], log=True)
fig.layout.title.update(text="Elements in Matbench Perovskites dataset")
fig.show()
# pmv.save_fig(fig, "perovskites-ptable-heatmap.pdf")


# %%
fig = df_perov[Key.crystal_system].value_counts().plot.bar(rot="horizontal")
fig.layout.title.update(text="Crystal systems in Matbench Perovskites")
pmv.powerups.annotate_bars(fig, v_offset=250)

fig.show()
# pmv.save_fig(fig, "perovskites-crystal-system-counts.pdf")


# %%
df_perov.plot.scatter(x=Key.volume, y="e_form", c=Key.spg_num, colormap="viridis")


# %%
fig = pmv.spacegroup_sunburst(df_perov[Key.spg_num], show_counts="percent")
fig.layout.title.update(text="Matbench Perovskites spacegroup sunburst", x=0.5)
fig.show()
# fig.write_image("perovskite-spacegroup-sunburst.pdf")
