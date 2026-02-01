# data_cleaning.py
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

# download NLTK stopwords
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

'''
1. lower case text
2. remove punctuations
3. remove stopwords
4. remove extra spaces
(ONLY for natural language text)
'''
def clean_text(text):
    if not isinstance(text, str):
        return text   # <-- THIS LINE FIXES THE ERROR

      # encoding / normalization cleaning
    text = re.sub(r"[^\x00-\x7F]", " ", text)

    text = str(text).lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = " ".join([w for w in text.split() if w not in stop_words])
    text = re.sub(r"\s+", " ", text).strip()
    return text


'''
Light cleaning:
- lowercase
- remove extra spaces
(NO stopwords, NO punctuation removal)
Used for yes/no, dates, labels
'''
def clean_light(text):
    text = str(text).lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text


# =========================
# COLUMN CONFIGURATIONS
# =========================

AMAZON_TEXT_COLUMNS = [
    "Product Name",
    "Category",
    "User Review",
    "Comment"
]

FLIPKART_TEXT_COLUMNS = [
    "ProductName",
    "Price",
    "Review",
    "Summary"
]

AMAZON_LIGHT_CLEAN_COLUMNS = [
    "Verified Purchase",
    "Sentiment",
    "Date of Review"
]


'''
1. drop duplicates
2. clean text columns
3. clean categorical/date columns safely
'''
def clean_dataframe(df, text_columns, light_columns):
    df = df.drop_duplicates()

    # NLP cleaning
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)

    # light cleaning (yes/no, dates)
    if light_columns:
        for col in light_columns:
            if col in df.columns:
                df[col] = df[col].apply(clean_light)

    return df


# =========================
# DRIVER CODE
# =========================
if __name__ == "__main__":
    # df = pd.read_csv("data/flipkart_product.csv", encoding="latin1", engine="python")
    df = pd.read_excel("data/Amazon DataSheet - Pradeep.xlsx")

    df_clean = clean_dataframe(
        df,
        text_columns=AMAZON_TEXT_COLUMNS,
        light_columns=AMAZON_LIGHT_CLEAN_COLUMNS
    )

    df_clean.to_csv("data/amazon_cleaned_data.csv", index=False, encoding='utf-8')
    # df_clean.to_csv("data/flipkart_cleaned_data.csv", index=False, encoding='utf-8')
