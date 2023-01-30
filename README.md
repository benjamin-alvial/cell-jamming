![poster](presentations/poster/poster_nuclei_dynamics_final.png)

# Nuclei dynamics in epithelial monolayer

## Introduction

In granular systems, a critical packing fraction induces a jamming phenomenon, where particle velocity approaches zero. In epithelial tissue systems, a similar jamming phenomenon has been observed. The relationship between **nuclei velocity** and **nuclei packing fraction** is studied for MDCK (Madin-Darby canine kidney) cell migration, an example of unjamming.

First, a **correlation between these two variables is studied**. Second, the same correlation is analyzed with a more traditional measure of density, **number density**. We aim to show that nuclei packing fraction can be used as an equivalent measure to number density, useful for more diverse cell morphologies.

## Methods

The space is divided in a grid (Fig. 1). FIJI’s plugin TrackMate [1] is used to obtain the trajectories of each nucleus (Fig. 2). For each window j in the grid, an average velocity vj and speed uj is calculated for the nuclei contained within. Similarly, a packing fraction Φj for each window is calculated, as the quotient between nuclei pixels and total pixels.

For each time frame, the average local speeds and inverse packing fractions are used to calculate the Pearson correlation coefficient. This is also done for the inverse of number density and for both the 20 x 20 and 8 x 20 grid.

## Results and Discussion

* All fields (Fig. 3) show the significant migration in the upper-right corner of the video. In this region, nuclei travel at great speeds and are less packed.

* All correlation values are positive (Fig. 4), meaning speed increases as the packing of nuclei decreases, as is expected in an unjamming phenomenon.

* Correlation becomes stronger as time passes, probably because the chemical activation wave signalling for migration propagates to the left and induces a drift and enhanced transport, which corresponds to the unjamming phenomenon. This wave might have a specific frequency, which would explain the fact that after 5 hours correlation gets weaker and after 7 hours correlation increases once again.

* The correlations for the smaller grid show bigger fluctuations, probably due to being close to the wound.

* Between packing fraction and number density, the latter seems to have better correlation values, which may be due to how the contribution of a nuclei to a given window in the grid is calculated.

## Conclusions

Visual representations of the observables allowed for confirmation of expected results, and the Pearson coefficients calculated showed the existence of **moderate correlation** between speed and packing fraction, which **varied with time**. Number density seems to have better results, but not significant, than packing fraction. That is, **packing fraction can still be useful as a more universal measure of density**, considering nuclei of different morphologies.

## Future work

In the future, it would be useful to explore **different sizes for the grid’s windows** because there might be a characteristic correlation distance at which nuclei behave similar to their neighbors, which may have not been coincidental with those studied in this experiment. Furthermore, it would be interesting to study the same phenomenon in confluent videos of **healthy and cancerous tissues with dividing cells**, as a model describing these systems could be useful in cancer detection.

## References

[1] Ershov, D., Phan, M.-S., Pylvänäinen, J. W., Rigaud, S. U., Le Blanc, L., Charles-Orszag, A., ... Tinevez, J.-Y. (2022). TrackMate 7: integrating state-of-the-art segmentation
algorithms into tracking pipelines. Nature Methods, 19(7), 829–832. doi:10.1038/s41592-022-01507-1.

[2] Aoki, K. et al. (2017). “Propagating wave of ERK activation orients collective cell migration,” Developmental Cell, 43(3). Available at: https://doi.org/10.1016/j.devcel.2017.10.016.
