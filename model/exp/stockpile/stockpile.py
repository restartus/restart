"""Test Iterable.

Overall testing of iteration
"""
import numpy as np  # type: ignore
from util import Log


def main():
    """Run Main.

    here we go
    """
    root_log = Log()
    log = root_log.log

    # this is a numpy vector so of type (3,)
    # this kind of vector cannot be cast
    v_r = np.array([30, 60, 90])
    log.critical(f"{v_r=} {v_r.shape=}")
    # The s_r is a (3,1) list so a row vector
    row_r = np.array([[30, 60, 90]])
    log.critical(f"{row_r=} {row_r.shape=}")
    # making a real column vector
    # https://stackoverflow.com/questions/17428621/python-differentiating-between-row-and-column-vectors
    col_r = np.array([[30], [60], [90]])
    log.critical(f"{col_r=} {col_r.shape=}")

    c_pn = np.array([[200, 3],
                     [1, 900]])
    log.critical(f"{c_pn=} {c_pn.shape=}")

    # the simplest way but potentially slower
    ein_rpn = np.einsum("r,pn->rpn", v_r, c_pn)
    log.critical(f"{ein_rpn=}")

    # using casting
    cast_rpn = c_pn * row_r
    log.critical(f"{cast_rpn=}")


if __name__ == "__main__":
    main()
