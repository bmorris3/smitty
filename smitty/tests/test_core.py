import numpy as np

from ..core import samples_to_latex

np.random.seed(42)

n_points = 1000

# Generate fake posterior samples:
flatchain = np.hstack([
    # Symmetric error bars
    np.random.normal(
        loc=[0, np.pi],
        scale=[0.1, 1],
        size=(n_points, 2)
    ),

    # Asymmetric distribution
    np.random.normal(
        loc=1, scale=0.2, size=(n_points, 1)
    ) ** 3.5
])

simple_table = r"""\begin{table}
\begin{tabular}{cc}
Parameter & Measurement \\
a & ${0.004}_{-0.096}^{+0.095}$ \\
b & ${183}_{-56}^{+58}$ \\
c & ${1.00}_{-0.52}^{+0.81}$ \\
\end{tabular}
\end{table}
"""


def test_samples_to_latex():
    table = samples_to_latex(
        flatchain,
        labels='a b c'.split(),
        transformation=[None, np.degrees, None],
        show_sign=True
    )

    assert table == simple_table
