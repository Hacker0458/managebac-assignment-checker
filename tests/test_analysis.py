import unittest

from managebac_checker.analysis import analyse_assignments
from tests.factories import make_assignment


class AnalysisTests(unittest.TestCase):
    def test_counts_by_status(self):
        submitted = make_assignment(status="Submitted", priority="low", submitted=True)
        overdue = make_assignment(status="Overdue", priority="high", overdue=True)
        pending = make_assignment(status="Pending", priority="medium")

        analysis = analyse_assignments(
            [submitted, overdue, pending],
            priority_keywords=["exam", "project"],
            days_ahead=7,
        )

        self.assertEqual(analysis["total_assignments"], 3)
        self.assertEqual(analysis["submitted_count"], 1)
        self.assertEqual(analysis["overdue_count"], 1)
        self.assertEqual(analysis["pending_count"], 1)
        self.assertEqual(len(analysis["grouped_by_status"]["submitted"]), 1)
        self.assertEqual(len(analysis["grouped_by_status"]["overdue"]), 1)
        self.assertEqual(len(analysis["grouped_by_status"]["pending"]), 1)

    def test_urgency_buckets(self):
        urgent = make_assignment(due_date="today")
        soon = make_assignment(due_date="tomorrow")
        later = make_assignment(due_date="2025-12-31")

        analysis = analyse_assignments(
            [urgent, soon, later],
            priority_keywords=[],
            days_ahead=3,
        )

        self.assertGreaterEqual(len(analysis["assignments_by_urgency"]["urgent"]), 1)
        self.assertGreaterEqual(len(analysis["assignments_by_urgency"]["later"]), 1)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
