from hashlib import sha256
from random import Random
from typing import Callable, Final, TypeVar

vowels: Final = ("a", "e", "i", "o", "u")
consonants: Final = (
    "b",
    "d",
    "f",
    "g",
    "h",
    "j",
    "k",
    "l",
    "m",
    "n",
    "p",
    "r",
    "s",
    "t",
    "v",
    "w",
    "x",
    "z",
)
syllables: Final = tuple(c + v for c in consonants for v in vowels)


def random_name(generator: Random) -> str:
    syllable_count: Final = generator.randint(1, 4)
    basic_syllables: Final = generator.choices(syllables, k=syllable_count)
    modified_syllables: Final = (
        syl + generator.choice(("", generator.choice(consonants)))
        for syl in basic_syllables
    )
    return "".join(modified_syllables).capitalize()


NameT = TypeVar("NameT", bound=str)


def insensitive_sha256(name: str) -> bytes:
    """SHA256 but insensitive to enclosing whitespace and character case."""
    return sha256(name.strip().lower().encode()).digest()


def pseudonymize(
    name: NameT,
    hash_function: Callable[[NameT], bytes] = insensitive_sha256,
    min_subnames: int = 2,
    max_subnames: int = 3,
) -> str:
    if not (0 < min_subnames <= max_subnames):
        raise ValueError(
            "At least one subname is required. "
            "max_subnames can not be less than min_subnames."
        )

    seed: Final = hash_function(name)
    generator: Final = Random(seed)
    subname_count: Final = generator.randint(min_subnames, max_subnames)
    subnames: Final = (random_name(generator) for _ in range(subname_count))
    return " ".join(subnames)
