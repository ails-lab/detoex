import pickle
from collections import OrderedDict

import stanza

from detoex.api_modules.matching_module import find_matches
from detoex.utils.settings import STANZA_MODELS_KWARGS, STARTUP_LANGUAGES, PROCESSED_TERMS_FILEPATHS


in_memory_models = OrderedDict({
    lang: stanza.Pipeline(lang, **STANZA_MODELS_KWARGS[lang])
    for lang in STARTUP_LANGUAGES
})

in_memory_terms = OrderedDict()

for lang in STARTUP_LANGUAGES:
    with open(PROCESSED_TERMS_FILEPATHS[lang], 'rb') as fp:
        in_memory_terms[lang] = pickle.load(fp)


def non_term_pipeline(texts, language='en') -> list[str | None]:
    pass


def term_based_pipeline(texts, language='en') -> list[str | None]:
    # Load model from memory
    if language in in_memory_models:
        nlp = in_memory_models[language]
        in_memory_models.move_to_end(language)
    elif language not in STANZA_MODELS_KWARGS:
        raise ValueError('lang code not supported\n lang code must be one of '
                         + ', '.join(list(STANZA_MODELS_KWARGS)))
    else:
        nlp = stanza.Pipeline(language, **STANZA_MODELS_KWARGS[language])
        in_memory_models.popitem(last=False)
        in_memory_models[language] = nlp

    if language in in_memory_terms:
        terms = in_memory_terms[language]
        in_memory_terms.move_to_end(language)
    else:
        with open(PROCESSED_TERMS_FILEPATHS[language], 'rb') as fp:
            terms = pickle.load(fp)
        in_memory_terms.popitem(last=False)
        in_memory_terms[language] = terms

    out_texts = nlp.bulk_process(texts)

    matches_by_text = []
    for text in out_texts:
        text_matches = []
        for sentence_id, sentence in enumerate(text.sentences):
            sentence_matches = find_matches(sentence, terms)
            for match in sentence_matches:
                match.text = text.text[match.start_char:match.end_char]
                match.sentence_index = sentence_id
            text_matches.extend(sentence_matches)
        matches_by_text.append(text_matches)
    matches_by_text = dict(zip(texts, matches_by_text))
    pass


def fuse_explanations(e1, e2) -> str:
    pass


def detect_and_explain(texts: list[str], language: str = 'en') -> list[str]:
    explanation1 = non_term_pipeline(texts, language=language)
    explanation2 = term_based_pipeline(texts, language=language)
    final_explanation = [fuse_explanations(e1, e2) if e1 and e2
                         else e1 if e1
                         else e2
                         for e1, e2 in zip(explanation1, explanation2)]
    return final_explanation
