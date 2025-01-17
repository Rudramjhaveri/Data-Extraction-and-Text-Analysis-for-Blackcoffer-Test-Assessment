# Data Extraction and Text Analysis Project 📊

## Overview
This project performs automated text extraction and analysis from web URLs, computing various metrics including sentiment scores, readability indices, and text statistics. It's designed to process multiple URLs from an Excel input and generate comprehensive text analytics in a structured output format.

## 🎯 Features

### Web Scraping
- Multi-threaded URL processing
- Support for various web page structures
- Robust error handling and retry mechanisms
- Clean text extraction with HTML parsing

### Text Analysis
- **Sentiment Analysis**
  - Positive/Negative score calculation
  - Polarity score computation
  - Subjectivity analysis
  
- **Readability Metrics**
  - FOG Index calculation
  - Average sentence length
  - Complex word percentage
  - Syllable per word ratio

- **Text Statistics**
  - Word count and frequency
  - Sentence count
  - Average word length
  - Complex word analysis

## 🛠️ Technical Stack

### Core Technologies
- Python 3.8+
- Pandas for data handling
- NLTK for natural language processing

### Web Scraping Libraries
- BeautifulSoup4
- Selenium WebDriver
- Scrapy (optional)

### Analysis Libraries
- NumPy for numerical operations
- NLTK for text processing
- TextBlob for sentiment analysis

## 📥 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/text-analysis-project.git
cd text-analysis-project
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

1. Prepare your input file:
   - Place your `Input.xlsx` file in the project root directory
   - Ensure it contains a column with URLs to analyze

2. Run the analysis:
```bash
python data_extraction_analysis.py
```

3. Check results:
   - Output will be generated as `Output.xlsx`
   - Review the generated metrics and analysis

## 📊 Output Format

The `Output.xlsx` file contains the following metrics for each URL:

| Metric | Description |
|--------|-------------|
| Positive Score | Count of positive words |
| Negative Score | Count of negative words |
| Polarity Score | Overall text polarity (-1 to 1) |
| Subjectivity Score | Text subjectivity measure (0 to 1) |
| FOG Index | Readability measure |
| Average Sentence Length | Mean words per sentence |
| Complex Word Count | Number of complex words |
| Word Count | Total word count |

## 📁 Project Structure
```
text-analysis-project/
├── data_extraction_analysis.py
├── Input.xlsx
├── Output.xlsx
├── requirements.txt
├── README.md
└── utils/
    ├── scraper.py
    ├── analyzer.py
    └── helpers.py
```

## ⚙️ Configuration

Modify `config.py` to adjust:
- Scraping parameters
- Analysis thresholds
- Output format preferences
- Threading settings

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Dependencies

Main dependencies include:
```
beautifulsoup4>=4.9.3
selenium>=3.141.0
pandas>=1.2.0
nltk>=3.5
numpy>=1.19.5
textblob>=0.15.3
```

## 🔍 Troubleshooting

Common issues and solutions:
- **URL Access Errors**: Check internet connection and URL validity
- **Memory Issues**: Reduce batch size in configuration
- **Slow Processing**: Adjust thread count in settings

## 👥 Contact
- Email: rudram.jhaveri@gmail.com
