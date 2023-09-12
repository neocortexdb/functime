import polars as pl
from polars.testing import assert_frame_equal

from functime.feature_extraction.features_raphael import (
    change_quantiles,
    first_location_of_maximum,
    first_location_of_minimum,
    last_location_of_maximum,
    last_location_of_minimum,
    mean_abs_change,
    mean_change,
    number_crossing_m,
    var_greater_than_std,
)


def test_change_quantiles():
    df = pl.DataFrame({"value": list(range(10))})
    df_lazy = pl.LazyFrame({"value": list(range(10))})
    assert_frame_equal(
        df.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=0.9, isabs=True, f_agg="mean")
        ),
        pl.DataFrame({"value": [1.0]}),
    )
    assert_frame_equal(
        df_lazy.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=0.9, isabs=True, f_agg="mean")
        ).collect(),
        pl.DataFrame({"value": [1.0]}),
    )
    assert_frame_equal(
        df.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=0.9, isabs=False, f_agg="std")
        ),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df_lazy.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=0.9, isabs=False, f_agg="std")
        ).collect(),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df.select(
            change_quantiles(
                pl.col("value"), ql=0.15, qh=0.18, isabs=True, f_agg="mean"
            )
        ),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df_lazy.select(
            change_quantiles(
                pl.col("value"), ql=0.15, qh=0.18, isabs=True, f_agg="mean"
            )
        ).collect(),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=0.9, isabs=True, f_agg="std")
        ),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df_lazy.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=0.9, isabs=True, f_agg="std")
        ).collect(),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=0.9, isabs=False, f_agg="mean")
        ),
        pl.DataFrame({"value": [1.0]}),
    )
    assert_frame_equal(
        df_lazy.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=0.9, isabs=False, f_agg="mean")
        ).collect(),
        pl.DataFrame({"value": [1.0]}),
    )
    assert_frame_equal(
        df.select(
            change_quantiles(
                pl.col("value"), ql=0.15, qh=0.18, isabs=False, f_agg="mean"
            )
        ),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df_lazy.select(
            change_quantiles(
                pl.col("value"), ql=0.15, qh=0.18, isabs=False, f_agg="mean"
            )
        ).collect(),
        pl.DataFrame({"value": [0.0]}),
    )

    df = pl.DataFrame({"value": [0, 1, 0, 0, 0]})
    df_lazy = pl.LazyFrame({"value": [0, 1, 0, 0, 0]})
    assert_frame_equal(
        df.select(
            change_quantiles(pl.col("value"), ql=0, qh=1, isabs=True, f_agg="mean")
        ),
        pl.DataFrame({"value": [0.5]}),
    )
    assert_frame_equal(
        df_lazy.select(
            change_quantiles(pl.col("value"), ql=0, qh=1, isabs=True, f_agg="mean")
        ).collect(),
        pl.DataFrame({"value": [0.5]}),
    )
    assert_frame_equal(
        df.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=1, isabs=True, f_agg="mean")
        ),
        pl.DataFrame({"value": [0.5]}),
    )
    assert_frame_equal(
        df_lazy.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=1, isabs=True, f_agg="mean")
        ).collect(),
        pl.DataFrame({"value": [0.5]}),
    )
    assert_frame_equal(
        df.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=0.6, isabs=True, f_agg="mean")
        ),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df_lazy.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=0.6, isabs=True, f_agg="mean")
        ).collect(),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df.select(
            change_quantiles(pl.col("value"), ql=0, qh=1, isabs=False, f_agg="mean")
        ),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df_lazy.select(
            change_quantiles(pl.col("value"), ql=0, qh=1, isabs=False, f_agg="mean")
        ).collect(),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=1, isabs=False, f_agg="mean")
        ),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df_lazy.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=1, isabs=False, f_agg="mean")
        ).collect(),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=0.6, isabs=False, f_agg="mean")
        ),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df_lazy.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=0.6, isabs=False, f_agg="mean")
        ).collect(),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df.select(
            change_quantiles(pl.col("value"), ql=0, qh=1, isabs=True, f_agg="std")
        ),
        pl.DataFrame({"value": [0.5]}),
    )
    assert_frame_equal(
        df_lazy.select(
            change_quantiles(pl.col("value"), ql=0, qh=1, isabs=True, f_agg="std")
        ).collect(),
        pl.DataFrame({"value": [0.5]}),
    )

    df = pl.DataFrame({"value": [0, 1, -9, 0, 0]})
    df_lazy = pl.LazyFrame({"value": [0, 1, -9, 0, 0]})
    assert_frame_equal(
        df.select(
            change_quantiles(pl.col("value"), ql=0, qh=1, isabs=True, f_agg="mean")
        ),
        pl.DataFrame({"value": [5.0]}),
    )
    assert_frame_equal(
        df_lazy.select(
            change_quantiles(pl.col("value"), ql=0, qh=1, isabs=True, f_agg="mean")
        ).collect(),
        pl.DataFrame({"value": [5.0]}),
    )
    assert_frame_equal(
        df.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=1, isabs=True, f_agg="mean")
        ),
        pl.DataFrame({"value": [0.5]}),
    )
    assert_frame_equal(
        df_lazy.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=1, isabs=True, f_agg="mean")
        ).collect(),
        pl.DataFrame({"value": [0.5]}),
    )
    assert_frame_equal(
        df.select(
            change_quantiles(pl.col("value"), ql=0, qh=1, isabs=False, f_agg="mean")
        ),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df_lazy.select(
            change_quantiles(pl.col("value"), ql=0, qh=1, isabs=False, f_agg="mean")
        ).collect(),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=1, isabs=False, f_agg="mean")
        ),
        pl.DataFrame({"value": [0.5]}),
    )
    assert_frame_equal(
        df_lazy.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=1, isabs=False, f_agg="mean")
        ).collect(),
        pl.DataFrame({"value": [0.5]}),
    )

    df = pl.DataFrame({"value": [0, 1, -9, 0, 0, 1, 0]})
    df_lazy = pl.LazyFrame({"value": [0, 1, -9, 0, 0, 1, 0]})
    assert_frame_equal(
        df.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=1, isabs=True, f_agg="mean")
        ),
        pl.DataFrame({"value": [0.75]}),
    )
    assert_frame_equal(
        df_lazy.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=1, isabs=True, f_agg="mean")
        ).collect(),
        pl.DataFrame({"value": [0.75]}),
    )
    assert_frame_equal(
        df.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=1, isabs=False, f_agg="mean")
        ),
        pl.DataFrame({"value": [0.25]}),
    )
    assert_frame_equal(
        df_lazy.select(
            change_quantiles(pl.col("value"), ql=0.1, qh=1, isabs=False, f_agg="mean")
        ).collect(),
        pl.DataFrame({"value": [0.25]}),
    )

    df = pl.DataFrame({"value": [0, 1, 0, 1, 0]})
    df_lazy = pl.LazyFrame({"value": [0, 1, 0, 1, 0]})
    assert_frame_equal(
        df.select(
            change_quantiles(pl.col("value"), ql=0, qh=1, isabs=False, f_agg="std")
        ),
        pl.DataFrame({"value": [1.0]}),
    )
    assert_frame_equal(
        df_lazy.select(
            change_quantiles(pl.col("value"), ql=0, qh=1, isabs=False, f_agg="std")
        ).collect(),
        pl.DataFrame({"value": [1.0]}),
    )


