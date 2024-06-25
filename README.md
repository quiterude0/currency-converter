# Currency Converter

A sleek and modern currency converter application built with Python and PyQt6. This app fetches real-time exchange rates and provides an intuitive interface for currency conversion.

## Features

- Real-time currency conversion using the ExchangeRate-API
- Sleek dark-themed user interface
- Support for multiple currencies
- Animated result display
- Secure API key management using environment variables

## Requirements

- Python 3.8+(Recommended 3.10)
- PyQt6
- Requests
- python-dotenv

## Installation

Clone this repository.

Create a virtual environment (optional but recommended).

Install the required packages. (pip install -r requirements.txt)

Sign up for a free API key at [ExchangeRate-API](https://www.exchangerate-api.com/).

Then in the '.env' file(rename it from .env.example to .env) just paste your API key.

1. Enter the amount you want to convert in the "Amount" field.
2. Select the currency you're converting from in the "From" dropdown.
3. Select the currency you're converting to in the "To" dropdown.
4. Click the "Convert" button or press Enter to see the result.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgements

- [ExchangeRate-API](https://www.exchangerate-api.com/) for providing real-time exchange rates.
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework.
