import os
from typing import Annotated

from fastapi import Header, Depends, HTTPException
import hmac
import hashlib
import base64
from urllib.parse import parse_qs, urlparse

SECRET_KEY = os.environ.get("SECRET_KEY")


def verify_signature(url: str, secret_key: str) -> bool:
    parsed_url = urlparse(url)
    url_params = parse_qs(parsed_url.query)

    if 'sign_keys' not in url_params or 'sign' not in url_params:
        return False

    sign_keys = url_params['sign_keys'][0].split(',')
    ordered_params = {key: url_params[key][0] for key in sign_keys}

    # Формируем строку вида "param_name1=value&param_name2=value"
    string_params = "&".join(f"{key}={value}" for key, value in ordered_params.items())

    # Получаем хеш-код от строки, используя секретный ключ. Генерация на основе метода HMAC.
    hash_signature = hmac.new(bytes(secret_key, 'utf-8'), msg=bytes(string_params, 'utf-8'), digestmod=hashlib.sha256).digest()
    sign = base64.urlsafe_b64encode(hash_signature).decode('utf-8').rstrip("=")

    return sign == url_params['sign'][0]


class InitData:
    def __init__(self, load_url: str):
        # todo парсинг строки в параметры
        pass


async def parse_launch_params(load_url: str = Header(..., title="URL запуска приложения")) -> InitData:

    if SECRET_KEY and not verify_signature(load_url, SECRET_KEY):
        raise HTTPException(401, "Invalid load url")

    return InitData(load_url)


HeaderInitParams = Annotated[InitData, Depends(parse_launch_params)]
