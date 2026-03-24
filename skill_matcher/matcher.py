import spacy
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
from typing import List, Set

nlp = spacy.load("en_core_web_lg")
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)


def clean_raw_skills(raw_skills: List[str]) -> List[str]:
    cleaned = []

    for skill in raw_skills:
        if not skill:
            continue

        s = skill.lower().strip()

        if len(s) <= 2:
            continue

        if "ai machine" in s:
            s = "machine learning"
        if "programming e" in s:
            s = "programming"

        cleaned.append(s)

    return cleaned


def extract_skills(text: str) -> Set[str]:
    if not text or len(text.strip()) < 5:
        return set()

    try:
        annotations = skill_extractor.annotate(text)

        return {
            match["doc_node_value"].lower().strip()
            for match in annotations["results"]["full_matches"]
        }

    except Exception:
        return set()


def normalize_user_skills(raw_skills: List[str]) -> Set[str]:
    if not raw_skills:
        return set()

    cleaned = clean_raw_skills(raw_skills)
    text = ", ".join(cleaned)

    extracted = extract_skills(text)

    fallback = {
        s for s in cleaned
        if s in {"programming", "app development"}
    }

    return extracted | fallback
