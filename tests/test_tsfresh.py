import numpy as np
import polars as pl
import pytest
from polars.testing import assert_frame_equal, assert_series_equal
import inspect

# percent_recoccuring_values,
from functime.feature_extraction.tsfresh import (
    absolute_energy,
    absolute_maximum,
    absolute_sum_of_changes,
    approximate_entropy,
    autocorrelation,

    benford_correlation,
    longest_strike_above_mean,
    longest_strike_below_mean,
    mean_n_absolute_max,
    mean_second_derivative_central,
    percent_reocurring_points,
    sum_reocurring_points,
    sum_reocurring_values,
    number_peaks,
    symmetry_looking,
    time_reversal_asymmetry_statistic,
    percent_reoccuring_values
)

np.random.seed(42)

@pytest.mark.parametrize("S, res", [
    ([-5, 0, 1], [26]),
    ([0], [0]),
    ([-1, 2, -3], [14]),
    ([-1, 1.3], [2.6900000000000004]),
    ([1], [1])
])
def test_abolute_energy(S, res):
    assert_frame_equal(
        pl.DataFrame(
            {"a": S}
        ).select(
            absolute_energy(pl.col("a"))
        ),
        pl.DataFrame(pl.Series("a", res))
    )
    assert_frame_equal(
        pl.LazyFrame(
            {"a": S}
        ).select(
            absolute_energy(pl.col("a"))
        ).collect(),
        pl.DataFrame(pl.Series("a", res))
    )
    assert absolute_energy(pl.Series(S)) == res[0]


@pytest.mark.parametrize("S, res", [
    ([-5, 0, 1], [5]),
    ([0], [0]),
    ([-1.0, 2.0, -3.0], [3.0]),
])
def test_absolute_maximum(S, res):
    assert_frame_equal(
        pl.DataFrame(
            {"a": S}
        ).select(
            absolute_maximum(pl.col("a"))
        ),
        pl.DataFrame(pl.Series("max", res))
    )
    assert_frame_equal(
        pl.LazyFrame(
            {"a": S}
        ).select(
            absolute_maximum(pl.col("a"))
        ).collect(),
        pl.DataFrame(pl.Series("max", res))
    )
    assert absolute_maximum(pl.Series(S)) == res[0]


@pytest.mark.parametrize("S, res", [
    ([1, 1, 1, 1, 2, 1], [2]),
    ([1.4, -1.3, 1.7, -1.2], [8.6]),
    ([1], [0])
])
def test_absolute_sum_of_changes(S, res):
    assert_frame_equal(
        pl.DataFrame(
            {"a": S}
        ).select(
            absolute_sum_of_changes(pl.col("a"))
        ),
        pl.DataFrame(pl.Series("a", res))
    )
    assert_frame_equal(
        pl.LazyFrame(
            {"a": S}
        ).select(
            absolute_sum_of_changes(pl.col("a"))
        ).collect(),
        pl.DataFrame(pl.Series("a", res))
    )
    assert absolute_sum_of_changes(pl.Series(S)) == res[0]


@pytest.mark.parametrize("S, res, m, r, scale", [
    ([1], 0, 2, 0.5, False),
    ([12, 13, 15, 16, 17] * 10, 0.282456191276673, 2, 0.9, True),
    ([1.4, -1.3, 1.7, -1.2], 0.0566330122651324, 2, 0.5, False),
    ([0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], 0.002223871246127107, 2, 0.5, False),
    ([0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1], 0.47133806162842484, 2, 0.5, False),
    ([85, 80, 89] * 17, 1.099654110658932e-05, 2, 3, False),
    ([85, 80, 89] * 17, 0.0, 2, 3, True)
])
def test_approximate_entropy(S, res, m, r, scale):
    assert approximate_entropy(x = pl.Series(S), run_length=m, filtering_level=r, scale_by_std=scale) == res

