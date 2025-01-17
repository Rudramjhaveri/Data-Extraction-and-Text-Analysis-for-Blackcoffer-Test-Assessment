Data Extraction and Text Analysis for Blackcoffer Test Assessment
📄 Objective
The project involves extracting textual data from given URLs and performing text analysis to compute metrics such as polarity score, subjectivity score, word counts, and readability indices.

🛠️ Tools and Technologies
Programming Language: Python
Libraries Used: BeautifulSoup, Selenium, Scrapy, Pandas, NLTK, NumPy
📑 Steps to Run
Install required dependencies:
bash
Copy
Edit
pip install -r requirements.txt
Place Input.xlsx in the root directory.
Run the Python script:
bash
Copy
Edit
python data_extraction_analysis.py
The output will be generated in a file named Output.xlsx.
📊 Output
The output includes:

Positive and negative scores.
Polarity and subjectivity scores.
Readability indices like FOG Index.
Word and sentence metrics.
📂 Folder Structure
graphql
Copy
Edit
├── data_extraction_analysis.py  # Main script
├── Input.xlsx                  # Input URLs
├── Output.xlsx                 # Resulting analysis
├── requirements.txt            # Dependencies
├── README.md                   # Documentation
