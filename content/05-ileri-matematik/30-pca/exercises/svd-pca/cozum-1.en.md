**What is asked?** Going from the SVD's singular values to PCA's eigenvalues and share.

**Idea:** $X^\mathsf{T}X = VS^2V^\mathsf{T}$; the covariance is $\frac{1}{n - 1}X^\mathsf{T}X$, with eigenvalues $\frac{s_j^2}{n - 1}$.

**Step 1 — $\lambda_1$.** $\frac{400}{10} = 40$.

**Step 2 — $\lambda_3$.** $\frac{25}{10} = 2.5$. ($\lambda_2 = 10$.)

**Step 3 — Share.** $\frac{40}{40 + 10 + 2.5} = \frac{40}{52.5} \approx 0.762$.

**Check:** As the singular values halve, the eigenvalues fall to a quarter ($40 \to 10 \to 2.5$): the square relation ✓.

**Watch out:** Computing the share directly from the singular values ($\frac{20}{35} \approx 0.571$) is wrong; variance is proportional to the square of the singular value.

**Answer:** $40$, $2.5$, $\approx 0.762$.