def test_mean_abs_change():
    df = pl.DataFrame({"value": [-2, 2, 5]})
    df_lazy = pl.LazyFrame({"value": [-2, 2, 5]})
    assert_frame_equal(
        df.select(mean_abs_change(pl.col("value"))), pl.DataFrame({"value": 3.5})
    )
    assert_frame_equal(
        df_lazy.select(mean_abs_change(pl.col("value"))).collect(),
        pl.DataFrame({"value": 3.5}),
    )
    df = pl.DataFrame({"value": [1, 2, -1]})
    df_lazy = pl.LazyFrame({"value": [1, 2, -1]})
    assert_frame_equal(
        df_lazy.select(mean_abs_change(pl.col("value"))).collect(),
        pl.DataFrame({"value": [2.0]}),
    )


def test_mean_change():
    df = pl.DataFrame({"value": [-2, 2, 5]})
    df_lazy = pl.LazyFrame({"value": [-2, 2, 5]})
    assert_frame_equal(
        df.select(mean_change(pl.col("value"))), pl.DataFrame({"value": [3.5]})
    )
    assert_frame_equal(
        df_lazy.select(mean_change(pl.col("value"))).collect(),
        pl.DataFrame({"value": [3.5]}),
    )
    df = pl.DataFrame({"value": [1, 2, -1]})
    df_lazy = pl.LazyFrame({"value": [1, 2, -1]})
    assert_frame_equal(
        df.select(mean_change(pl.col("value"))), pl.DataFrame({"value": [-1.0]})
    )
    assert_frame_equal(
        df_lazy.select(mean_change(pl.col("value"))).collect(),
        pl.DataFrame({"value": [-1.0]}),
    )
    df = pl.DataFrame({"value": [10, 20]})
    df_lazy = pl.LazyFrame({"value": [10, 20]})
    assert_frame_equal(
        df.select(mean_change(pl.col("value"))), pl.DataFrame({"value": [10.0]})
    )
    assert_frame_equal(
        df_lazy.select(mean_change(pl.col("value"))).collect(),
        pl.DataFrame({"value": [10.0]}),
    )
    df = pl.DataFrame({"value": [1]})
    df_lazy = pl.LazyFrame({"value": [1]})
    assert_frame_equal(
        df.select(mean_change(pl.col("value"))),
        pl.DataFrame({"value": [None]}, schema={"value": pl.Float64}),
    )
    assert_frame_equal(
        df_lazy.select(mean_change(pl.col("value"))).collect(),
        pl.DataFrame({"value": [None]}, schema={"value": pl.Float64}),
    )
    df = pl.DataFrame({"value": []})
    df_lazy = pl.LazyFrame({"value": []})
    assert_frame_equal(
        df.select(mean_change(pl.col("value"))), pl.DataFrame({"value": [None]})
    )
    assert_frame_equal(
        df_lazy.select(mean_change(pl.col("value"))).collect(),
        pl.DataFrame({"value": [None]}),
    )


