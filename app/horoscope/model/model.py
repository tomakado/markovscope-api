import markovify


class TextModel:
    def __init__(self):
        self.__model: markovify.Text = None

    def train(self, corpora: str, state_size=3):
        self.__model = markovify.NewlineText(corpora, state_size=state_size)

    def load_from_dict(self, data: dict):
        self.__model = markovify.Text.from_dict(data)

    def generate(self, min_words=15, max_words=100, tries=1000, stop_start='') -> str:
        sentence = self.__model.make_sentence(
            min_words=min_words,
            max_words=max_words,
            tries=tries,
        )

        if sentence.startswith(stop_start):
            return self.generate()

        return sentence
