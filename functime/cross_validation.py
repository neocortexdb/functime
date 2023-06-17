from typing import List, Optional

import numpy as np
import polars as pl


def train_test_split(test_size: int):
    """Return a time-ordered train set and test set given `test_size`.

    Parameters
    ----------
    test_size : int
        Number of test samples.

    Returns
    -------
    splitter : Callable[pl.LazyFrame, pl.LazyFrame]
        Function that takes a panel LazyFrame and returns a LazyFrame of train / test splits.
    """

    def split(X: pl.LazyFrame) -> pl.LazyFrame:
        X = X.lazy()  # Defensive
        entity_col = X.columns[0]
        train_split = (
            X.groupby(entity_col)
            .agg(pl.all().slice(0, pl.count() - test_size))
            .explode(pl.all().exclude(entity_col))
        )
        test_split = (
            X.groupby(entity_col)
            .agg(pl.all().slice(-1 * test_size, test_size))
            .explode(pl.all().exclude(entity_col))
        )
        return train_split, test_split

    return split


def _window_split(
    X: pl.LazyFrame,
    test_size: int,
    n_splits: int,
    step_size: int,
    window_size: Optional[int] = None,
) -> List[pl.LazyFrame]:
    X = X.lazy()  # Defensive
    backward_steps = np.arange(1, n_splits) * step_size + test_size
    cutoffs = np.flip(np.concatenate([np.array([test_size]), backward_steps]))
    entity_col = X.columns[0]
    if window_size:
        # Sliding window CV
        train_exprs = [
            pl.all().slice(pl.count() - cutoff - window_size, window_size)
            for cutoff in cutoffs
        ]
    else:
        # Expanding window CV
        train_exprs = [pl.all().slice(0, pl.count() - cutoff) for cutoff in cutoffs]

    test_exprs = [pl.all().slice(-cutoffs[i], test_size) for i in range(n_splits)]
    train_test_exprs = zip(train_exprs, test_exprs)
    splits = {}
    for i, train_test_expr in enumerate(train_test_exprs):
        train_expr, test_expr = train_test_expr
        train_split = (
            X.groupby(entity_col).agg(train_expr).explode(pl.all().exclude(entity_col))
        )
        test_split = (
            X.groupby(entity_col).agg(test_expr).explode(pl.all().exclude(entity_col))
        )
        splits[i] = train_split, test_split
    return splits


def expanding_window_split(
    test_size: int,
    n_splits: int = 5,
    step_size: int = 1,
):
    """Return train/test splits using expanding window splitter.

    Split time series repeatedly into an growing training set and a fixed-size test set.
    For example, given `test_size = 3`, `n_splits = 5` and `step_size = 1`,
    the train `o`s and test `x`s folds can be visualized as:

    ```
    | o o o x x x - - - - |
    | o o o o x x x - - - |
    | o o o o o x x x - - |
    | o o o o o o x x x - |
    | o o o o o o o x x x |
    ```

    Parameters
    ----------
    test_size : int
        Number of test samples for each split.
    n_splits : int, default=5
        Number of splits.
    step_size : int, default=1
        Step size between windows.

    Returns
    -------
    splitter : Callable[pl.LazyFrame, pl.LazyFrame]
        Function that takes a panel LazyFrame and Dict of (train, test) splits, where
        the key represents the split number (1,2,...,n_splits) and the value is a tuple of LazyFrames.
    """

    def split(X: pl.LazyFrame) -> pl.LazyFrame:
        return _window_split(X, test_size, n_splits, step_size)

    return split


def sliding_window_split(
    test_size: int,
    n_splits: int = 5,
    step_size: int = 1,
    window_size: int = 10,
):
    """Return train/test splits using sliding window splitter.
    Split time series repeatedly into a fixed-length training and test set.
    For example, given `test_size = 3`, `n_splits = 5`, `step_size = 1` and `window_size=5`
    the train `o`s and test `x`s folds can be visualized as:

    ```
    | o o o o o x x x - - - - |
    | - o o o o o x x x - - - |
    | - - o o o o o x x x - - |
    | - - - o o o o o x x x - |
    | - - - - o o o o o x x x |
    ```

    Parameters
    ----------
    test_size : int
        Number of test samples for each split.
    n_splits : int, default=5
        Number of splits.
    step_size : int, default=1
        Step size between windows.
    window_size: int, default=10
        Window size for training.

    Returns
    -------
    splitter : Callable[pl.LazyFrame, pl.LazyFrame]
        Function that takes a panel LazyFrame and Dict of (train, test) splits, where
        the key represents the split number (1,2,...,n_splits) and the value is a tuple of LazyFrames.
    """

    def split(X: pl.LazyFrame) -> pl.LazyFrame:
        return _window_split(X, test_size, n_splits, step_size, window_size)

    return split
