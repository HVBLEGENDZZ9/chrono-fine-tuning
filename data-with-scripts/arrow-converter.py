from pathlib import Path
from typing import List, Optional, Union

import numpy as np
import pandas as pd
from gluonts.dataset.arrow import ArrowWriter


def convert_to_arrow(
    path: Union[str, Path],
    time_series: Union[List[np.ndarray], np.ndarray],
    start_times: Optional[Union[List[np.datetime64], np.ndarray]] = None,
    compression: str = "lz4",
):
    if start_times is None:
        # Set an arbitrary start time
        start_times = [np.datetime64("2000-01-01 00:00", "s")] * len(time_series)

    assert len(time_series) == len(start_times)

    dataset = [
        {"start": start, "target": ts} for ts, start in zip(time_series, start_times)
    ]
    ArrowWriter(compression=compression).write_to_file(
        dataset,
        path=path,
    )


if __name__ == "__main__":
    # Generate 20 random time series of length 1024

    df = pd.read_csv('data-with-scripts/data/bitcoin-prices.csv')
    time_series = [df['Price'].values]

    # Convert to GluonTS arrow format
    convert_to_arrow("data-with-scripts/data/bitcoin-prices.arrow", time_series=time_series)
