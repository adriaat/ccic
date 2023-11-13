"""
Tests for the ccic.data.utils module.
"""
import os
from pathlib import Path

import numpy as np
import pytest

from ccic.data.cpcir import CPCIR
from ccic.data.utils import extract_roi, included_pixel_mask

TEST_DATA = os.environ.get("CCIC_TEST_DATA", None)
if TEST_DATA is not None:
    TEST_DATA = Path(TEST_DATA)
NEEDS_TEST_DATA = pytest.mark.skipif(
    TEST_DATA is None, reason="Needs 'CCIC_TEST_DATA'."
)
CPCIR_FILE = "merg_2008020101_4km-pixel.nc4"

@NEEDS_TEST_DATA
def test_extract_roi():
    """
    Ensure that extracting data based on a region of interest returns
    and area with the coordinates within the expected limits and ensures
    the min_size option return correctly sized region.
    """
    cpcir_file = CPCIR(TEST_DATA / CPCIR_FILE)
    cpcir_data = cpcir_file.to_xarray_dataset()

    data_roi = extract_roi(cpcir_data, (-10, -10, 10, 10))
    assert (data_roi.lat.data >= -10).all()
    assert (data_roi.lat.data <= 10).all()
    assert (data_roi.lon.data >= -10).all()
    assert (data_roi.lon.data <= 10).all()

    data_roi = extract_roi(cpcir_data, (-1, -1, 1, 1), min_size=256)
    assert data_roi.lat.size == 256
    assert data_roi.lon.size == 256

    data_roi_1 = extract_roi(cpcir_data, (170, -10, 180, 10))
    data_roi_2 = extract_roi(cpcir_data, (170, -10, 190, 10))

    assert data_roi_1.lat.size == data_roi_2.lat.size
    assert 2 * data_roi_1.lon.size == data_roi_2.lon.size



def test_included_pixel_mask():
    """
    Ensure that included pixel mask

    """
    indices = (np.arange(101), np.arange(101))
    mask = included_pixel_mask(indices, 50, 50, 10)

    assert np.isclose(mask.sum(), 10)
