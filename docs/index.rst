Format LaTeX tables from posterior samples
------------------------------------------

Basic Usage
^^^^^^^^^^^

Say you've generated a flat posterior sample chain, like from emcee,
for example. There are three free parameters, one is given in units of radians.
Let's represent these results with their plus/minus one-sigma limits in a
LaTeX table:


.. code-block:: python

    >>> import numpy as np
    >>> from smitty import samples_to_latex

    >>> np.random.seed(42)
    >>> flatchain = np.random.normal(
    ...     loc=[0, np.pi, 10],
    ...     scale=[0.1, 1, 4],
    ...     size=(1000, 3)
    ... )

    >>> print(
    ...     samples_to_latex(
    ...         flatchain,
    ...         labels='a b c'.split(),
    ...     )
    ... )
    \begin{table}
    \begin{tabular}{cc}
    Parameter & Measurement \\
    a & ${0.006}_{-0.096}^{+0.095}$ \\
    b & ${3.12}_{-1.00}^{+0.99}$ \\
    c & ${10.2}_{-3.8}^{+3.8}$ \\
    \end{tabular}
    \end{table}

The results are shown with usually appropriate numbers of significant figures.
Let's say the second quantity is an angle in units of radians and we'd like to
report it in units of degrees, and we don't want signs on the upper and lower
intervals. We can do this with:

.. code-block:: python

    >>> print(
    ...     samples_to_latex(
    ...         flatchain,
    ...         labels='a b c'.split(),
    ...         transformation=[None, np.degrees, None],
    ...         show_sign=False
    ...     )
    ... )
    \begin{table}
    \begin{tabular}{cc}
    Parameter & Measurement \\
    a & ${0.006}_{0.096}^{0.095}$ \\
    b & ${179}_{57}^{57}$ \\
    c & ${10.2}_{3.8}^{3.8}$ \\
    \end{tabular}
    \end{table}

Want more decimal places reported?

.. code-block:: python

    >>> print(
    ...     samples_to_latex(
    ...         flatchain,
    ...         labels='a b c'.split(),
    ...         decimal_places=3
    ...     )
    ... )
    \begin{table}
    \begin{tabular}{cc}
    Parameter & Measurement \\
    a & ${0.006}_{-0.096}^{+0.095}$ \\
    b & ${3.124}_{-0.997}^{+0.994}$ \\
    c & ${10.169}_{-3.785}^{+3.803}$ \\
    \end{tabular}
    \end{table}

Want to add an extra column with comments defining each variable?

.. code-block:: python

    >>> print(
    ...     samples_to_latex(
    ...         flatchain,
    ...         labels='a b c'.split(),
    ...         extra_column='apples bananas cucumbers'.split()
    ...     )
    ... )
    \begin{table}
    \begin{tabular}{ccc}
    Parameter & Comment & Measurement \\
    a & apples & ${0.006}_{-0.096}^{+0.095}$ \\
    b & bananas & ${3.12}_{-1.00}^{+0.99}$ \\
    c & cucumbers & ${10.2}_{-3.8}^{+3.8}$ \\
    \end{tabular}
    \end{table}


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   smitty/index.rst
