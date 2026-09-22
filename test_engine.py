import unittest
from engine import DriftMonitor

class DriftTests(unittest.TestCase):
    def test_identical_distribution(self):
        m=DriftMonitor.fit(range(100))
        self.assertAlmostEqual(m.compare(range(100))['psi'],0)
    def test_shift_detected(self):
        m=DriftMonitor.fit(range(100))
        self.assertIn('distribution-shift',m.compare(range(1000,1100))['alerts'])
    def test_missingness_separate(self):
        m=DriftMonitor.fit(range(100))
        result=m.compare(list(range(100))+[None]*100)
        self.assertAlmostEqual(result['psi'],0)
        self.assertIn('missingness-increase',result['alerts'])
    def test_constant_reference_and_extreme_values(self):
        m=DriftMonitor.fit([5]*100)
        self.assertEqual(m.compare([5]*100)['psi'],0)
        self.assertGreater(m.compare([-100]*100)['psi'],0)
    def test_small_batch_does_not_report_valid_psi(self):
        self.assertIsNone(DriftMonitor.fit(range(100)).compare([1,2])['psi'])
    def test_invalid_and_nonfinite(self):
        with self.assertRaises(ValueError): DriftMonitor.fit([None,None])
        result=DriftMonitor.fit(range(100)).compare([float('nan')]*40)
        self.assertEqual(result['missing_rate'],1)
        self.assertIn('insufficient-finite-samples',result['alerts'])
