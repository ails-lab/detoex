from openai import OpenAI

from detoex.utils.settings import LLAMA_URL, API_KEY


def prompt_llama(system_prompt: str, user_prompt: str, system_args: list[str] = (), user_args: list[str] = ())\
        -> str:
    client = OpenAI(
        api_key=API_KEY,
        base_url=LLAMA_URL
    )
    args = {
        'model': 'llama',
        'stop': ['<|eot_id|>'],
        'temperature': 0,
        'max_tokens': 4096,
        'messages': [
            {'role': 'system', 'content': system_prompt.format(*system_args)},
            {'role': 'user', 'content': user_prompt.format(*user_args)}
        ]
    }
    print(args['messages'])
    response = client.chat.completions.create(**args)
    return response.choices[0].message.content
