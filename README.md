# The Correlation between Wikimedians of Mainland China Membership and Voting Pattern in 2017 on Chinese Wikipedia

By [mys_721tx][1], [PhiLiP][2]

All documentations are released under
[Creative Commons Attribution-ShareAlike 3.0 Unported][3]. All programs are
released under [GNU General Public License 3.0][4].

We investigated the correlation between Wikimedians of Mainland
China (WMC) membership and voting pattern.

## Methods

We sampled all [community elections in 2017 on Chinese Wikipedia][5]. Community
election is defined as an election where the community decides whether the
nominee should receive an administrative privilege including administrator,
bureaucrat, checkuser, or oversighters. Any election that was closed before the
two week election period is not counted in the sample. We used the
[public list of WMC members][6] to compile a list of WMC members.

Every user that had casted a valid vote is counted as an instance. Each support
vote is coded as 1. Each oppose vote is coded as -1. If a user was absent or
voted other than support or oppose, their vote is coded 0.

We removed one invalid vote due to error in the sampling process. We
reattributed 16 votes as the users that casted them had either changed their
signatures or their usernames. A 23-by-217 matrix is made from the sample.

In order to obtain a lower dimension representation of the data, we used the
`pca` function provided in `scikit-learn` to perform principle component
analysis to 2 dimensions. We obtain first two principle component, PC1 and PC2.

![A plot of PC1 and PC2 of the voting pattern. Blue points represents non-WMC members. Green points represents WMC members.](plots/pca-2017.png?raw=true)

We performed logistic regression in the log-likelihood of being a WMC member in
response of changes in PC1 and PC2.

```R
Logistic Regression Model

 lrm(formula = Membership ~ PC1 + PC2, data = sample)

                       Model Likelihood     Discrimination    Rank Discrim.
                          Ratio Test           Indexes           Indexes
 Obs           217    LR chi2     107.73    R2       0.589    C       0.918
  FALSE        166    d.f.             2    g        2.928    Dxy     0.836
  TRUE          51    Pr(> chi2) <0.0001    gr      18.684    gamma   0.841
 max |deriv| 2e-09                          gp       0.298    tau-a   0.302
                                            Brier    0.096

           Coef    S.E.   Wald Z Pr(>|Z|)
 Intercept -2.0626 0.3001 -6.87  <0.0001
 PC1        1.2297 0.2791  4.41  <0.0001
 PC2       -3.7190 0.6354 -5.85  <0.0001
 ```

We simulated random voting by drawing from the uniform distribution `{-1, 0, 1}`
for comparison. We repeated the PCA for non-WMC users and the simulated data.

![A plot of PC1 and PC2 of the simulated voting pattern. Blue points represents non-WMC members. Green points represents simulated data.](plots/pca-simulation.png?raw=true)

### Discussion

[1]: https://meta.wikimedia.org/wiki/User:Mys_721tx
[2]: https://meta.wikimedia.org/wiki/User:PhiLiP
[3]: https://creativecommons.org/licenses/by-sa/3.0/
[4]: https://www.gnu.org/licenses/gpl-3.0.txt
[5]: https://zh.wikipedia.org/wiki/Wikipedia:管理人員任免記錄/2017年
[6]: https://meta.wikimedia.org/wiki/Wikimedians_of_Mainland_China/Members