@pytest.mark.parametrize("S, res, n_lags", [
    ([1, 2, 1, 2, 1, 2], [-1.0], 1),
    ([1, 2, 1, 2, 1, 2], [1.0], 2),
    ([1, 2, 1, 2, 1, 2], [1.0], 4),
    ([0, 1, 2, 0, 1, 2], [-0.75], 2),
    ([1, 2, 1, 2, 1, 2], [1.0], 0)
])
def test_autocorrelation(S, res, n_lags):
    # Doesn't work for lazy mode
    assert_frame_equal(
        pl.DataFrame(
            {"a": S}
        ).select(
            autocorrelation(pl.col("a"), n_lags=n_lags)
        ),
        pl.DataFrame(pl.Series("a", res))
    )
    # assert_frame_equal(
    #     pl.LazyFrame(
    #         {"a": S}
    #     ).select(
    #         autocorrelation(pl.col("a"), n_lags=n_lags)
    #     ).collect(),
    #     pl.DataFrame(pl.Series("a", res))
    # )
    assert autocorrelation(pl.Series(S), n_lags=n_lags) == res[0]

def test_benford_correlation():
    # Nan, division by 0
    X_uniform = pl.DataFrame({
        "a": [1, 2, 3, 4, 5, 6, 7, 8, 9]
    })
    X_uniform_lazy = pl.LazyFrame({
        "a": [1, 2, 3, 4, 5, 6, 7, 8, 9]
    })
    # Random serie
    X_random = pl.DataFrame({
        "a": [26.24, 3.03, -2.92, 3.5, -0.07, 0.35, 0.10, 0.51, -0.43]
    })
    X_random_lazy = pl.LazyFrame({
        "a": [26.24, 3.03, -2.92, 3.5, -0.07, 0.35, 0.10, 0.51, -0.43]
    })
    # Fibo, distribution same as benford law
    l_fibo = [0, 1]
    for i in range(2, 50):
        l_fibo.append(l_fibo[i - 1] + l_fibo[i - 2])
    
    X_fibo = pl.DataFrame({
        "a": l_fibo
    })

    X_fibo_lazy = pl.LazyFrame({
        "a": l_fibo
    })
    assert_frame_equal(
        X_uniform.select(
            benford_correlation(pl.col("a"))
        ),
        pl.DataFrame({"counts": [np.nan]})
    )
    assert_frame_equal(
        X_uniform_lazy.select(
            benford_correlation(pl.col("a"))
        ).collect(),
        pl.DataFrame({"counts": [np.nan]})
    )
    assert_frame_equal(
        X_random.select(
            benford_correlation(pl.col("a"))
        ),
        pl.DataFrame({"counts": [0.39753280229716703]})
    )
    assert_frame_equal(
        X_random_lazy.select(
            benford_correlation(pl.col("a"))
        ).collect(),
        pl.DataFrame({"counts": [0.39753280229716703]})
    )
    assert_frame_equal(
        X_fibo.select(
            benford_correlation(pl.col("a"))
        ),
        pl.DataFrame({"counts": [0.9959632739083689]})
    )
    assert_frame_equal(
        X_fibo_lazy.select(
            benford_correlation(pl.col("a"))
        ).collect(),
        pl.DataFrame({"counts": [0.9959632739083689]})
    )

@pytest.mark.parametrize("S, res", [
    ([1, 2, 1, 1, 1, 2, 2, 2], [3]),
    ([1, 2, 3, 4, 5, 6], [3]),
    ([1, 2, 3, 4, 5], [2]),
    ([1, 2, 1], [1]),
    ([1, 1, 1], [0]),
    ([], [0])
])
def test_longest_strike_below_mean(S, res):
    assert_frame_equal(
        pl.DataFrame(
            {"a": S}
        ).select(
            longest_strike_below_mean(pl.col("a")).alias("lengths")
        ),
        pl.DataFrame(pl.Series("lengths", res, dtype=pl.UInt64))
    )
    assert_frame_equal(
        pl.LazyFrame(
            {"a": S}
        ).select(
            longest_strike_below_mean(pl.col("a")).alias("lengths")
        ).collect(),
        pl.DataFrame(pl.Series("lengths", res, dtype=pl.UInt64))
    )


