import unittest
from pathlib import Path

from managebac_checker.analysis import analyse_assignments
from managebac_checker.reporting import ReportBuilder
from tests.factories import make_assignment


class ReportingTests(unittest.TestCase):
    def test_report_builder_generates_requested_formats(self):
        tmp_path = Path("./reports_test")
        tmp_path.mkdir(exist_ok=True)

        assignments = [make_assignment(title="Essay", priority="high")]
        analysis = analyse_assignments(assignments, priority_keywords=["essay"], days_ahead=7)
        builder = ReportBuilder(output_dir=tmp_path, report_formats=["console", "html", "json", "markdown"])

        reports = builder.build(assignments, analysis)
        self.assertEqual(set(reports.keys()), {"console", "html", "json", "markdown"})

        saved = builder.persist(reports)
        self.assertEqual(set(saved.keys()), {"html", "json", "markdown"})
        for path in saved.values():
            target = Path(path)
            self.assertTrue(target.exists())
            self.assertTrue(target.read_text(encoding="utf-8"))

        for path in tmp_path.iterdir():
            path.unlink()
        tmp_path.rmdir()


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
