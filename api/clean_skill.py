# encoding: utf8

import re
import html


def clean_skill(skill, remove_stopwords=True):
    """Clean and normalize skill/technology names.

    Args:
        skill: Raw skill name to clean
        remove_stopwords: Whether to remove common stopwords

    Returns:
        str: Cleaned and normalized skill name
    """
    skill = str(skill)
    skill = html.unescape(skill)

    skill = skill.replace("_", " ").split()
    skill = " ".join([sk for sk in skill if sk])

    skill = re.sub(r"\(.*\)", "", skill)
    skill = (
        skill.replace("-", "")
        .replace("(", "")
        .replace(".", "")
        .replace(",", "")
        .replace("-", "")
        .replace(":", "")
        .replace(")", "")
        .replace("åá", "")
        .replace("&", "and")
        .replace(" js", "js")
        .replace("-js", "js")
        .replace("_js", "js")
        .replace("java script", "js")
    )

    skill = skill.lower()

    # Special cases replace
    alias_string = {}
    alias_string["javascript"] = ["js", "java script", "javascripts", "java scrip"]
    alias_string["wireframe"] = [
        "wireframes",
        "wire frame",
        "wire frames",
        "wire-frame",
        "wirefram",
        "wire fram",
        "wireframing",
    ]
    alias_string["aws"] = [
        "amazon web service",
    ]
    alias_string["OOP"] = [
        "object oriented",
        "object oriented programming",
    ]
    alias_string["osx"] = ["mac os x", "os x"]
    alias_string["OOD"] = [
        "object oriented design",
    ]
    alias_string["OLAP"] = [
        "online analytical processing",
    ]
    alias_string["Ecommerce"] = [
        "e commerce",
    ]
    alias_string["consultant"] = [
        "consulting",
    ]
    alias_string["ux"] = [
        "user experience",
        "web user experience design",
        "user experience design",
        "ux designer",
        "user experience/ux",
    ]
    alias_string["html5"] = [
        "html 5",
    ]
    alias_string["bigdata"] = [
        "big data",
    ]
    alias_string["j2ee"] = [
        "jee",
    ]
    alias_string["senior"] = ["sr"]
    alias_string["qa"] = [
        "quality",
    ]
    alias_string["nlp"] = ["natural language process", "natural language", "nltk"]
    alias_string["bigdata"] = [
        "big data",
    ]
    alias_string["webservice"] = ["webservices", "website", "webapps"]
    alias_string["xml"] = ["xml file", "xml schemas", "xml/json", "xml web service"]

    for root_skill in alias_string:
        if skill in alias_string[root_skill]:
            skill = root_skill

    # Special case regex
    alias_string_regex = {
        r"^angular.*$": "angularjs",
        r"^node.*$": "nodejs",
        r"^(.*)[_\s]js$": "\\1js",
        r"^(.*) js$": "\\1js",
        r"^(.*) (and|or).*$": "\\1",
    }
    for regex_rule in alias_string_regex:
        after_skill = re.sub(regex_rule, alias_string_regex[regex_rule], skill)
        if after_skill != skill:
            skill = after_skill
            break

    # skill stopwords
    if remove_stopwords:
        skill_stopwords = [
            "app",
            "touch",
            "the",
            "application",
            "programming",
            "program",
            "design" "developer",
            "framework",
            "development",
            "programmer",
            "technologies",
            "advance",
            "core",
            "include",
        ]
        skill_after = skill.split(" ")
        skill = " ".join([sk for sk in skill_after if sk not in skill_stopwords])

    # NOTE: replace js tail
    skill = re.sub("js$", "", skill)

    try:
        skill = skill.split("/")
        skill = skill[0]
    except:
        pass
    try:
        skill = skill.split(";")
        skill = skill[0]
    except:
        pass

    skill = skill.lower().strip().replace(" ", "_")
    skill = re.sub(" +", " ", skill)
    skill = skill.strip()

    # Is number
    if skill.isdigit():
        return ""

    return skill