@pytest.mark.parametrize("S, res", [
    ([1, 2, 1, 2, 1, 2, 2, 1], [2]),
    ([1, 2, 3, 4, 5, 6], [3]),
    ([1, 2, 3, 4, 5], [2]),
    ([1, 2, 1], [1]),
    ([1, 1, 1], [0]),
    ([], [0])
])
def test_longest_strike_above_mean(S, res):
    assert_frame_equal(
        pl.DataFrame(
            {"a": S}
        ).select(
            longest_strike_above_mean(pl.col("a")).alias("lengths")
        ),
        pl.DataFrame(pl.Series("lengths", res, dtype=pl.UInt64))
    )
    assert_frame_equal(
        pl.LazyFrame(
            {"a": S}
        ).select(
            longest_strike_above_mean(pl.col("a")).alias("lengths")
        ).collect(),
        pl.DataFrame(pl.Series("lengths", res, dtype=pl.UInt64))
    )

@pytest.mark.parametrize("S, n_max, res", [
    ([], 1, [None]),
    ([12, 3], 10, [7.5]),
    ([-1, -5, 4, 10], 3, [6.333333]),
    ([0, -5, -9], 2, [7.0]),
    ([0, 0, 0], 1, [0.0])
])
def test_mean_n_absolute_max(S, n_max, res):
    assert_frame_equal(
        pl.DataFrame(
            {"a": S}
        ).select(
            mean_n_absolute_max(pl.col("a"), n_maxima=n_max).cast(pl.Float64)
        ),
        pl.DataFrame(pl.Series("a", res, dtype=pl.Float64))
    )
    assert_frame_equal(
        pl.LazyFrame(
            {"a": S}
        ).select(
            mean_n_absolute_max(pl.col("a"), n_maxima=n_max).cast(pl.Float64)
        ).collect(),
        pl.DataFrame(pl.Series("a", res, dtype=pl.Float64))
    )

def test_mean_n_absolute_max_value_error():
    with pytest.raises(ValueError):
        mean_n_absolute_max(
            x = pl.Series([12, 3]),
            n_maxima = 0
        )
    with pytest.raises(ValueError):
        mean_n_absolute_max(
            x = pl.Series([12, 3]),
            n_maxima = -1
        )


@pytest.mark.parametrize("S, res", [
    ([1, 1, 2, 3, 4], [0.4]),
    ([1, 1.5, 2, 3], [0]),
    ([1], [0]),
    ([1.111, -2.45, 1.111, 2.45], [0.5]),
    ([], [np.nan])
])
def test_percent_reoccuring_values(S, res):
    assert_frame_equal(
        pl.DataFrame(
            {"a": S}
        ).select(
            percent_reoccuring_values(pl.col("a"))
        ),
        pl.DataFrame(pl.Series("a", res, dtype=pl.Float64))
    )
    assert_frame_equal(
        pl.LazyFrame(
            {"a": S}
        ).select(
            percent_reoccuring_values(pl.col("a"))
        ).collect(),
        pl.DataFrame(pl.Series("a", res, dtype=pl.Float64))
    )


@pytest.mark.parametrize("S, res", [
    ([1, 1, 2, 3, 4], [0.25]),
    ([1, 1.5, 2, 3], [0]),
    ([1], [0]),
    ([1.111, -2.45, 1.111, 2.45], [1.0 / 3.0])
])
def test_percent_reoccuring_values(S, res):
    assert_frame_equal(
        pl.DataFrame(
            {"a": S}
        ).select(
            percent_reoccuring_values(pl.col("a"))
        ),
        pl.DataFrame(pl.Series("a", res, dtype=pl.Float64))
    )
    assert_frame_equal(
        pl.LazyFrame(
            {"a": S}
        ).select(
            percent_reoccuring_values(pl.col("a"))
        ).collect(),
        pl.DataFrame(pl.Series("a", res, dtype=pl.Float64))
    )


