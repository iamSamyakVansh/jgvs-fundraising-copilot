"""AppTest smoke coverage for every page render function."""
import unittest

from streamlit.testing.v1 import AppTest


class PageSmokeTests(unittest.TestCase):
    """Ensure each page renders without Streamlit exceptions."""

    def test_all_page_renderers(self) -> None:
        """Smoke-render all eight modules against initialized demo state."""
        modules = ["overview", "opportunities", "eligibility", "knowledge_base", "proposal", "donor_crm", "approval_queue", "followups"]
        for module in modules:
            with self.subTest(page=module):
                script = f"from state import init_state\nfrom pages import {module}\ninit_state()\n{module}.render()"
                app = AppTest.from_string(script).run(timeout=10)
                self.assertEqual(len(app.exception), 0, [item.message for item in app.exception])
