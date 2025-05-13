# tests/test_app.py

def test_price_level_mapping():
    level_to_label = {
        1: "Inexpensive",
        2: "Moderate",
        3: "Expensive",
        4: "Very Expensive"
    }
    assert level_to_label[1] == "Inexpensive"
    assert level_to_label[4] == "Very Expensive"