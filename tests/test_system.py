import pytest
from friday.tools.system import run_smart_task

def test_run_smart_task_safe():
    result = run_smart_task("echo 'hello world'")
    assert "hello world" in result

def test_run_smart_task_dangerous():
    result = run_smart_task("rm -rf /")
    assert "SAFETY ALERT" in result

def test_run_smart_task_command_injection():
    # If the vulnerability is present, this will execute the command and return its output
    # By providing `ls ; echo injected`, we can see if `echo injected` is executed
    # Using shlex.split and shell=False, the command "echo" will receive "test", ";", "echo", "injected" as arguments
    # So it will print them all out. This means "injected" WILL be in the output, but as a string printed by echo, NOT as an executed command.
    # To truly test command injection, we should try to execute a command that does something recognizable, or we verify that the shell metacharacters aren't interpreted.
    # A better way is to test a command that relies on shell interpretation to work, and show it fails or doesn't execute as intended.
    result = run_smart_task("echo test && echo injected")
    assert "injected" in result # It will be in the output because echo prints "test && echo injected"

    # Let's verify it actually just printed the string instead of executing the second echo
    assert "test && echo injected" in result
