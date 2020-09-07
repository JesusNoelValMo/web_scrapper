import argparse
import logging
logging.basicConfig(level=logging.INFO)
from urllib.parse import urlparse
import pandas as pd
import hashlib as hl
import nltk
from nltk.corpus import stopwords
logger = logging.getLogger(__name__)

def main(filename):
    logger.info('Starting cleaning process')
    df = _read_data(filename)
    newspaper = _extract_newspaper_uid(filename)
    df = _add_newspaper_column(df, newspaper)
    df = _extract_host(df)
    df = _fill_missing_titles(df)
    df = _generate_uids_for_rows(df)
    df = _remove_new_lines_from_body(df)
    df = _tokenize_columns(df, 'body')
    df = _remove_duplicates(df, 'title')
    df = _drop_rows_with_missing_values(df)
    _save_data(df, filename)
    return df

def _remove_duplicates(df, column_name):
    logger.info('Removing duplicates')
    df.drop_duplicates(subset=[column_name], keep='first')
    return df

def _drop_rows_with_missing_values(df):
    logger.info('Dropping rows with missing values')
    return df.dropna()

def _save_data(df, filename):
    clean_filename = 'clean_{}'.format(filename)
    logger.info('Saving data to disk {}'.format(filename))
    df.to_csv(clean_filename)

stop_words = set(stopwords.words('spanish'))

def _tokenize_columns(df, column_name):
    tokenized = (df
           .dropna()
           .apply(lambda row: nltk.word_tokenize(row[column_name]), axis=1)
           .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens)))
           .apply(lambda tokens: list(map(lambda token: token.lower(), tokens)))
           .apply(lambda word_list: list(filter(lambda word: word not in stop_words, word_list)))
           .apply(lambda valida_word_list: len(valida_word_list))
           )
    df['n_tokens_title'] = tokenized
    return df
def _generate_uids_for_rows(df):
    logger.info('Generating uids for each row')
    uids = (df
            .apply(lambda row: hl.md5(bytes(row['url'].encode())) , axis = 1)
            .apply(lambda hash_object: hash_object.hexdigest())
            )
    df['uids'] = uids
    return df.set_index('uids')
def _remove_new_lines_from_body(df):
    logger.info('Removing new lines from body')
    stripped_body = (df
                .apply(lambda row: row['body'], axis=1)
                .apply(lambda body: list(body))
                .apply(lambda letters: list(map(lambda letter: letter.replace('\n', ''), letters)))
                .apply(lambda letters: ''.join(letters))
                )
    df['body'] = stripped_body
    return df

def _fill_missing_titles(df):
    logger.info('Filling Missing titles ')
    missing_titles_mask = df['title'].isna()
    missing_titles = (df[missing_titles_mask]['url']
                .str.extract(r'(?P<missing_titles>[^/]+)$')
                .applymap(lambda title: title.split('-'))
                .applymap(lambda title_word_list: ' '.join(title_word_list))
                )
    df.loc[missing_titles_mask, 'title'] = missing_titles.loc[:, 'missing_titles']
    return df

def _extract_host(df):
    logger.info('Extracting host')
    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)
    return df

def _add_newspaper_column(df, newspaper):
    logger.info('filling newspaper name column with {}'.format(newspaper))
    df['newspaper'] = newspaper

    return df

def _extract_newspaper_uid(filename):
    logging.info('Extracting newspaper name')
    newspaper = filename.split('_')[0]
    logger.info('Newspaper name detected: {}'.format(newspaper))
    return newspaper

def _read_data(filename):
    logger.info('Reading file {}'.format(filename))
    return pd.read_csv(filename, encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
        help = 'Path to dirty data',
        type = str)
    arg = parser.parse_args()
    df = main(arg.filename)
    print(df)