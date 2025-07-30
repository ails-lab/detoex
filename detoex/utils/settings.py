import os
import json


API_KEY = 'dummy-key'
LLAMA_URL = 'http://localhost:8080/v1'

# Language-specific LLM endpoints
LLM_ENDPOINTS = {
    'en': {
        'url': os.getenv('LLM_URL_EN', LLAMA_URL),
        'api_key': os.getenv('LLM_API_KEY_EN', API_KEY),
        'model': os.getenv('LLM_MODEL_EN', 'llama'),
    },
    'fr': {
        'url': os.getenv('LLM_URL_FR', LLAMA_URL),
        'api_key': os.getenv('LLM_API_KEY_FR', API_KEY),
        'model': os.getenv('LLM_MODEL_FR', 'llama'),
    },
    'el': {
        'url': os.getenv('LLM_URL_EL', LLAMA_URL),
        'api_key': os.getenv('LLM_API_KEY_EL', API_KEY),
        'model': os.getenv('LLM_MODEL_EL', 'llama'),
    },
}


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
        'dir': STANZA_RESOURCES_DIR,
    },
    'fr': {
        'download_method': 'reuse_resources',
        'processors': 'tokenize, mwt, pos, lemma',
        'package': 'default_accurate',
        'dir': STANZA_RESOURCES_DIR,
    },
    'el': {
        'download_method': 'reuse_resources',
        'processors': 'tokenize, mwt, pos, lemma',
        'package': 'default_accurate',
        'dir': STANZA_RESOURCES_DIR,
    }
}

LANGUAGE_CODES = [
    'en',
    'fr',
    'el',
]

PROCESSED_TERMS_FILEPATHS = {
    'en': os.path.join(VOCABULARIES_DIR, 'en_vocab_processed.pickle'),
    'fr': os.path.join(VOCABULARIES_DIR, 'fr_vocab_processed.pickle'),
    'el': os.path.join(VOCABULARIES_DIR, 'el_vocab_processed.pickle'),
}
