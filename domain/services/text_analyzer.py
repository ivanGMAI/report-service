from typing import Dict, AsyncIterator
from domain.value_objects.word import Word
from domain.value_objects.line_number import LineNumber
from domain.entities.word_statistics import WordStatistics
from domain.services.lemmatizer import RussianLemmatizer
import re


class TextAnalyzer:
    def __init__(self, lemmatizer: RussianLemmatizer, min_word_length: int = 2):
        self.lemmatizer = lemmatizer
        self.min_word_length = min_word_length
        self.stats: Dict[str, WordStatistics] = {}
        self.total_lines = 0

        self.word_pattern = re.compile(
            r"^[а-яё]+$|" r"^[А-ЯЁ]{2,}$|" r"^[а-яё]+-[а-яё]+$", re.IGNORECASE
        )

    async def analyze(self, lines: AsyncIterator[str]) -> Dict[str, WordStatistics]:
        self.stats.clear()
        line_number = 0

        async for line_text in lines:
            line_text = line_text.strip()
            if not line_text:
                line_number += 1
                continue

            words = line_text.split()

            for word_text in words:
                cleaned = re.sub(r"[^\w\-]", "", word_text)
                if not cleaned:
                    continue

                if not self.word_pattern.match(cleaned):
                    continue

                if len(cleaned) < self.min_word_length:
                    continue

                word_lower = cleaned.lower()

                lemma_word = self.lemmatizer.get_lemma(word_lower)
                lemma_text = str(lemma_word)

                if lemma_text not in self.stats:
                    self.stats[lemma_text] = WordStatistics(word=Word(lemma_text))

                self.stats[lemma_text].add_occurrence(LineNumber(line_number))

            line_number += 1

        self.total_lines = line_number
        return self.stats.copy()

    def get_total_lines(self) -> int:
        return self.total_lines
