def calculate_skill_score(resume_skills, jd_skills):

    matched = []

    for skill in jd_skills:

        if skill in resume_skills:
            matched.append(skill)

    if len(jd_skills) == 0:
        return 0, [], []

    score = int((len(matched) / len(jd_skills)) * 100)

    missing = []

    for skill in jd_skills:

        if skill not in resume_skills:
            missing.append(skill)

    return score, matched, missing
