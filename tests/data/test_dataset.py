import colorteller.data.dataset as dataset
from loguru import logger


def test__TwoDimScalar():
    ds = dataset.TwoDimScalar()
    ds_1 = dataset.TwoDimScalar(index=6)

    logger.debug(ds_1.data().head())
