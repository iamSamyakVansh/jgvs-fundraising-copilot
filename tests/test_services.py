"""Unit tests for framework-independent fundraising services."""
import unittest

from services.budget import line_percentages, summarize_budget
from services.eligibility import CHECKS, score_eligibility
from services.export import escape_html
from services.ids import new_id
from services.validation import valid_date, valid_email, valid_number, valid_url


class ServiceTests(unittest.TestCase):
    """Unit tests collected by both unittest and pytest."""

    def test_eligibility_scores_and_readiness(self) -> None:
        """All weighted checks yield 100; incomplete checks remain partial."""
        labels = {label for label, _, _ in CHECKS}
        self.assertEqual(score_eligibility(labels).score, 100)
        self.assertEqual(score_eligibility(labels).readiness, "Ready for human review")
        self.assertEqual(score_eligibility(set()).readiness, "Not ready")
        self.assertEqual(score_eligibility({next(iter(labels))}).readiness, "Partially ready")

    def test_budget_math_and_percentages(self) -> None:
        """Budget subtotal, variance, and shares are consistent."""
        result = summarize_budget({"People": 60, "Travel": 40}, 125)
        self.assertEqual((result.subtotal, result.variance), (100, 25))
        self.assertEqual(line_percentages({"People": 60, "Travel": 40}), {"People": 60, "Travel": 40})
        with self.assertRaises(ValueError):
            summarize_budget({"People": -1}, 0)

    def test_unique_id_generation(self) -> None:
        """Record identifiers are unique and hex encoded."""
        first, second = new_id(), new_id()
        self.assertNotEqual(first, second)
        self.assertRegex(first, r"^[0-9a-f]{32}$")

    def test_url_email_date_number_validation(self) -> None:
        """Reject malformed values and accept valid examples."""
        for value in ("https://example.org/path", "http://example.org"):
            with self.subTest(value=value): self.assertTrue(valid_url(value))
        self.assertFalse(valid_url("javascript:alert(1)"))
        self.assertFalse(valid_url("https://"))
        self.assertTrue(valid_email("person@example.org"))
        self.assertFalse(valid_email("not-an-email"))
        self.assertTrue(valid_date("2026-12-31"))
        self.assertFalse(valid_date("31-12-2026"))
        self.assertTrue(valid_number("100.5"))
        self.assertFalse(valid_number("-2"))

    def test_html_escaping(self) -> None:
        """Untrusted content is escaped before any safe HTML interpolation."""
        self.assertEqual(escape_html('<script>alert("x")</script>'), "&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;")
