import re
from typing import Set
from transformers import GPT2TokenizerFast

from nltk.tokenize import sent_tokenize

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")


def __count_tokens(text: str) -> int:
    """count the number of tokens in a string"""
    return len(tokenizer.encode(text))


def __reduce_long(
        long_text: str, long_text_tokens: bool = False, max_len: int = 590
) -> str:
    """
    Reduce a long text to a maximum of `max_len` tokens by potentially cutting at a sentence end
    """
    if not long_text_tokens:
        long_text_tokens = __count_tokens(long_text)
    if long_text_tokens > max_len:
        sentences = sent_tokenize(long_text.replace("\n", " "))
        ntokens = 0
        for i, sentence in enumerate(sentences):
            ntokens += 1 + __count_tokens(sentence)
            if ntokens > max_len:
                return ". ".join(sentences[:i][:-1]) + "."

    return long_text


discard_categories_en_pl = ('See also', 'References', 'External links', 'Further reading', "Footnotes",
                            "Bibliography", "Sources", "Citations", "Literature", "Footnotes", "Notes and references",
                            "Photo gallery", "Works cited", "Photos", "Gallery", "Notes", "References and sources",
                            "References and notes",
                            'Zobacz też', 'Przypisy', 'Bibliografia', 'Linki zewnętrzne', 'Uwagi',
                            'W literaturze pięknej',
                            'Literatura uzupełniająca', 'Galeria', 'Inne opracowania',
                            )


def extract_sections(
        wiki_text: str,
        title: str,
        max_len: int = 1500,
        discard_categories: Set[str] = discard_categories_en_pl,
) -> list[tuple[str, str, str, int]]:
    """
    Extract the sections of a Wikipedia page, discarding the references and other low information sections
    """
    if len(wiki_text) == 0:
        return []

    # find all headings and the corresponding contents
    headings = re.findall("==+ .* ==+", wiki_text)
    for heading in headings:
        wiki_text = wiki_text.replace(heading, "==+ !! ==+")
    contents = wiki_text.split("==+ !! ==+")
    contents = [c.strip() for c in contents]
    assert len(headings) == len(contents) - 1

    cont = contents.pop(0).strip()
    outputs = [(title, "Summary", cont, __count_tokens(cont) + 4)]

    # discard the discard categories, accounting for a tree structure
    max_level = 100
    keep_group_level = max_level
    remove_group_level = max_level
    nheadings, ncontents = [], []
    for heading, content in zip(headings, contents):
        plain_heading = " ".join(heading.split(" ")[1:-1])
        num_equals = len(heading.split(" ")[0])
        if num_equals <= keep_group_level:
            keep_group_level = max_level

        if num_equals > remove_group_level:
            if (
                    num_equals <= keep_group_level
            ):
                continue
        keep_group_level = max_level
        if plain_heading in discard_categories:
            remove_group_level = num_equals
            keep_group_level = max_level
            continue
        nheadings.append(heading.replace("=", "").strip())
        ncontents.append(content)
        remove_group_level = max_level

    # count the tokens of each section
    ncontent_ntokens = [
        __count_tokens(c)
        + 3
        + __count_tokens(" ".join(h.split(" ")[1:-1]))
        - (1 if len(c) == 0 else 0)
        for h, c in zip(nheadings, ncontents)
    ]

    # Create a tuple of (title, section_name, content, number of tokens)
    outputs += [(title, h, c, t) if t < max_len
                else (title, h, __reduce_long(c, max_len=max_len), __count_tokens(__reduce_long(c, max_len=max_len)))
                for h, c, t in zip(nheadings, ncontents, ncontent_ntokens)]

    return outputs
