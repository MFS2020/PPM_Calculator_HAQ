def drift_to_ppm_ppb(drift_seconds: float, period_seconds: float = 86400.0):
    """
    Convert time drift in seconds to parts per million (PPM) and parts per billion (PPB).

    Parameters
    ----------
    drift_seconds : float
        The amount of time, in seconds, that the watch has gained or lost.
        Positive values indicate the watch is fast; negative values indicate it is slow.
    period_seconds : float
        The length of the measurement period, in seconds (default 86400 seconds = 24 hours).

    Returns
    -------
    tuple
        A pair (ppm, ppb) where:
        - ppm: parts per million error as a float
        - ppb: parts per billion error as a float
    """
    if period_seconds <= 0:
        raise ValueError("period_seconds must be positive.")

    # Calculate the fraction of drift relative to the measurement period
    fractional_drift = drift_seconds / period_seconds

    # Convert fractional drift to PPM and PPB
    ppm = fractional_drift * 1_000_000
    ppb = fractional_drift * 1_000_000_000

    return ppm, ppb


if __name__ == "__main__":
    # Example usage: 0.25 seconds drift over a day (86400 seconds)
    ppm, ppb = drift_to_ppm_ppb(0.25, 86400)
    print(f"Drift: +0.25 s/day => {ppm:.3f} PPM, {ppb:.3f} PPB")
