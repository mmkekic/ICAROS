"""
Tests for fit_functions
"""

import numpy as np

from pytest        import mark
from pytest        import approx
from pytest        import raises
from flaky         import flaky
from numpy.testing import assert_array_equal
from numpy.testing import assert_allclose

from hypothesis            import given, settings
from hypothesis.strategies import integers
from hypothesis.strategies import floats
from invisible_cities.core.testing_utils       import exactly
from invisible_cities.core.testing_utils       import float_arrays
from invisible_cities.core.testing_utils       import FLOAT_ARRAY
from invisible_cities.core.testing_utils       import random_length_float_arrays

from . core_functions       import find_nearest
from . core_functions       import divide_np_arrays
from . core_functions       import file_numbers_from_file_range

from   invisible_cities.evm.ic_containers  import Measurement


def nearest(a, v):
    """Alternative (not optimized) implementation of find_nearest
    Used for testing purpose only

    """
    nr =a[0]
    diff = 1e+9
    for x in a:
        if np.abs(x-v) < diff:
            nr = x
            diff = np.abs(x-v)
    return nr


def test_simple_find_nearest():
    x = np.arange(100)
    assert find_nearest(x, 75.6)   == exactly(76)
    assert find_nearest(x, 75.5)   == exactly(75)


def test_gauss_find_nearest():
    e = np.random.normal(100, 10, 100)

    for x in range(1, 100, 10):
        assert find_nearest(e, x)   == approx(nearest(e, x), rel=1e-3)


@given(float_arrays(min_value=1,
                    max_value=100))
def test_find_nearest(data):
    assert find_nearest(data, 10)   == approx(nearest(data, 10), rel=1e-3)


def test_divide_np_array():
    x = np.array([10,100,1000,5000])
    y = np.array([2,5,0,100])
    assert_array_equal(divide_np_arrays(x,y), np.array([  5.,  20.,   0.,  50.]))


def test_file_numbers_from_file_range():
    N = file_numbers_from_file_range((0,10))
    N09       = ['0000','0001','0002','0003','0004','0005','0006','0007','0008','0009']
    assert_array_equal(N, N09)
    N1119     = ['0011', '0012', '0013', '0014', '0015', '0016', '0017', '0018']
    N = file_numbers_from_file_range((11,19))
    assert_array_equal(N, N1119)
    N100109   = ['0100', '0101', '0102', '0103', '0104', '0105', '0106', '0107', '0108']
    N = file_numbers_from_file_range((100,109))
    assert_array_equal(N, N100109)
    N10001009 = ['1000', '1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008']
    N = file_numbers_from_file_range((1000,1009))
    assert_array_equal(N, N10001009)
