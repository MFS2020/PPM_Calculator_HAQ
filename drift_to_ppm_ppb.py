"""Utility helpers for converting between clock drift and PPM/PPB errors."""

from datetime import datetime


def _now() -> datetime:
    """Return the current local datetime.

    A dedicated helper makes it straightforward to patch the current time in
    tests without needing to monkeypatch :func:`datetime.datetime.now`.
    """

    return datetime.now()


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


def ppm_ppb_to_drift(
    *, ppm: float | None = None, ppb: float | None = None, period_seconds: float = 86400.0
) -> float:
    """Convert PPM or PPB error into seconds of drift over ``period_seconds``.

    Parameters
    ----------
    ppm : float, optional
        The parts per million error. Exactly one of ``ppm`` or ``ppb`` must be provided.
    ppb : float, optional
        The parts per billion error. Exactly one of ``ppm`` or ``ppb`` must be provided.
    period_seconds : float
        The length of the measurement period, in seconds (default 86400 seconds = 24 hours).

    Returns
    -------
    float
        The drift, in seconds, over the given period.
    """

    if (ppm is None) == (ppb is None):
        raise ValueError("Provide exactly one of ppm or ppb.")

    if period_seconds <= 0:
        raise ValueError("period_seconds must be positive.")

    fractional_drift = (ppm / 1_000_000) if ppm is not None else (ppb / 1_000_000_000)
    drift_seconds = fractional_drift * period_seconds

    return drift_seconds


def print_current_time() -> None:
    """Print the current date and time down to the second."""

    now = _now()
    print(now.strftime("Current date and time: %Y-%m-%d %H:%M:%S"))


def print_current_date() -> None:
    """Print the current calendar date."""

    today = _now()
    print(today.strftime("Current date: %Y-%m-%d"))


def print_current_unix_time() -> None:
    """Print the current Unix time to the nearest second."""

    unix_time = int(_now().timestamp())
    print(f"Current Unix time: {unix_time}")


if __name__ == "__main__":
    # Example usage: 0.25 seconds drift over a day (86400 seconds)
    ppm, ppb = drift_to_ppm_ppb(0.25, 86400)
    print(f"Drift: +0.25 s/day => {ppm:.4f} PPM, {ppb:.4f} PPB")

    print()
    print("Enter a PPM or PPB value to estimate the daily drift (press Enter to skip a value).")
    ppm_input = input("PPM: ").strip()
    ppb_input = input("PPB: ").strip()

    special_commands = {
        "time": print_current_time,
        "date": print_current_date,
        "unix": print_current_unix_time,
    }

    handled_command = False
    for user_input in (ppm_input, ppb_input):
        command = user_input.lower()
        if command in special_commands:
            special_commands[command]()
            handled_command = True

    if handled_command:
        raise SystemExit(0)

    try:
        ppm_value = float(ppm_input) if ppm_input else None
        ppb_value = float(ppb_input) if ppb_input else None
    except ValueError:
        print("Error: Please enter numeric values for PPM/PPB.")
    else:
        try:
            drift = ppm_ppb_to_drift(ppm=ppm_value, ppb=ppb_value)
        except ValueError as exc:
            print(f"Error: {exc}")
        else:
            # Format drift output to four decimal places for consistency with PPM/PPB.
            print(f"Estimated drift over a day: {drift:+.6f} seconds")
