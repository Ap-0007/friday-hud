import unittest
from friday.tools.system import run_smart_task

class TestRunSmartTask(unittest.TestCase):
    def test_run_smart_task_safe(self):
        result = run_smart_task("echo 'hello'")
        self.assertIn("hello", result)

    def test_run_smart_task_dangerous(self):
        result = run_smart_task("rm -rf /")
        self.assertIn("SAFETY ALERT", result)

    def test_run_smart_task_injection(self):
        # We want to ensure that "echo hello; echo injected"
        # doesn't actually execute the second command but instead fails or echoes it literally.
        # Without shell=True, "echo hello; echo injected" passes "hello; echo injected" as one arg to echo
        # Let's test that "echo 'hello'; id" doesn't execute 'id'

        # Shlex parses "echo 'hello'; id" into ['echo', 'hello;', 'id']
        # The echo command will output "hello; id\n"
        result = run_smart_task("echo 'hello'; id")
        self.assertIn("Task completed", result)
        self.assertIn("hello; id", result)

        # Or injection like `echo hello && id`
        result_amp = run_smart_task("echo hello && id")
        self.assertIn("hello && id", result_amp)

if __name__ == '__main__':
    unittest.main()