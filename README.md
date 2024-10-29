# Daraz Mobile Product Scraper and Chatbot

This repository contains two primary components:
1. A **web scraper** that extracts mobile product details and reviews from [Daraz.pk](https://www.daraz.pk/).
2. A **Flask-based chatbot** that uses the scraped data to provide user-friendly interactions and answers user queries related to mobile product details and reviews.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)

## Project Overview

The project consists of two main components:
1. **Web Scraper**: Uses Selenium to scrape mobile phone product data and reviews from Daraz, storing them in CSV files.
2. **Chatbot**: Built using Flask, the chatbot interacts with users and provides relevant information about mobile products based on the user’s queries, such as brand, price range, rating, etc. It can also display reviews for specific products.

## Features

- **Scraping Product Details**: Extracts product details such as name, brand, price, rating, specifications, and reviews.
- **Review Sentiment Analysis**: Performs sentiment analysis on reviews using the NLTK library to classify them as positive, negative, or neutral.
- **Query Processing**: Users can search for products by brand, price range, and rating.
- **Flask-based Chatbot**: Provides a user-friendly interface to interact with the data, display product information, and view product reviews.
- **Additional Search Options**: Allows users to perform additional review-based searches within the same interface.

## Installation

### Prerequisites

1. Python 3.7 or higher
2. Google Chrome installed on your system

### Required Libraries

Ensure that the following libraries are installed:
- Selenium
- NLTK
- Pandas
- Flask
- Matplotlib
- Webdriver Manager

You can install these libraries individually using:

```bash
pip install selenium nltk pandas flask matplotlib webdriver-manager
```

### Setup NLTK

After installing NLTK, download the required datasets for tokenization and sentiment analysis:

```python
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

## Usage

### Scraping Data

1. **Run the Scraper**: 
   - Open `Data Scraping.ipynb` in Jupyter Notebook or any compatible environment.
   - Run the cells in the notebook sequentially to scrape mobile product details and reviews from Daraz.
   - The data will be stored in two CSV files: `Final_Phone_Data.csv` and `Final_Review_Data.csv`.

**Note:** The scraping functionality might not work correctly if Daraz has made changes to their website structure. You may need to update the XPaths, class names, or other selectors in the code to match the new layout of the website.

### Running the Chatbot

1. **Run the Flask App**:
   - In the terminal, run:

   ```bash
   python app.py
   ```

2. **Interact with the Chatbot**:
   - After running the Flask app, check the terminal for the server path (e.g., `http://127.0.0.1:5000/`).
   - Click on the server path to open the chatbot interface in your web browser.
   - Enter queries such as:
     - “Show Samsung phones with a rating above 4.5”
     - “Display Infinix phones under 20,000 PKR”
     - “Show reviews for product ID 123”

## File Structure

```
daraz-scraper-chatbot/
│
├── app.py                    # Flask-based chatbot application
├── Data Scraping.ipynb       # Jupyter Notebook for scraping data from Daraz
├── Final_Phone_Data.csv      # CSV file storing scraped mobile product details
├── Final_Review_Data.csv     # CSV file storing scraped reviews
├── requirements.txt          # List of required Python libraries
│
├── templates/                # HTML templates for the web interface
│   ├── home.html             # Main template for the chatbot interface
│   └── dashboard.html        # Template for displaying product dashboard
│
├── static/                   # Static files for web app (images, CSS)
│   ├── bar_graph.jpg         # Bar graph image
│   ├── count.png             # Count plot image
│   ├── graph2.png            # Additional graph image
│   └── line_graph.jpg        # Line graph image
│
└── __pycache__/              # Python cache files (auto-generated)
```

### Explanation

- **`app.py`**: The main Flask application that runs the chatbot, processes user queries, and renders templates.
- **`Data Scraping.ipynb`**: Jupyter Notebook used for scraping mobile data from Daraz, storing it in CSV format.
- **`Final_Phone_Data.csv`** & **`Final_Review_Data.csv`**: CSV files containing the scraped mobile phone data and reviews.
- **`templates/`**: Contains HTML templates for the Flask application.
  - **`home.html`**: Main template for interacting with the chatbot and searching for products.
  - **`dashboard.html`**: Template for displaying product data in a dashboard format.
- **`static/`**: Contains static assets such as images used in the web interface.

## Technologies Used

- **Python**: Primary programming language used.
- **Selenium**: For web scraping product data from Daraz.
- **NLTK**: For sentiment analysis of reviews.
- **Flask**: For building the chatbot web application.
- **Pandas**: For data handling and processing.
- **Matplotlib**: For visualization (if needed).

## Contributing

Feel free to contribute to this project by creating pull requests, reporting issues, or suggesting new features.
