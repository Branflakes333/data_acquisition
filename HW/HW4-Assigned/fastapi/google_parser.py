import requests

from bs4 import BeautifulSoup


def retreive_google_career_qualification(url: str) -> dict:
    """
    For the given Google Jobs URL, retrieve all the "qualification" sections.
    This should return a dictionary format of the qualification string (Ex. Minimum qualification) as a key,
    and a list of paragraphs given under the qualifiaction string.
    {'Minimum qualifications:': ['Currently enrolled in or graduated from a degree program within Product Management, Computer Science, Engineering, Data Science, Mathematics, Statistics, or a related technical field, or equivalent practical experience.', 'Internship or Teaching Assistant experience in product management, software development or a similar technical field.', 'Experience leading entrepreneurial efforts or outreach within organizations while building cross-functional relationships.', 'Experience preparing and delivering technical presentations to an audience through internships, coursework, or extracurriculars.'],
     'Preferred qualifications:': ['Experience with methodologies aimed to drive product development and delivery.', 'Experience applying AI/ML concepts to build products or features through relevant internship, capstone projects, or other academic work.', 'Technical experience with programming languages, data analysis, business case/modeling, pricing, or design.', 'Ability to start full-time in the primary cohort onboarding cycle between April and August 2026.', 'Ability to communicate in English fluently to support cross-functional business relationships in the region.', 'Excellent problem-solving, organizational, investigative, and critical thinking skills.']}
    """
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    headers = [h3 for h3 in soup.find_all(
        "h3") if "qualifications" in h3.get_text().lower()]

    results = {header.get_text(strip=True): header.find_next("ul").find_all("li")
               for header in headers}

    for heading, items in results.items():
        print(f"\n{heading}")
        for li in items:
            print("-", li.get_text(strip=True))


retreive_google_career_qualification(
    "https://www.google.com/about/careers/applications/jobs/results/89208145057850054-data-scientist-product-intern-ms-summer-2026?q=%22Data%20Scientist%22#!t=jo&jid=127025001&")
