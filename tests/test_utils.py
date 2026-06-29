import json
from friday.tools.utils import format_json

def test_format_json_valid_string():
    # Test with a valid JSON string
    input_str = '{"name": "Tony", "role": "Iron Man"}'
    expected_output = json.dumps(json.loads(input_str), indent=2)
    assert format_json(input_str) == expected_output

def test_format_json_invalid_string():
    # Test with an invalid JSON string
    input_str = '{"name": "Tony", "role": "Iron Man"'
    result = format_json(input_str)
    assert result.startswith("Invalid JSON or parsing error:")

def test_format_json_dict_list():
    # Test with a Python dict
    input_dict = {"name": "Tony", "role": "Iron Man"}
    expected_output = json.dumps(input_dict, indent=2)
    assert format_json(input_dict) == expected_output

    # Test with a Python list
    input_list = [{"name": "Tony"}, {"name": "Steve"}]
    expected_output = json.dumps(input_list, indent=2)
    assert format_json(input_list) == expected_output
