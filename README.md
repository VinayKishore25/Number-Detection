# Phone Number Info Finder

## Overview
Phone Number Info Finder is a Python-based GUI application built using Tkinter and the `phonenumbers` library. It allows users to retrieve information about a phone number, including its region, country, and service provider.

## Features
- Full-screen responsive GUI using Tkinter.
- User-friendly interface with a country code selection dropdown.
- Fetches details like region, country, and service provider.
- Displays results in a text area with easy-to-read formatting.
- Options to clear input and save results to a file.
- Hover effects for a modern button UI.
- Uses the NumVerify API for service provider details.

## Requirements
Ensure you have the following dependencies installed before running the application:

```sh
pip install phonenumbers tkinter requests
```

## Installation
1. Clone the repository or download the script.
2. Ensure all dependencies are installed.
3. Run the script using:

```sh
python phone_number_info.py
```

## Usage
1. Select the country code from the dropdown.
2. Enter the phone number (without the country code).
3. Click on **Get Info** to retrieve details.
4. Click **Clear** to reset input fields.
5. Click **Save Result** to save the details to a text file.

## API Configuration
This application uses the NumVerify API to fetch the service provider. Replace `api_key` in the script with your valid API key:

```python
api_key = "your_api_key_here"
```

You can obtain an API key from [NumVerify](https://numverify.com/).

## Screenshots
![App Screenshot](screenshot.png)

## License
This project is open-source and available under the MIT License.

## Author
Munjuluri V V D Surya Kishore Vinay

