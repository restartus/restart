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

    s_r = np.array([30, 60, 90])
    c_pn = np.array([[200, 3],
                     [1, 900]])
    log.critical(f"{s_r=}")
    log.critical(f"{c_pn=}")

    c_rpn = np.einsum("r,pn->rpn", s_r, c_pn)
    log.critical(f"{c_rpn=}")


if __name__ == "__main__":
    main()