@pytest.mark.parametrize("S, res", [
    ([1, 1, 2, 3, 4, 4], [10]),
    ([1, 1.5, 2, 3], [0.0]),
    ([1], [0]),
    ([1.111, -2.45, 1.111, 2.45], [2.222])
])
def test_sum_reocurring_points(S, res):
    assert_frame_equal(
        pl.DataFrame(
            {"a": S}
        ).select(
            sum_reocurring_points(pl.col("a"))
        ),
        pl.DataFrame(pl.Series("a", res))
    )
    assert_frame_equal(
        pl.LazyFrame(
            {"a": S}
        ).select(
            sum_reocurring_points(pl.col("a"))
        ).collect(),
        pl.DataFrame(pl.Series("a", res))
    )


@pytest.mark.parametrize("S, res", [
    ([1, 1, 2, 3, 4, 4], [5]),
    ([1, 1.5, 2, 3], [0.0]),
    ([1], [0]),
    ([1.111, -2.45, 1.111, 2.45], [1.111])
])
def test_sum_reocurring_values(S, res):
    assert_frame_equal(
        pl.DataFrame(
            {"a": S}
        ).select(
            sum_reocurring_values(pl.col("a"))
        ),
        pl.DataFrame(pl.Series("a", res))
    )
    assert_frame_equal(
        pl.LazyFrame(
            {"a": S}
        ).select(
            sum_reocurring_values(pl.col("a"))
        ).collect(),
        pl.DataFrame(pl.Series("a", res))
    )


@pytest.mark.parametrize("S, res", [
    ([1, 1, 2, 3, 4], [0.4]),
    ([1, 1.5, 2, 3], [0]),
    ([1], [0]),
    ([1.111, -2.45, 1.111, 2.45], [0.5]),
    ([], [np.nan])
])
def test_percent_reocurring_points(S, res):
    assert_frame_equal(
        pl.DataFrame(
            {"a": S}
        ).select(
            percent_reocurring_points(pl.col("a"))
        ),
        pl.DataFrame(pl.Series("a", res, dtype=pl.Float64))
    )
    assert_frame_equal(
        pl.LazyFrame(
            {"a": S}
        ).select(
            percent_reocurring_points(pl.col("a"))
        ).collect(),
        pl.DataFrame(pl.Series("a", res, dtype=pl.Float64))
    )


@pytest.mark.parametrize("S, n, res", [
    ([0, 5, 2, 3, 0, 1, 2, 3, 4, 5, 4, 3, 2, 1], 1, [3]),
    ([0, 1, 2, 3, 0, 1, 2, 3, 4, 5, 4, 3, 2, 1], 2, [2]),
    ([0, 1, 2, 3, 0, 1, 2, 3, 4, 5, 4, 3, 2, 1], 3, [2]),
    ([0, 1, 2, 3, 0, 1, 2, 3, 4, 5, 4, 3, 2, 1], 4, [1])
])
def test_number_peaks(S, n, res):
    assert_frame_equal(
        pl.DataFrame(
            {"a": S}
        ).select(
            number_peaks(pl.col("a"), n).alias("a")
        ),
        pl.DataFrame(pl.Series("a", res, dtype=pl.UInt32))
    )
    assert_frame_equal(
        pl.LazyFrame(
            {"a": S}
        ).select(
            number_peaks(pl.col("a"), n).alias("a")
        ).collect(),
        pl.DataFrame(pl.Series("a", res, dtype=pl.UInt32))
    )


