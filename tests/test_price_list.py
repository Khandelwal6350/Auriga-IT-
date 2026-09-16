import unittest

from habit_tracker.price_list import clean_price_list


class PriceListTests(unittest.TestCase):
    def test_case_insensitive_duplicates_keep_last_valid_price(self):
        result = clean_price_list([
            {"seat_class": "Economy", "price": "1000"},
            {"seat_class": "economy", "price": "1200"},
            {"seat_class": "ECONOMY", "price": "1300"},
        ])

        self.assertEqual(result["imported"], [{"seat_class": "Economy", "price": 1300.0}])
        self.assertEqual(len(result["deduplicated"]), 2)

    def test_messy_price_formats_are_normalized(self):
        result = clean_price_list([
            {"seat_class": "A", "price": "1200"},
            {"seat_class": "B", "price": "1,200"},
            {"seat_class": "C", "price": "₹1200.00"},
            {"seat_class": "D", "price": "1200/-"},
            {"seat_class": "E", "price": " 1200 "},
            {"seat_class": "F", "price": "1200.50"},
        ])

        self.assertEqual([item["price"] for item in result["imported"]], [1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.5])

    def test_blank_price_is_rejected(self):
        result = clean_price_list([{"seat_class": "Economy", "price": "  "}])
        self.assertEqual(result["imported"], [])
        self.assertEqual(result["rejected"][0]["reason"], "price is blank")

    def test_negative_price_is_rejected(self):
        result = clean_price_list([{"seat_class": "Business", "price": "-500"}])
        self.assertEqual(result["imported"], [])
        self.assertEqual(result["rejected"][0]["reason"], "price cannot be negative")

    def test_fully_valid_row_is_imported_in_title_case(self):
        result = clean_price_list([{"seat_class": "premium economy", "price": "₹1,499.50"}])
        self.assertEqual(result["imported"], [{"seat_class": "Premium Economy", "price": 1499.5}])
        self.assertEqual(result["deduplicated"], [])
        self.assertEqual(result["rejected"], [])


if __name__ == "__main__":
    unittest.main()
