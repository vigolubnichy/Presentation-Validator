from app.validators.parser import parse_presentation

def test_parser_function_exists():
    assert callable(parse_presentation)
