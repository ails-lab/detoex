import re


def extract_non_term_output(response: str, language: str = 'en') -> (bool, str):
    decision_match = re.search(r'<DECISION>\s*(.*?)\s*</DECISION>', response, re.DOTALL)
    if decision_match is None:
        decision = False
    elif language == 'en':
        decision = decision_match.group(1).strip() in ['["Toxic"]', '"Toxic"', 'Toxic']
    explanation = None
    explanation_match = re.search(r'((<EXPLANATION>)|(<REASONING>)|(<REFLECTION>))\s*(.*?)\s*</EXPLANATION>', response,
                                  re.DOTALL)
    if explanation_match:
        explanation = explanation_match.group(5).strip()
    else:
        explanation_match = re.search(r'<REASONING>\s*(.*?)\s*</EXPLANATION>', response, re.DOTALL)
        if explanation_match:
            explanation = explanation_match.group(1).strip()
        else:
            explanation_match = re.search(r'((<REASONING>)|(<EXPLANATION>)|<REFLECTION>)\s*(.*)', response, re.DOTALL)
            if explanation_match:
                explanation = explanation_match.group(4).strip()
                explanation = re.sub(r'\s*(</REASONING>)|(</EXPLANATION>)|(</REFLECTION>)\s*$', '', explanation).strip()
            else:
                print(response)
    return (decision, explanation)


def extract_term_output():
    pass


def extract_fusion_output():
    pass
