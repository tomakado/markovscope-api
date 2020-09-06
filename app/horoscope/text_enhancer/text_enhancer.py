import logging
from abc import ABCMeta

import aiohttp
import ujson

__all__ = [
    'TextEnhancer',
    'YandexTranslateTextEnhancer',
]

LOG = logging.getLogger(__name__)


class TextEnhancer(metaclass=ABCMeta):
    async def enhance(self, text: str) -> str:
        raise NotImplementedError


class YandexTranslateTextEnhancer(TextEnhancer):
    __API_ENDPOINT = 'https://translate.api.cloud.yandex.net/translate/v2/translate'
    __IAM_ENDPOINT = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'

    def __init__(self, oauth_token: str, folder_id: str):
        # self.__iam_token = iam_token
        self.__oauth_token = oauth_token
        self.__folder_id = folder_id

    async def enhance(self, text: str) -> str:
        en_text = await self.__translate_to(text, 'en')
        if len(en_text) == 0:
            return ''

        ru_text = await self.__translate_to(en_text, 'ru')

        return ru_text

    async def __get_iam_token(self) -> str:
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            async with session.post(
                    self.__IAM_ENDPOINT,
                    json={
                        'yandexPassportOauthToken': self.__oauth_token,
                    },
            ) as res:
                json_body = await res.json()
                LOG.debug('Got response from Yandex Cloud API: {}'.format(json_body))
                return json_body['iamToken']

    async def __translate_to(self, text: str, target_lang: str) -> str:
        # TODO Raise exception on failure
        iam_token = await self.__get_iam_token()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {iam_token}',
        }
        body = {
            'folder_id': self.__folder_id,
            'texts': [text],
            'targetLanguageCode': target_lang,
        }

        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            async with session.post(
                    self.__API_ENDPOINT,
                    headers=headers,
                    json=body,
            ) as res:
                json_body = await res.json()
                LOG.debug('Response from Yandex Translate API: {}'.format(json_body))
                result = ''
                try:
                    result = json_body['translations'][0]['text']
                except KeyError:
                    LOG.exception('No result. API response: {}'.format(json_body))
                    pass
                except Exception as e:
                    LOG.exception('Error occurred: {}'.format(e))

                return result