def test_number_crossing_m():
    df = pl.DataFrame({"value": [10, -10, 10, -10]})
    df_lazy = pl.LazyFrame({"value": [10, -10, 10, -10]})
    assert_frame_equal(
        df.select(
            number_crossing_m(pl.col("value"), 0.0),
        ),
        pl.DataFrame({"value": [3]}, schema={"value": pl.UInt32}),
    )
    assert_frame_equal(
        df_lazy.select(
            number_crossing_m(pl.col("value"), 0.0),
        ).collect(),
        pl.DataFrame({"value": [3]}, schema={"value": pl.UInt32}),
    )
    assert_frame_equal(
        df.select(
            number_crossing_m(pl.col("value"), 10.0),
        ),
        pl.DataFrame({"value": [0]}, schema={"value": pl.UInt32}),
    )
    assert_frame_equal(
        df_lazy.select(
            number_crossing_m(pl.col("value"), 10.0),
        ).collect(),
        pl.DataFrame({"value": [0]}, schema={"value": pl.UInt32}),
    )
    df = pl.DataFrame({"value": [10, 20, 20, 30]})
    df_lazy = pl.LazyFrame({"value": [10, 20, 20, 30]})
    assert_frame_equal(
        df.select(
            number_crossing_m(pl.col("value"), 0.0),
        ),
        pl.DataFrame({"value": [0]}, schema={"value": pl.UInt32}),
    )
    assert_frame_equal(
        df_lazy.select(
            number_crossing_m(pl.col("value"), 0.0),
        ).collect(),
        pl.DataFrame({"value": [0]}, schema={"value": pl.UInt32}),
    )
    assert_frame_equal(
        df.select(
            number_crossing_m(pl.col("value"), 15.0),
        ),
        pl.DataFrame({"value": [1]}, schema={"value": pl.UInt32}),
    )
    assert_frame_equal(
        df_lazy.select(
            number_crossing_m(pl.col("value"), 15.0),
        ).collect(),
        pl.DataFrame({"value": [1]}, schema={"value": pl.UInt32}),
    )


def test_var_larger_than_std():
    df = pl.DataFrame({"value": [-1, -1, 1, 1, 1]})
    df_lazy = pl.LazyFrame({"value": [-1, -1, 1, 1, 1]})
    assert_frame_equal(
        df.select(var_greater_than_std(pl.col("value"))),
        pl.DataFrame({"value": [False]}),
    )
    assert_frame_equal(
        df_lazy.select(var_greater_than_std(pl.col("value"))).collect(),
        pl.DataFrame({"value": [False]}),
    )
    df = pl.DataFrame({"value": [-1, -1, 1, 1, 2]})
    df_lazy = pl.LazyFrame({"value": [-1, -1, 1, 1, 2]})
    assert_frame_equal(
        df_lazy.select(var_greater_than_std(pl.col("value"))).collect(),
        pl.DataFrame({"value": [True]}),
    )


