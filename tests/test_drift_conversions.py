import unittest

from drift_to_ppm_ppb import drift_to_ppm_ppb, ppm_ppb_to_drift


class DriftConversionTests(unittest.TestCase):
    def test_drift_to_ppm_ppb_symmetry(self):
        ppm, ppb = drift_to_ppm_ppb(0.25, 86400)
        self.assertAlmostEqual(ppm, 2.8935185185, places=7)
        self.assertAlmostEqual(ppb, 2893.5185185185, places=4)

    def test_ppm_ppb_to_drift_with_ppm(self):
        drift = ppm_ppb_to_drift(ppm=10.0, period_seconds=86400)
        self.assertAlmostEqual(drift, 0.864, places=6)

    def test_ppm_ppb_to_drift_with_ppb(self):
        drift = ppm_ppb_to_drift(ppb=10_000.0, period_seconds=60)
        self.assertAlmostEqual(drift, 0.0006, places=9)

    def test_ppm_ppb_to_drift_requires_one_argument(self):
        with self.assertRaises(ValueError):
            ppm_ppb_to_drift()
        with self.assertRaises(ValueError):
            ppm_ppb_to_drift(ppm=1.0, ppb=1_000.0)

    def test_invalid_period_raises(self):
        with self.assertRaises(ValueError):
            drift_to_ppm_ppb(0.1, 0)
        with self.assertRaises(ValueError):
            ppm_ppb_to_drift(ppm=1.0, period_seconds=0)


if __name__ == "__main__":
    unittest.main()
