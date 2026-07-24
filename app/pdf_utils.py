import io

from fastapi import UploadFile, HTTPException
from pypdf import PdfReader


async def load_resume_pdf(resume: UploadFile):
    try:
        pdf_bytes = await resume.read()

        reader = PdfReader(io.BytesIO(pdf_bytes))

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="The uploaded PDF contains no readable text."
            )

        return text

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to read the uploaded PDF."
        )