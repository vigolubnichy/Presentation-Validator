from app.validators.rules import single_item_list, multiple_fonts

def test_single_item_list_positive():
    slide = {"texts": ["one"], "fonts": ["Arial"]}
    assert single_item_list(slide) is not None

def test_single_item_list_negative():
    slide = {"texts": ["one", "two"], "fonts": ["Arial"]}
    assert single_item_list(slide) is None

def test_multiple_fonts_positive():
    slide = {"texts": ["a", "b"], "fonts": ["Arial", "Times"]}
    assert multiple_fonts(slide) is not None

def test_multiple_fonts_negative():
    slide = {"texts": ["a"], "fonts": ["Arial"]}
    assert multiple_fonts(slide) is None
