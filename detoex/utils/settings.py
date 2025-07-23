import os
import json


API_KEY = 'dummy-key'
LLAMA_URL = 'http://localhost:8080/v1'


LLM_PROMPTS_DIR = os.getenv('LLM_PROMPTS_DIR')

with open(os.path.join(LLM_PROMPTS_DIR, 'non_term_prompts.json'), 'rt') as fp:
    NON_TERM_PROMPTS = json.load(fp)
with open(os.path.join(LLM_PROMPTS_DIR, 'term_prompts.json'), 'rt') as fp:
    TERM_PROMPTS = json.load(fp)
with open(os.path.join(LLM_PROMPTS_DIR, 'fusion_prompts.json'), 'rt') as fp:
    FUSION_PROMPTS = json.load(fp)

STANZA_RESOURCES_DIR = os.getenv('STANZA_RESOURCES_DIR')
VOCABULARIES_DIR = os.getenv('VOCABULARIES_DIR')

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
    # 'en': os.path.join(VOCABULARIES_DIR, 'en_vocab_processed.pickle'),
    # 'fr': os.path.join(VOCABULARIES_DIR, 'fr_vocab_processed.pickle'),
    # 'el': os.path.join(VOCABULARIES_DIR, 'el_vocab_processed.pickle'),
}
