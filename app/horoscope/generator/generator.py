from app.horoscope.model import TextModel
from app.horoscope.text_enhancer import TextEnhancer

__all__ = [
    'HoroscopeGenerator',
]


class HoroscopeGenerator:
    __STOP_START = ('Однако', 'Но')

    def __init__(self, model: TextModel, enhancer: TextEnhancer):
        self.__model = model
        self.__enhancer = enhancer

    async def generate(self) -> str:
        sentence = self.__model.generate(stop_start=self.__STOP_START)
        enhanced_sentence = await self.__enhancer.enhance(sentence)
        return enhanced_sentence