def test_first_location_of_maximum():
    df = pl.DataFrame({"value": [1, 2, 1, 2, 1]})
    df_lazy = pl.LazyFrame({"value": [1, 2, 1, 2, 1]})
    assert_frame_equal(
        df.select(first_location_of_maximum(pl.col("value"))),
        pl.DataFrame({"value": [0.2]}),
    )
    assert_frame_equal(
        df_lazy.select(first_location_of_maximum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [0.2]}),
    )
    df = pl.DataFrame({"value": [1, 2, 1, 1, 1]})
    df_lazy = pl.LazyFrame({"value": [1, 2, 1, 1, 1]})
    assert_frame_equal(
        df.select(first_location_of_maximum(pl.col("value"))),
        pl.DataFrame({"value": [0.2]}),
    )
    assert_frame_equal(
        df_lazy.select(first_location_of_maximum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [0.2]}),
    )
    df = pl.DataFrame({"value": [2, 1, 1, 1, 1]})
    df_lazy = pl.LazyFrame({"value": [2, 1, 1, 1, 1]})
    assert_frame_equal(
        df.select(first_location_of_maximum(pl.col("value"))),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df_lazy.select(first_location_of_maximum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [0.0]}),
    )
    df = pl.DataFrame({"value": [1, 1, 1, 1, 1]})
    df_lazy = pl.LazyFrame({"value": [1, 1, 1, 1, 1]})
    assert_frame_equal(
        df.select(first_location_of_maximum(pl.col("value"))),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df_lazy.select(first_location_of_maximum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [0.0]}),
    )
    df = pl.DataFrame({"value": [1]})
    df_lazy = pl.LazyFrame({"value": [1]})
    assert_frame_equal(
        df.select(first_location_of_maximum(pl.col("value"))),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df_lazy.select(first_location_of_maximum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [0.0]}),
    )
    df = pl.DataFrame({"value": []})
    df_lazy = pl.LazyFrame({"value": []})
    assert_frame_equal(
        df.select(first_location_of_maximum(pl.col("value"))),
        pl.DataFrame({"value": [None]}, schema={"value": pl.Float64}),
    )
    assert_frame_equal(
        df_lazy.select(first_location_of_maximum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [None]}, schema={"value": pl.Float64}),
    )


def test_last_location_of_maximum():
    df = pl.DataFrame({"value": [1, 2, 1, 2, 1]})
    df_lazy = pl.LazyFrame({"value": [1, 2, 1, 2, 1]})
    assert_frame_equal(
        df.select(last_location_of_maximum(pl.col("value"))),
        pl.DataFrame({"value": [0.8]}),
    )
    assert_frame_equal(
        df_lazy.select(last_location_of_maximum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [0.8]}),
    )

    df = pl.DataFrame({"value": [1, 2, 1, 1, 2]})
    df_lazy = pl.LazyFrame({"value": [1, 2, 1, 1, 2]})
    assert_frame_equal(
        df.select(last_location_of_maximum(pl.col("value"))),
        pl.DataFrame({"value": [1.0]}),
    )
    assert_frame_equal(
        df_lazy.select(last_location_of_maximum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [1.0]}),
    )

    df = pl.DataFrame({"value": [2, 1, 1, 1, 1]})
    df_lazy = pl.LazyFrame({"value": [2, 1, 1, 1, 1]})
    assert_frame_equal(
        df.select(last_location_of_maximum(pl.col("value"))),
        pl.DataFrame({"value": [0.2]}),
    )
    assert_frame_equal(
        df_lazy.select(last_location_of_maximum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [0.2]}),
    )

    df = pl.DataFrame({"value": [1, 1, 1, 1, 1]})
    df_lazy = pl.LazyFrame({"value": [1, 1, 1, 1, 1]})
    assert_frame_equal(
        df.select(last_location_of_maximum(pl.col("value"))),
        pl.DataFrame({"value": [1.0]}),
    )
    assert_frame_equal(
        df_lazy.select(last_location_of_maximum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [1.0]}),
    )

    df = pl.DataFrame({"value": [1]})
    df_lazy = pl.LazyFrame({"value": [1]})
    assert_frame_equal(
        df.select(last_location_of_maximum(pl.col("value"))),
        pl.DataFrame({"value": [1.0]}),
    )
    assert_frame_equal(
        df_lazy.select(last_location_of_maximum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [1.0]}),
    )

    df = pl.DataFrame({"value": []})
    df_lazy = pl.LazyFrame({"value": []})
    assert_frame_equal(
        df.select(last_location_of_maximum(pl.col("value"))),
        pl.DataFrame({"value": [None]}, schema={"value": pl.Float64}),
    )
    assert_frame_equal(
        df_lazy.select(last_location_of_maximum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [None]}, schema={"value": pl.Float64}),
    )


