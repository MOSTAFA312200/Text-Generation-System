from unittest.mock import patch

from generator import generate_text


def test_generate_text():
    with patch("generator.tokenizer") as mock_tokenizer, \
         patch("generator.model") as mock_model:

        mock_tokenizer.return_value = {
            "input_ids": [[101, 2023, 2003]]
        }

        mock_model.generate.return_value = [
            [101, 2023, 2003, 1037, 3231, 102]
        ]

        mock_tokenizer.decode.return_value = (
            "Artificial intelligence is powerful."
        )

        result = generate_text("Artificial intelligence is")

        assert isinstance(result, str)
        assert len(result) > 0