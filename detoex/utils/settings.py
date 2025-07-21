import os


STANZA_RESOURCES_DIR = os.getenv('STANZA_RESOURCES_DIR')
VOCABULARIES_PATH = os.getenv('VOCABULARIES_PATH')

STANZA_MODELS_KWARGS = {
    'en': {
        'download_method': 'reuse_resources',
        'processors': 'tokenize, mwt, pos, lemma',
        'package': 'default_accurate',
    },
    'fr': {
        'download_method': 'reuse_resources',
        'processors': 'tokenize, mwt, pos, lemma',
        'package': 'default_accurate',
    },
    'el': {
        'download_method': 'reuse_resources',
        'processors': 'tokenize, mwt, pos, lemma',
        'package': 'default_accurate',
    }
}

STARTUP_LANGUAGES = [
    'en',
    'fr',
    'el',
]

PROCESSED_TERMS_FILEPATHS = {
    'en': os.path.join(VOCABULARIES_PATH, 'en_vocab_processed.pickle'),
    'fr': os.path.join(VOCABULARIES_PATH, 'fr_vocab_processed.pickle'),
    'el': os.path.join(VOCABULARIES_PATH, 'el_vocab_processed.pickle'),
}
