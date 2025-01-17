import os
import re
import textstat
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from tqdm import tqdm

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

def load_word_lists():
    """Load positive and negative word lists from files"""
    positive_words_path = 'D:/project/MasterDictionary/positive-words.txt'
    negative_words_path = 'D:/project/MasterDictionary/negative-words.txt'

    try:
        with open(positive_words_path, 'r', encoding='utf-8') as file:
            positive_words = set(word.strip() for word in file.readlines() 
                               if word.strip() and not word.startswith(';'))
        
        with open(negative_words_path, 'r', encoding='utf-8') as file:
            negative_words = set(word.strip() for word in file.readlines()
                               if word.strip() and not word.startswith(';'))
        
        return positive_words, negative_words
    except FileNotFoundError as e:
        print(f"Error loading word lists: {e}")
        return set(), set()

def clean_text(text):
    """Clean text while preserving word boundaries and sentence structure"""
    text = text.replace('\n', ' ')
    text = ' '.join(text.split())
    text = re.sub(r'([.,!?:;])', r' \1 ', text)
    text = re.sub(r'[^a-zA-Z\s.,!?]', ' ', text)
    text = ' '.join(text.split())
    return text.lower()

def get_words_with_lemma(text):
    """Get lemmatized words with proper boundaries."""
    words = text.split()
    words = [re.sub(r'[.,!?:;]', '', word) for word in words]
    words = [word for word in words if word.isalpha()]
    return [lemmatizer.lemmatize(word) for word in words]

def analyze_sentiment(text, positive_words, negative_words):
    """Analyze sentiment with exact word matching."""
    cleaned_text = clean_text(text)
    words = get_words_with_lemma(cleaned_text)

    positive_matches = [word for word in words if word in positive_words]
    negative_matches = [word for word in words if word in negative_words]

    print("Positive words found:", positive_matches)
    print("Positive word count:", len(positive_matches))
    print("Negative words found:", negative_matches)
    print("Negative word count:", len(negative_matches))

    return len(positive_matches), len(negative_matches)

def analyze_article(file_path, positive_words, negative_words):
    """Analyze a single article and return metrics"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                text = file.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None

    cleaned_text = clean_text(text)
    sentences = sent_tokenize(cleaned_text)
    words = get_words_with_lemma(cleaned_text)

    if not words:
        print(f"Warning: No valid words found in {file_path}")
        return None

    positive_score, negative_score = analyze_sentiment(text, positive_words, negative_words)

    word_count = len(words)
    sentence_count = len(sentences)
    complex_words = [word for word in words if textstat.syllable_count(word) > 2]
    complex_word_count = len(complex_words)
    syllable_count = sum(textstat.syllable_count(word) for word in words)

    try:
        polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
        subjectivity_score = (positive_score + negative_score) / (word_count + 0.000001)
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        percentage_complex_words = (complex_word_count / word_count * 100) if word_count > 0 else 0
        fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
        syllable_per_word = syllable_count / word_count if word_count > 0 else 0
        avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
        personal_pronouns = len(re.findall(r'\b(?!US\b)(I|we|my|ours|us)\b', text, flags=re.IGNORECASE))
    except ZeroDivisionError:
        print(f"Warning: Zero division error in file {file_path}")
        return None

    return {
        "URL_ID": os.path.splitext(os.path.basename(file_path))[0],
        "POSITIVE SCORE": positive_score,
        "NEGATIVE SCORE": negative_score,
        "POLARITY SCORE": polarity_score,
        "SUBJECTIVITY SCORE": subjectivity_score,
        "AVG SENTENCE LENGTH": avg_sentence_length,
        "PERCENTAGE OF COMPLEX WORDS": percentage_complex_words,
        "FOG INDEX": fog_index,
        "AVG NUMBER OF WORDS PER SENTENCE": avg_sentence_length,
        "COMPLEX WORD COUNT": complex_word_count,
        "WORD COUNT": word_count,
        "SYLLABLE PER WORD": syllable_per_word,
        "PERSONAL PRONOUNS": personal_pronouns,
        "AVG WORD LENGTH": avg_word_length
    }

def main():
    input_excel = 'D:/project/Input.xlsx'
    input_dir = 'extracted_articles'
    output_path = 'D:/project/Output_Data_Analysis2.xlsx'

    try:
        input_df = pd.read_excel(input_excel)
        print(f"Loaded {len(input_df)} entries from Input.xlsx")
    except Exception as e:
        print(f"Error reading Input.xlsx: {e}")
        return

    positive_words, negative_words = load_word_lists()
    if not positive_words or not negative_words:
        print("Error: Failed to load word lists")
        return

    print(f"Loaded {len(positive_words)} positive words and {len(negative_words)} negative words")

    results = []
    for file_name in tqdm(os.listdir(input_dir), desc="Analyzing articles"):
        if not file_name.endswith('.txt'):
            continue

        file_path = os.path.join(input_dir, file_name)
        result = analyze_article(file_path, positive_words, negative_words)

        if result:
            url_id = result["URL_ID"]
            input_row = input_df[input_df['URL_ID'].astype(str) == str(url_id)]

            if not input_row.empty:
                input_data = input_row.iloc[0].to_dict()
                result.update(input_data)
                results.append(result)

    if results:
        output_df = pd.DataFrame(results)
        column_order = [
            'URL_ID', 'URL',
            'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE',
            'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH',
            'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX',
            'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT',
            'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS',
            'AVG WORD LENGTH'
        ]
        output_df = output_df[column_order]
        output_df.to_excel(output_path, index=False)
        print(f"\nAnalysis completed. Results saved to '{output_path}'")
        print(f"Processed {len(results)} articles successfully")
    else:
        print("No data to save")

if __name__ == "__main__":
    main()
