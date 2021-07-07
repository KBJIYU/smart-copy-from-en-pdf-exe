from .data_reader import get_fixtures
from modifytext import modify_en_text

def test_novel():
    fixtures = get_fixtures()

    fixture = fixtures['novel']
    expected_output = fixture['output']
    actual_output = ''.join(modify_en_text(fixture['input']))

    assert expected_output == actual_output

def test_thesis():
    fixtures = get_fixtures()

    fixture = fixtures['thesis']
    expected_output = fixture['output']
    actual_output = ''.join(modify_en_text(fixture['input']))

    assert expected_output == actual_output

def test_latex():
    fixtures = get_fixtures()

    fixture = fixtures['latex']
    expected_output = fixture['output']
    actual_output = ''.join(modify_en_text(fixture['input']))

    assert expected_output == actual_output

def test_thesis_basic():
    fixtures = get_fixtures()

    fixture = fixtures['thesis_basic']
    expected_output = fixture['output']
    actual_output = ''.join(modify_en_text(fixture['input']))

    assert expected_output == actual_output
