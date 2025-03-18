import pandas as pd
import statistics
import nltk
from collections import Counter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from cachetools import TTLCache
from app.models import Note


class NoteAnalytics:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.cache = TTLCache(maxsize=50, ttl=300)

    async def _update_cache_if_needed(self):
        last_updated = await self.db.execute(select(func.max(Note.created_at)))
        current_timestamp = last_updated.scalar()

        if self.cache.get("last_updated") != current_timestamp:
            self.cache.clear()
            self.cache["last_updated"] = current_timestamp

    async def get_word_count(self) -> int:
        await self._update_cache_if_needed()
        if "word_count" in self.cache:
            return self.cache["word_count"]

        result = await self.db.execute(
            select(func.sum(func.length(Note.content) - func.length(func.replace(Note.content, " ", "")) +1))
        )
        total_words = result.scalar() or 0
        self.cache["word_count"] = total_words
        return total_words

    async def get_average_length(self) -> float:
        await self._update_cache_if_needed()
        if "avg_length" in self.cache:
            return self.cache["avg_length"]

        result = await self.db.execute(select(func.avg(func.length(Note.content))))
        avg_length = result.scalar() or 0
        self.cache["avg_length"] = avg_length
        return avg_length

    async def get_most_common_words(self, top_n: int = 10) -> list[str]:
        await self._update_cache_if_needed()
        if "common_words" in self.cache:
            return self.cache["common_words"]

        result = await self.db.execute(select(func.unnest(func.string_to_array(func.lower(Note.content), ' '))))
        words = [row[0] for row in result.all() if row[0].isalnum()]

        most_common = Counter(words).most_common(top_n)
        common_words = [word for word, _ in most_common]
        self.cache["common_words"] = common_words
        return common_words

    async def get_top_notes(self) -> dict:
        await self._update_cache_if_needed()
        if "top_notes" in self.cache:
            return self.cache["top_notes"]

        result = await self.db.execute(select(Note.id, Note.content))
        notes = [(row[0], row[1] or '') for row in result.all()]

        df = pd.DataFrame(notes, columns=["id", "content"])
        df["length"] = df["content"].apply(len)

        longest_notes = df.nlargest(3, "length")[["id", "length"]].to_dict(orient="records")
        shortest_notes = df.nsmallest(3, "length")[["id", "length"]].to_dict(orient="records")

        result = {"longest": longest_notes, "shortest": shortest_notes}
        self.cache["top_notes"] = result
        return result

    async def get_character_count(self) -> int:
        await self._update_cache_if_needed()
        if "char_count" in self.cache:
            return self.cache["char_count"]

        result = await self.db.execute(select(func.sum(func.length(Note.content))))
        char_count = result.scalar() or 0
        self.cache["char_count"] = char_count
        return char_count

    async def get_median_length(self) -> float:
        await self._update_cache_if_needed()
        if "median_length" in self.cache:
            return self.cache["median_length"]

        result = await self.db.execute(select(func.length(Note.content)))
        lengths = [row[0] for row in result.all()]

        median_length = statistics.median(lengths) if lengths else 0
        self.cache["median_length"] = median_length
        return median_length

    async def get_common_bigrams(self, top_n: int = 10) -> list[str]:
        await self._update_cache_if_needed()
        if "common_bigrams" in self.cache:
            return self.cache["common_bigrams"]

        result = await self.db.execute(select(func.unnest(func.string_to_array(func.lower(Note.content), ' '))))
        words = [row[0] for row in result.all()]

        bigrams = [" ".join(pair) for pair in zip(words, words[1:])]
        most_common = Counter(bigrams).most_common(top_n)

        result = [phrase for phrase, _ in most_common]
        self.cache["common_bigrams"] = result
        return result

    async def get_common_trigrams(self, top_n: int = 10) -> list[str]:
        await self._update_cache_if_needed()
        if "common_trigrams" in self.cache:
            return self.cache["common_trigrams"]

        result = await self.db.execute(select(func.unnest(func.string_to_array(func.lower(Note.content), ' '))))
        words = [row[0] for row in result.all()]

        trigrams = [" ".join(trio) for trio in zip(words, words[1:], words[2:])]
        most_common = Counter(trigrams).most_common(top_n)

        result = [phrase for phrase, _ in most_common]
        self.cache["common_trigrams"] = result
        return result
