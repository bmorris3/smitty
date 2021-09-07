import numpy as np

__all__ = [
    'display_one_sigma',
    'samples_to_astropy_table',
    'samples_to_latex'
]


def default_decimal_places(lo, mi, hi):
    """
    Default guess for the number of decimal places to display
    """
    return abs(int(np.min(np.floor(np.log10([hi - mi, mi - lo]))) - 1))


def format_upper_lower(low, mid, high, decimal_places=None, zero_pad='',
                       wrap='$', show_sign=True):
    """
    Format a string with the median and one-sigma upper and lower bounds.
    """
    if decimal_places is None:
        fmt_str = "{0}.{1}f".format(zero_pad,
                                    default_decimal_places(low, mid, high))
    else:
        fmt_str = "{0}.{1}f".format(zero_pad, decimal_places)

    if show_sign:
        signs = ['-', '+']
    else:
        signs = ['', '']

    return (
        wrap + f"{{{mid: ^{fmt_str}}}}_{{{signs[0]}{mid - low:^{fmt_str}}}}"
        f"^{{{signs[1]}{high - mid:^{fmt_str}}}}" + wrap
    )


def chain_to_one_sigma(samples, transformation=None):
    """
    Turn samples from a chain into [-1, 0, 1] sigma measurements
    """
    if transformation is None:
        transformation = lambda x: x
    return np.percentile(transformation(samples), [16, 50, 84])


def display_one_sigma(samples):
    """
    Display the measurement and one-sigma interval in iPython with LaTeX
    """
    from IPython.display import display_latex

    display_latex(format_upper_lower(*chain_to_one_sigma(samples)), raw=True)


def samples_to_astropy_table(flatchain, labels=None, transformation=None,
                             extra_column=None, **kwargs):
    """
    Turn a flat chain (from emcee for example) into an astropy table of formatted strings
    """
    from astropy.table import Table

    rows = []

    if isinstance(transformation, list):
        trans = transformation
    elif transformation is not None:
        trans = flatchain.shape[1] * [transformation]
    else:
        trans = flatchain.shape[1] * [lambda x: x]

    if labels is None:
        labels = [f'Parameter {n}' for n in range(flatchain.shape[1])]

    if extra_column is not None:
        if isinstance(extra_column, bool):
            extras = ["" for _ in range(flatchain.shape[1])]
        else:
            extras = extra_column

    for i, label, samples, tr in zip(
            range(len(labels)), labels, flatchain.T, trans
    ):
        if extra_column is not None:
            rows.append(
                [label, extras[i],
                 format_upper_lower(*chain_to_one_sigma(
                     samples, transformation=tr
                 ), **kwargs)]
            )
        else:
            rows.append(
                [label,
                 format_upper_lower(*chain_to_one_sigma(
                     samples, transformation=tr
                 ), **kwargs)]
            )

    return Table(
        rows=rows, names="Parameter, Comment, Measurement".split(', ')
        if extra_column is not None else "Parameter, Measurement".split(', ')
    )


def samples_to_latex(flatchain, labels=None, transformation=None, **kwargs):
    """
    Turn a flat chain (from emcee for example) into a LaTeX table.
    """
    import io
    from astropy.io import ascii

    with io.StringIO() as output:
        ascii.write(
            samples_to_astropy_table(
                flatchain, labels=labels, transformation=transformation,
                **kwargs
            ),
            output,
            format='latex'
        )
        return output.getvalue()
