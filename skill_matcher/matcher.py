import spacy
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
from typing import List, Set

nlp = spacy.load("en_core_web_lg")
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)


def extract_skills(text: str) -> Set[str]:
    if not text or len(text.strip()) < 5:
        return set()
    try:
        annotations = skill_extractor.annotate(text)
        skills = set()
        for match in annotations["results"]["full_matches"]:
            skills.add(match["doc_node_value"].lower())
        for match in annotations["results"]["ngram_scored"]:
            if match["score"] > 0.7:
                skills.add(match["doc_node_value"].lower())
        return skills
    except Exception:
        return set()


def normalize_user_skills(raw_skills: List[str]) -> Set[str]:
    if not raw_skills:
        return set()
    text = "experienced in " + ", ".join([s for s in raw_skills if s])
    return extract_skills(text)


def compute_match(job: dict, user_skills: Set[str]) -> dict:
    if not user_skills:
        job["matchScore"] = 0.0
        job["matchedSkills"] = []
        job["missingSkills"] = []
        return job

    title = job.get("title", "")
    desc = job.get("description", "")
    query = job.get("skillMatched") or ""
    text = f"{title} {desc} {query}"

    job_skills = extract_skills(text)

    if not job_skills:
        job["matchScore"] = 0.0
        job["matchedSkills"] = []
        job["missingSkills"] = []
        return job

    matched = job_skills & user_skills
    missing = job_skills - user_skills

    job["matchScore"] = round(len(matched) / len(job_skills), 2)
    job["matchedSkills"] = list(matched)
    job["missingSkills"] = list(missing)
    return job