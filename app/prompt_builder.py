from app.pdf_utils import load_resume_pdf


def load_prompt():
    with open("prompts/resume_prompt.txt", "r", encoding="utf-8") as file:
        return file.read()


async def build_prompt(resume, job_description):
    prompt = load_prompt()
    resume_text = await load_resume_pdf(resume)

    return f"""{prompt}

Job Description:
{job_description}

Resume:
{resume_text}
"""