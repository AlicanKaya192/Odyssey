The formula of linear regression contains $(X^\mathsf{T}X)^{-1}$. Consider two small data matrices (row = example, column = feature):

$$
X_1 = \begin{bmatrix} 1 & 2 \\ 2 & 4 \\ 3 & 6 \end{bmatrix}
$$

$$
X_2 = \begin{bmatrix} 1 & 2 \\ 2 & 4 \\ 3 & 7 \end{bmatrix}
$$

The only difference is the $6$ versus $7$ in the last row. Find $\det(X^\mathsf{T}X)$ for each.
