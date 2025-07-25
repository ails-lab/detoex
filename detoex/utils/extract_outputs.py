import re


def extract_non_term_output(response: str, language: str = 'en') -> (bool, str):
    decision_match = re.search(r'<DECISION>\s*(.*?)\s*</DECISION>', response, re.DOTALL)
    if decision_match is None:
        decision = False
    elif language == 'en':
        decision = decision_match.group(1).strip() in ['["Toxic"]', '"Toxic"', 'Toxic']
    elif language == 'fr':
        decision = decision_match.group(1).strip() in ['"Toxique"', 'Toxique', '["Toxique"]']
    elif language == 'el':
        decision = decision_match.group(1).strip() in ['["Τοξικό"]', '"Τοξικό"']
    else:
        raise ValueError('Wrong language code: {}'.format(language))
    pattern = r'<(?:EXPLANATION|REASONING|REFLECTION)>\s*(.*?)(?:\s*</(?:EXPLANATION|REASONING|REFLECTION)>|$)'
    explanation_match = re.search(pattern, response, re.DOTALL)
    explanation = explanation_match.group(1).strip() if explanation_match else None
    return decision, explanation


def extract_term_output(response, language='en'):
    def extract_step(step_num):
        pattern = rf'<STEP_{step_num}>\s*(.*?)(?:\s*</STEP_{step_num}>|$)'
        match = re.search(pattern, response, re.DOTALL)
        return match.group(1).strip() if match else None

    decision, explanation = extract_step(3), extract_step(4)
    if language == 'en':
        decision = re.search(r"((non)|(not)|(n't)).*toxic", decision.lower()) is None
    elif language == 'fr':
        decision = re.search(r"((non)|(ne)|(n'est)).*toxique", decision.lower()) is None
    elif language == 'el':
        decision = decision == 'Τοξική'
    else:
        raise ValueError('Wrong language code: {}'.format(language))

    return decision, explanation


# def extract_fusion_output():
#     pass
