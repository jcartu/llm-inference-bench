"""None-safety behavioral tests for measured sample window end selection."""

import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "llm_decode_bench.py"
SPEC = importlib.util.spec_from_file_location("bench_decode_time_guards", MODULE_PATH)
BENCH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BENCH)


class SampleWindowEndTests(unittest.TestCase):
    def test_valid_post_start_sample_returns_last_time(self):
        self.assertEqual(
            BENCH._sample_window_end(
                last_time=15.0,
                sample_count=7,
                measurement_start=10.0,
                fallback=20.0,
            ),
            15.0,
        )

    def test_none_last_time_falls_back_without_type_error(self):
        self.assertEqual(
            BENCH._sample_window_end(
                last_time=None,
                sample_count=7,
                measurement_start=10.0,
                fallback=20.0,
            ),
            20.0,
        )

    def test_none_measurement_start_falls_back_without_type_error(self):
        self.assertEqual(
            BENCH._sample_window_end(
                last_time=15.0,
                sample_count=7,
                measurement_start=None,
                fallback=None,
            ),
            None,
        )

    def test_zero_samples_or_pre_start_sample_falls_back(self):
        self.assertEqual(
            BENCH._sample_window_end(
                last_time=15.0,
                sample_count=0,
                measurement_start=10.0,
                fallback=20.0,
            ),
            20.0,
        )
        self.assertEqual(
            BENCH._sample_window_end(
                last_time=10.0,
                sample_count=7,
                measurement_start=10.0,
                fallback=20.0,
            ),
            20.0,
        )


if __name__ == "__main__":
    unittest.main()