def test_last_location_of_minimum():
    df = pl.DataFrame({"value": [1, 2, 1, 2, 1]})
    df_lazy = pl.LazyFrame({"value": [1, 2, 1, 2, 1]})
    assert_frame_equal(
        df.select(last_location_of_minimum(pl.col("value"))),
        pl.DataFrame({"value": [1.0]}),
    )
    assert_frame_equal(
        df_lazy.select(last_location_of_minimum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [1.0]}),
    )

    df = pl.DataFrame({"value": [1, 2, 1, 2, 2]})
    df_lazy = pl.LazyFrame({"value": [1, 2, 1, 2, 2]})
    assert_frame_equal(
        df.select(last_location_of_minimum(pl.col("value"))),
        pl.DataFrame({"value": [0.6]}),
    )
    assert_frame_equal(
        df_lazy.select(last_location_of_minimum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [0.6]}),
    )

    df = pl.DataFrame({"value": [2, 1, 1, 1, 2]})
    df_lazy = pl.LazyFrame({"value": [2, 1, 1, 1, 2]})
    assert_frame_equal(
        df.select(last_location_of_minimum(pl.col("value"))),
        pl.DataFrame({"value": [0.8]}),
    )
    assert_frame_equal(
        df_lazy.select(last_location_of_minimum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [0.8]}),
    )

    df = pl.DataFrame({"value": [1, 1, 1, 1, 1]})
    df_lazy = pl.LazyFrame({"value": [1, 1, 1, 1, 1]})
    assert_frame_equal(
        df.select(last_location_of_minimum(pl.col("value"))),
        pl.DataFrame({"value": [1.0]}),
    )
    assert_frame_equal(
        df_lazy.select(last_location_of_minimum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [1.0]}),
    )

    df = pl.DataFrame({"value": [1]})
    df_lazy = pl.LazyFrame({"value": [1]})
    assert_frame_equal(
        df.select(last_location_of_minimum(pl.col("value"))),
        pl.DataFrame({"value": [1.0]}),
    )
    assert_frame_equal(
        df_lazy.select(last_location_of_minimum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [1.0]}),
    )

    df = pl.DataFrame({"value": []})
    df_lazy = pl.LazyFrame({"value": []})
    assert_frame_equal(
        df.select(last_location_of_minimum(pl.col("value"))),
        pl.DataFrame({"value": [None]}, schema={"value": pl.Float64}),
    )
    assert_frame_equal(
        df_lazy.select(last_location_of_minimum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [None]}, schema={"value": pl.Float64}),
    )


def test_first_location_of_minimum():
    df = pl.DataFrame({"value": [1, 2, 1, 2, 1]})
    df_lazy = pl.LazyFrame({"value": [1, 2, 1, 2, 1]})
    assert_frame_equal(
        df.select(first_location_of_minimum(pl.col("value"))),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df_lazy.select(first_location_of_minimum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [0.0]}),
    )

    df = pl.DataFrame({"value": [2, 2, 1, 2, 2]})
    df_lazy = pl.LazyFrame({"value": [2, 2, 1, 2, 2]})
    assert_frame_equal(
        df.select(first_location_of_minimum(pl.col("value"))),
        pl.DataFrame({"value": [0.4]}),
    )
    assert_frame_equal(
        df_lazy.select(first_location_of_minimum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [0.4]}),
    )

    df = pl.DataFrame({"value": [2, 1, 1, 1, 2]})
    df_lazy = pl.LazyFrame({"value": [2, 1, 1, 1, 2]})
    assert_frame_equal(
        df.select(first_location_of_minimum(pl.col("value"))),
        pl.DataFrame({"value": [0.2]}),
    )
    assert_frame_equal(
        df_lazy.select(first_location_of_minimum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [0.2]}),
    )

    df = pl.DataFrame({"value": [1, 1, 1, 1, 1]})
    df_lazy = pl.LazyFrame({"value": [1, 1, 1, 1, 1]})
    assert_frame_equal(
        df.select(first_location_of_minimum(pl.col("value"))),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df_lazy.select(first_location_of_minimum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [0.0]}),
    )

    df = pl.DataFrame({"value": [1]})
    df_lazy = pl.LazyFrame({"value": [1]})
    assert_frame_equal(
        df.select(first_location_of_minimum(pl.col("value"))),
        pl.DataFrame({"value": [0.0]}),
    )
    assert_frame_equal(
        df_lazy.select(first_location_of_minimum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [0.0]}),
    )

    df = pl.DataFrame({"value": []})
    df_lazy = pl.LazyFrame({"value": []})
    assert_frame_equal(
        df.select(first_location_of_minimum(pl.col("value"))),
        pl.DataFrame({"value": [None]}, schema={"value": pl.Float64}),
    )
    assert_frame_equal(
        df_lazy.select(first_location_of_minimum(pl.col("value"))).collect(),
        pl.DataFrame({"value": [None]}, schema={"value": pl.Float64}),
    )
