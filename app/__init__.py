import json
from typing import Dict

import pandas as pd
from aiohttp import web

from app.config import CONFIG
from app.horoscope.generator.generator import HoroscopeGenerator
from app.horoscope.model import TextModel
from app.horoscope.text_enhancer import YandexTranslateTextEnhancer


class MarkovscopeApplication:
    __SUN_SIGNS = [
        "aries",
        "taurus",
        "gemini",
        "cancer",
        "leo",
        "virgo",
        "libra",
        "scorpio",
        "sagittarius",
        "capricorn",
        "aquarius",
        "pisces",
    ]

    def __init__(self):
        self.__app = web.Application()
        self.__models: Dict[str, TextModel] = {
            sign: TextModel()
            for sign in self.__SUN_SIGNS
        }

        self.__setup_generators()
        self.__setup_routes()

    def __setup_generators(self) -> None:
        data = pd.read_csv(CONFIG.data_path, header=None)

        for sign in self.__SUN_SIGNS:
            data_subset = data[data[0] == sign][2].tolist()
            corpora = "\n".join(data_subset)

            self.__models[sign].train(corpora)

        text_enhancer = YandexTranslateTextEnhancer(
            oauth_token=CONFIG.yc_oauth_token,
            folder_id=CONFIG.yc_folder_id,
        )

        self.__generators = {
            sign: HoroscopeGenerator(model, text_enhancer)
            for sign, model in self.__models.items()
        }

    def __setup_routes(self) -> None:
        self.__app.add_routes([
            web.get('/', self.handle_generate_all),
            web.get('/{sign}', self.handle_generate_for_sign),
        ])

    async def handle_generate_all(self, request: web.Request):
        horoscopes = list()
        for sign, generator in self.__generators.items():
            text = await generator.generate()
            horoscopes.append({
                'sun_sign': sign,
                'text': text,
            })

        response = {
            'status': 'ok',
            'result': horoscopes,
        }

        return web.Response(
            content_type='application/json',
            text=json.dumps(response)
        )

    async def handle_generate_for_sign(self, request: web.Request):
        sign = request.match_info.get('sign')
        if sign not in self.__SUN_SIGNS:
            return web.Response(
                content_type='application/json',
                text=json.dumps({
                    'status': 'error',
                    'message': 'unknown sun sign',
                }),
                status=404,
            )

        generator = self.__generators[sign]
        text = await generator.generate()

        return web.Response(
            content_type='application/json',
            text=json.dumps({
                'status': 'ok',
                'sun_sign': sign,
                'text': text,
            })
        )

    def start(self):
        web.run_app(
            host=CONFIG.listen_host,
            port=CONFIG.listen_port,
            app=self.__app,
        )
