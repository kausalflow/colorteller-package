import colorteller.data.dataset as dataset


def test__TwoDimScalar():
    ds = dataset.TwoDimScalar(2, 2)
    assert ds.shape == (2, 2)
    assert ds.dtype == float
    assert ds.ndim == 2
    assert ds.size == 4
    assert ds.nbytes == 16

