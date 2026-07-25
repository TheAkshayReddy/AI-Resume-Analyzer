import requests
import streamlit as st

# -----------------------------
# Configuration
# -----------------------------
API_URL = "https://ai-resume-analyzer-cvyt.onrender.com/analyze"

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide",
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown(
    """
    <style>

    .main {
        padding-top: 20px;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    .title {
        text-align:center;
        font-size:42px;
        font-weight:bold;
        color:#2E86C1;
    }

    .subtitle {
        text-align:center;
        color:gray;
        margin-bottom:25px;
    }

    .section-header{
        font-size:24px;
        font-weight:bold;
        color:#1F618D;
        margin-top:20px;
        margin-bottom:10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("📌 Instructions")

    st.markdown("""
1. Upload your resume (PDF)

2. Paste the Job Description

3. Click **Analyze Resume**

4. Wait for AI Analysis

5. Review suggestions
""")

    st.divider()

    st.info(
        "This application compares your resume with a Job Description using Google's Gemini model."
    )

# -----------------------------
# Page Heading
# -----------------------------
st.markdown(
    "<div class='title'>🤖 AI Resume Analyzer</div>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='subtitle'>Match your resume against any job description using AI.</div>",
    unsafe_allow_html=True,
)

st.divider()

# -----------------------------
# Input Section
# -----------------------------
left, right = st.columns([1, 2])

with left:

    uploaded_file = st.file_uploader(
        "📄 Upload Resume (PDF)",
        type=["pdf"],
    )

with right:

    job_description = st.text_area(
        "📝 Job Description",
        height=250,
        placeholder="Paste the complete Job Description here...",
    )

analyze_button = st.button(
    "🚀 Analyze Resume",
    use_container_width=True,
)

st.divider()

# -----------------------------
# Helper Functions
# -----------------------------
def display_list(title, items):

    st.subheader(title)

    if not items:
        st.write("No data available.")
        return

    for item in items:
        st.markdown(f"- {item}")


def call_api(uploaded_file, job_description):

    files = {
        "resume": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "application/pdf",
        )
    }

    data = {
        "job_description": job_description
    }

    response = requests.post(
        API_URL,
        files=files,
        data=data
    )

    return response

# -----------------------------
# Analyze Button Logic
# -----------------------------
if analyze_button:

    # Validation
    if uploaded_file is None:
        st.error("Please upload a PDF resume.")
        st.stop()

    if not job_description.strip():
        st.error("Please enter the Job Description.")
        st.stop()

    with st.spinner("🤖 AI is analyzing your resume..."):

        try:

            response = call_api(
                uploaded_file,
                job_description,
            )

            if response.status_code != 200:

                try:
                    error_message = response.json().get(
                        "detail",
                        "Unknown error occurred."
                    )
                except Exception:
                    error_message = response.text

                st.error(f"API Error: {error_message}")
                st.stop()

            result = response.json()

        except requests.exceptions.ConnectionError:

            st.error(
                "Unable to connect to the FastAPI server.\n\n"
                "Make sure your FastAPI application is running."
            )
            st.stop()

        except requests.exceptions.RequestException as e:

            st.error(f"Request failed:\n\n{e}")
            st.stop()

        except Exception as e:

            st.error(f"Unexpected Error:\n\n{e}")
            st.stop()

    st.success("✅ Resume analyzed successfully!")

    st.divider()

    # -----------------------------
    # Match Score
    # -----------------------------
    st.markdown(
        "<div class='section-header'>🎯 Match Score</div>",
        unsafe_allow_html=True,
    )

    score = result.get("match_score", 0)

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            "Overall Match",
            f"{score}%"
        )

    with metric2:
        st.metric(
            "Matching Skills",
            len(result.get("matching_skills", []))
        )

    with metric3:
        st.metric(
            "Missing Skills",
            len(result.get("missing_skills", []))
        )

    st.progress(min(score / 100, 1.0))

    st.divider()

    # -----------------------------
    # Resume & Job Summary
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "<div class='section-header'>📄 Resume Summary</div>",
            unsafe_allow_html=True,
        )

        st.info(
            result.get(
                "resume_summary",
                "No summary available."
            )
        )

    with col2:

        st.markdown(
            "<div class='section-header'>📋 Job Summary</div>",
            unsafe_allow_html=True,
        )

        st.info(
            result.get(
                "job_summary",
                "No summary available."
            )
        )

    st.divider()


        # -----------------------------
    # Skills Section
    # -----------------------------
    st.markdown(
        "<div class='section-header'>🛠 Skills Analysis</div>",
        unsafe_allow_html=True,
    )

    skill_col1, skill_col2 = st.columns(2)

    with skill_col1:

        display_list(
            "✅ Matching Skills",
            result.get(
                "matching_skills",
                [],
            ),
        )

    with skill_col2:

        display_list(
            "❌ Missing Skills",
            result.get(
                "missing_skills",
                [],
            ),
        )

    st.divider()

    # -----------------------------
    # Strengths & Weaknesses
    # -----------------------------
    sw_col1, sw_col2 = st.columns(2)

    with sw_col1:

        display_list(
            "💪 Strengths",
            result.get(
                "strengths",
                [],
            ),
        )

    with sw_col2:

        display_list(
            "⚠ Weaknesses",
            result.get(
                "weaknesses",
                [],
            ),
        )

    st.divider()

    # -----------------------------
    # Resume Improvements
    # -----------------------------
    st.markdown(
        "<div class='section-header'>🚀 Resume Improvements</div>",
        unsafe_allow_html=True,
    )

    improvements = result.get(
        "resume_improvements",
        [],
    )

    if improvements:

        for index, improvement in enumerate(
            improvements,
            start=1,
        ):

            st.write(
                f"**{index}.** {improvement}"
            )

    else:

        st.success(
            "No major improvements suggested."
        )

    st.divider()

    # -----------------------------
    # Final Recommendation
    # -----------------------------
    st.markdown(
        "<div class='section-header'>⭐ Final Recommendation</div>",
        unsafe_allow_html=True,
    )

    recommendation = result.get(
        "final_recommendation",
        "No recommendation available.",
    )

    st.success(recommendation)

    st.divider()

        # -----------------------------
    # Analysis Summary
    # -----------------------------
    st.markdown(
        "<div class='section-header'>📊 Analysis Summary</div>",
        unsafe_allow_html=True,
    )

    matching_count = len(result.get("matching_skills", []))
    missing_count = len(result.get("missing_skills", []))
    strength_count = len(result.get("strengths", []))
    weakness_count = len(result.get("weaknesses", []))

    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:
        st.info(
            f"""
### Resume Statistics

- 🎯 Match Score: **{score}%**
- ✅ Matching Skills: **{matching_count}**
- ❌ Missing Skills: **{missing_count}**
- 💪 Strengths: **{strength_count}**
- ⚠ Weaknesses: **{weakness_count}**
"""
        )

    with summary_col2:

        if score >= 85:
            st.success(
                "Excellent match! Your resume aligns very well with this job."
            )

        elif score >= 70:
            st.warning(
                "Good match. A few improvements can increase your chances."
            )

        elif score >= 50:
            st.warning(
                "Average match. Consider updating your resume before applying."
            )
