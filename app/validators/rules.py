def rule_single_bullet(slide):
    messages = []
    for bullet_list in slide["bullets"]:
        if len(bullet_list) == 1:
            messages.append({
                "slide": slide["slide_number"],
                "rule": "single_bullet",
                "message": "Slide contains a bullet list with only one item",
                "severity": "warning"
            })
    return messages

def rule_font_inconsistency(slide, all_fonts=None):
    messages = []
    if all_fonts is None:
        all_fonts = set()
    all_fonts.update(slide["fonts"])
    return messages, all_fonts

def rule_empty_slide(slide):
    if not slide["texts"] and not slide["bullets"]:
        return [{
            "slide": slide["slide_number"],
            "rule": "empty_slide",
            "message": "Slide is empty",
            "severity": "warning"
        }]
    return []

RULES = [
    ("single_bullet", rule_single_bullet),
    ("empty_slide", rule_empty_slide),
]