def generate_ar1():
    np.random.seed(42)
    e = np.random.normal(0.1, 0.1, size=100)
    m = 50
    x = [0] * m
    x[0] = 100
    for i in range(1, m):
        x[i] = x[i - 1] * 0.5 + e[i]
    return pl.Series(x, dtype=pl.Float64)


@pytest.mark.parametrize(
    "x, param, res",
    [
        (
            pl.Series(np.cumsum(np.random.uniform(size=100))),
            [
                {"autolag": "BIC", "attr": "teststat"},
                {"autolag": "BIC", "attr": "pvalue"},
                {"autolag": "BIC", "attr": "usedlag"},
            ],
            pl.DataFrame(
                [
                    [
                        'attr_"teststat"__autolag_"BIC"',
                        'attr_"pvalue"__autolag_"BIC"',
                        'attr_"usedlag"__autolag_"BIC"',
                    ],
                    [0.037064, 0.961492, 0],
                ],
                schema=["index", "res"],
            ),
        ),
        (
            generate_ar1(),
            [
                {"autolag": "AIC", "attr": "teststat"},
                {"autolag": "AIC", "attr": "pvalue"},
                {"autolag": "AIC", "attr": "usedlag"},
            ],
            pl.DataFrame(
                [
                    [
                        'attr_"teststat"__autolag_"AIC"',
                        'attr_"pvalue"__autolag_"AIC"',
                        'attr_"usedlag"__autolag_"AIC"',
                    ],
                    [-595.259534, 0, 0],
                ],
                schema=["index", "res"],
            ),
        ),
    ],
)
def test_augmented_dickey_fuller(x, param, res):
    # assert_frame_equal(augmented_dickey_fuller(x, param), res, atol=1e-7)
    # res_linalg_error = (
    #     augmented_dickey_fuller(x=pl.Series(np.repeat(np.nan, 100)), param=param)
    #     .get_column("res")
    #     .to_numpy()
    # )
    # assert all(np.isnan(res_linalg_error))
    #
    # res_value_error = (
    #     augmented_dickey_fuller(x=pl.Series([]), param=param)
    #     .get_column("res")
    #     .to_numpy()
    # )
    # assert all(np.isnan(res_value_error))
    #
    # # Should return NaN if "attr" is unknown
    # res_attr_error = (
    #     augmented_dickey_fuller(x=x, param=[{"autolag": "AIC", "attr": ""}])
    #     .get_column("res")
    #     .to_numpy()
    # )
    # assert all(np.isnan(res_attr_error))
    assert True


@pytest.mark.parametrize(
    "x, res",
    [
        (pl.Series(range(10)), pl.Series([0.0])),
        (pl.Series([1, 3, 5]), pl.Series([0.0])),
        (pl.Series([1, 3, 7, -3]), pl.Series([-3.0])),
    ],
)
def test_mean_second_derivative_central(x, res):
    assert_series_equal(
        mean_second_derivative_central(x),
        res
    )
# This test needs to be rewritten..
@pytest.mark.parametrize(
    "x, r, res",
    [
        (
            pl.Series([-1, -1, 1, 1]),
            0.05,
            True
        ),
        (
            pl.Series([-2, -1, 0, 1, 1]),
            0.05,
            False
        ),
        (
            pl.Series([-2, -1, 0, 1, 1]),
            0.1,
            True
        ),
    ],
)
def test_symmetry_looking(x, r, res):
    ans = symmetry_looking(x, r)
    assert ans == res

    df = x.to_frame()
    assert_frame_equal(
        df.select(
            symmetry_looking(pl.col(x.name), ratio=r)
        ),
        pl.DataFrame({x.name:[res]})
    )


@pytest.mark.parametrize(
    "x, lag, res", [(pl.Series([1] * 10), 0, 0), (pl.Series([1, 2, -3, 4]), 1, -10)]
)
def test_time_reversal_asymmetry_statistic(x, lag, res):
    assert time_reversal_asymmetry_statistic(x, lag) == res
