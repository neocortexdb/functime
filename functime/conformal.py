from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Sequence

import polars as pl


def conformalize(
    *,
    y_pred: pl.DataFrame,
    y_preds: pl.DataFrame,
    y_resids: pl.DataFrame,
    alphas: Optional[Sequence[float]] = None,
) -> pl.DataFrame:
    """Compute prediction intervals using ensemble batch prediction intervals (ENBPI).

    Parameters
    ----------
    y_pred : pl.DataFrame | pl.LazyFrame
        The predicted values.
    y_preds : pl.DataFrame | pl.LazyFrame
        The predictions resulting from backtesting.
    y_resids : pl.DataFrame | pl.LazyFrame
        The backtesting residuals.
    alphas : Optional[Sequence[float]], optional
        The quantile levels to use for the prediction intervals. Defaults to (0.1, 0.9).
        Quantiles must be two values between 0 and 1 (exclusive).

    Returns
    -------
    pl.DataFrame
        The prediction intervals.
    """
    alphas = _validate_alphas(alphas)

    entity_col, time_col, target_col = y_pred.columns[:3]
    schema = y_pred.schema
    y_preds = pl.concat(
        [
            y_pred,
            y_preds.select(
                [
                    entity_col,
                    pl.col(time_col).cast(schema[time_col]),
                    pl.col(target_col).cast(schema[target_col]),
                ]
            ),
        ]
    )

    y_preds = y_preds.lazy()
    y_resids = y_resids.select(y_resids.columns[:3]).lazy()
    y_pred_quantiles = _compute_enbpi(
        y_preds=y_preds,
        y_resids=y_resids,
        alphas=alphas,
    )

    # Make alpha base 100
    y_pred_quantiles = y_pred_quantiles.with_columns(
        (pl.col("quantile") * 100).cast(pl.Int16)
    )

    return y_pred_quantiles


def _compute_enbpi(
    *,
    y_preds: pl.LazyFrame,
    y_resids: pl.LazyFrame,
    alphas: Sequence[float],
) -> pl.DataFrame:
    """Compute prediction intervals using ensemble batch prediction intervals (ENBPI)."""

    # 1. Group residuals by entity
    entity_col, time_col = y_preds.columns[:2]
    y_resids = y_resids.collect()

    # 2. Forecast future prediction intervals: use constant residual quantile
    schema = y_preds.schema
    y_pred_qnts = []
    for alpha in alphas:
        y_pred_qnt = y_preds.join(
            y_resids.group_by(entity_col)
            .agg(pl.col(y_resids.columns[-1]).quantile(alpha).alias("score"))
            .lazy(),
            how="left",
            on=entity_col,
        ).select(
            [
                pl.col(entity_col).cast(schema[entity_col]),
                pl.col(time_col).cast(schema[time_col]),
                pl.col(y_preds.columns[-1]) + pl.col("score"),
                pl.lit(alpha).alias("quantile"),
            ]
        )
        y_pred_qnts.append(y_pred_qnt)

    y_pred_qnts = pl.concat(y_pred_qnts).sort([entity_col, time_col]).collect()
    return y_pred_qnts


def _validate_alphas(alphas: Optional[Sequence[float]]) -> Sequence[float]:
    if alphas is None:
        return (0.1, 0.9)
    elif len(alphas) != 2:
        raise ValueError("alphas must be a list of length 2")
    elif not all(0 < alpha < 1 for alpha in alphas):
        raise ValueError("alphas must be between 0 and 1")
    return alphas
