import pickle
from collections import OrderedDict
from pprint import pprint

import stanza

from detoex.api_modules.matching_module import find_matches
from detoex.utils.extract_outputs import extract_non_term_output, extract_term_output
from detoex.utils.prompt_llama import prompt_llama
from detoex.utils.settings import (STANZA_MODELS_KWARGS, LANGUAGE_CODES, PROCESSED_TERMS_FILEPATHS,
                                   NON_TERM_PROMPTS, TERM_PROMPTS, FUSION_PROMPTS)


lang_to_model = {
    lang: stanza.Pipeline(lang, **STANZA_MODELS_KWARGS[lang])
    for lang in LANGUAGE_CODES
}

lang_to_term = {}

for lang in LANGUAGE_CODES:
    with open(PROCESSED_TERMS_FILEPATHS[lang], 'rb') as fp:
        lang_to_term[lang] = pickle.load(fp)


def non_term_pipeline(texts, language='en') -> list[str | None]:
    explanations = []
    prompts = NON_TERM_PROMPTS[language]
    system_prompt = prompts['system_prompt']
    user_prompt = prompts['user_prompt']
    for text in texts:
        response = prompt_llama(system_prompt, user_prompt, user_args=[text], language=language)
        decision, explanation = extract_non_term_output(response, language=language)
        explanations.append(explanation if decision else None)
    return explanations


def term_based_pipeline(texts, language='en') -> list[list[str]]:
    # Load model from memory
    if language in lang_to_model:
        nlp = lang_to_model[language]
    elif language not in LANGUAGE_CODES:
        raise ValueError('lang code not supported\n lang code must be one of '
                         + ', '.join(list(LANGUAGE_CODES)))

    if language in lang_to_term:
        terms = lang_to_term[language]
    else:
        raise ValueError('lang code not supported\n lang code must be one of '
                         + ', '.join(list(LANGUAGE_CODES)))

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
    matches_by_text = list(zip(texts, matches_by_text))
    print(matches_by_text)

    explanations_by_text = []
    prompts = TERM_PROMPTS[language]
    system_prompt = prompts['system_prompt']
    user_prompt = prompts['user_prompt']
    for text, matches in matches_by_text:
        explanations = []
        for match in matches:
            response = prompt_llama(system_prompt, user_prompt,
                                    user_args=[match.term_literal, match.issue_description, text, match.categories],
                                    language=language)
            decision, explanation = extract_term_output(response, language=language)
            if decision:
                explanations.append(explanation)
        explanations_by_text.append(explanations)
    pprint(explanations_by_text)
    return explanations_by_text


def fuse_explanations(explanations: list[str], language: str = 'en') -> str:
    if len(explanations) == 0:
        return ''
    if len(explanations) == 1:
        return explanations[0]

    prompts = FUSION_PROMPTS[language]
    system_prompt = prompts['system_prompt']
    user_prompt = prompts['user_prompt']

    formatted_explanations = []
    for i, explanation in enumerate(explanations, 1):
        formatted_explanations.append(f"**Text {i}:** {explanation}")
    formatted_explanations = "\n".join(formatted_explanations)
    return prompt_llama(system_prompt, user_prompt, user_args=[formatted_explanations], language=language)


def detect_and_explain(texts: list[str], language: str = 'en') -> list[str]:
    explanation1 = non_term_pipeline(texts, language=language)
    print(explanation1)
    explanation2 = term_based_pipeline(texts, language=language)
    final_explanation = [fuse_explanations([e1] + e2, language=language) if e1
                         else fuse_explanations(e2, language=language)
                         for e1, e2 in zip(explanation1, explanation2)]
    return final_explanation
