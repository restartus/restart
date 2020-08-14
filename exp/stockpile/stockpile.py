"""Test Iterable.

Overall testing of iteration
"""
import numpy as np  # type: ignore

from log import Log


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
    # This is a (1,3)
    col_r = np.array([[30], [60], [90]])
    log.critical(f"{col_r=} {col_r.shape=}")

    c_pn = np.array([[200, 3], [1, 900]])
    log.critical(f"{c_pn=} {c_pn.shape=}")

    # the simplest way but potentially slower
    ein_rpn = np.einsum("r,pn->rpn", v_r, c_pn)
    log.critical(f"{ein_rpn=}")

    # For broadcasting to work, numpy starts with the trailing dimensions
    # and determine compatbility. Either the dimensions are equal or
    # one of them is a one.
    # The resulting dimension is the max, so it it overrides the one with that
    # dimension
    # For this to work we have
    # A consumption array that is p x d
    # The stockpile is r long, so to make this work and to get eventually
    # r x p x d is tricky
    # so one choice is to to get (p, d, r) and then so we then need an 1x1xr
    # and then this should broadcast
    # https://towardsdatascience.com/two-cool-features-of-python-numpy-mutating-by-slicing-and-broadcasting-3b0b86e8b4c7
    # So it
    # https://numpy.org/doc/stable/reference/generated/numpy.expand_dims.html
    # or more clear is  which pushs a vector down as deep as the c_pn tuple is
    #
    # This means expand dimensions start at the front
    # up to the number of dimenstions of c_pn which is 2 for this test
    # but could be more when there is time etc.
    v_pnr = np.expand_dims(v_r, axis=tuple(range(len(c_pn.shape))))
    log.critical(f"{v_pnr=}")

    # how we add a lower dimension vs c_pn[np.newaxis,...]
    c_pnr = c_pn[..., np.newaxis]
    log.critical(f"{c_pnr=}")
    bcast_pnr = c_pnr * v_pnr
    # swap the high order and the lower order
    bcast_rpn = np.swapaxes(bcast_pnr, 0, len(bcast_pnr.shape) - 1)
    log.critical(f"{bcast_rpn=}")

    # you need a special function to handle different shapes
    # https://stackoverflow.com/questions/10580676/comparing-two-numpy-arrays-for-equality-element-wise
    # if np.array_equal(bcast_rpn, ein_rpn):
    if np.allclose(bcast_rpn, ein_rpn):
        log.error("bcast_rpn is not the same as ein_rpn")


if __name__ == "__main__":
    main()
