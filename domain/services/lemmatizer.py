from mawo_pymorphy3 import get_global_analyzer
from domain.value_objects.word import Word
from functools import lru_cache
from ..constans.verb_ending import VERB_ENDINGS


class RussianLemmatizer:
    def __init__(self) -> None:
        self._analyzer = get_global_analyzer()
        self.verb_endings = VERB_ENDINGS

    @lru_cache(maxsize=10000)
    def get_lemma(self, word_text: str) -> Word:
        word_lower = word_text.lower()
        parses = self._analyzer.parse(word_lower)

        if not parses:
            return Word(word_text)

        sorted_parses = sorted(parses, key=lambda p: p.score, reverse=True)
        has_verb = any("VERB" in str(p.tag) for p in sorted_parses)

        if has_verb and self._looks_like_verb(word_lower):
            for p in sorted_parses:
                if "VERB" in str(p.tag) or "INFN" in str(p.tag):
                    best_parse = p
                    break
            else:
                best_parse = sorted_parses[0]
        else:
            best_parse = sorted_parses[0]

        tag_str = str(best_parse.tag)
        if (
                "VERB" in tag_str
                or "INFN" in tag_str
                or "PRTS" in tag_str
                or "GRND" in tag_str
        ):
            for form in best_parse.lexeme:
                if "INFN" in str(form.tag):
                    return Word(form.normal_form)

        return Word(best_parse.normal_form)

    def _looks_like_verb(self, word: str) -> bool:
        return any(word.endswith(end) for end in self.verb_endings)
