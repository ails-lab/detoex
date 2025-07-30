from openai import OpenAI

from detoex.utils.settings import LLAMA_URL, API_KEY, LLM_ENDPOINTS, LANGUAGE_CODES


def prompt_llama(system_prompt: str, user_prompt: str, system_args: list[str] = (), 
                user_args: list[str] = (), language: str = 'en') -> str:
    """
    Send a prompt to the language model using the appropriate endpoint based on the language.
    
    Args:
        system_prompt: The system prompt template
        user_prompt: The user prompt template
        system_args: Arguments to format into the system prompt
        user_args: Arguments to format into the user prompt
        language: The language code ('en', 'fr', 'el')
        
    Returns:
        The LLM response as a string
    """
    # Validate language code
    if language not in LANGUAGE_CODES:
        raise ValueError(f"Unsupported language: {language}. Must be one of: {', '.join(LANGUAGE_CODES)}")
    
    # Get language-specific endpoint configuration
    endpoint_config = LLM_ENDPOINTS.get(language, LLM_ENDPOINTS['en'])  # Default to English if not found
    print(endpoint_config)
    
    # Create OpenAI client with language-specific settings
    client = OpenAI(
        api_key=endpoint_config['api_key'],
        base_url=endpoint_config['url']
    )
    
    args = {
        'model': endpoint_config['model'],
        'stop': ['<|eot_id|>'],
        'temperature': 0,
        'max_tokens': 4096,
        'messages': [
            {'role': 'system', 'content': system_prompt.format(*system_args)},
            {'role': 'user', 'content': user_prompt.format(*user_args)}
        ]
    }
    print(args)
    response = client.chat.completions.create(**args)
    return response.choices[0].message.content