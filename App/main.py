# imported all libraries
import streamlit as st
import pandas as pd
import base64, random, time, datetime, io, secrets

#seperated file imported of database
import database as db

import nltk
nltk.download('stopwords', quiet=True)
nltk.download('punkt')

from pyresparser import ResumeParser
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
from PIL import Image

# Import the separated logic of recommendations 
import recommendations as rc

#utility functions
def get_csv_download_link(df, filename, text):
    b64 = base64.b64encode(df.to_csv(index=False).encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'

def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file = io.StringIO()
    converter = TextConverter(resource_manager, fake_file, laparams=LAParams())
    interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh):
            interpreter.process_page(page)

    text = fake_file.getvalue()
    converter.close()
    fake_file.close()
    return text

def show_pdf(path):
    with open(path, "rb") as f:
        pdf = base64.b64encode(f.read()).decode()
    st.markdown(f'<iframe src="data:application/pdf;base64,{pdf}" width="700" height="1000"></iframe>', unsafe_allow_html=True)

#streamlit comnfig
st.set_page_config(page_title="Resume Analyzer with AI", page_icon='./Logo/recommend.png')

#main app logic
def run():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Place the image in the middle column
        st.image(Image.open('./Logo/RESUM.png'), width=350)
    menu = st.sidebar.selectbox("Menu", ["User", "Feedback", "About", "Admin"])

    #Initialize DB Tables from database.py
    db.create_tables()
    
    #user section
    if menu == "User":
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")

        file = st.file_uploader("Upload Resume", type=["pdf"])

        if file:
            path = "./Uploaded_Resumes/" + file.name
            with open(path, "wb") as f:
                f.write(file.getbuffer())

            show_pdf(path)

            data = ResumeParser(path).get_extracted_data()
            text = pdf_reader(path)

            st.header("Resume Analysis")

            # Candidate Level Check
            total_exp = data.get('total_experience', 0)
            if total_exp == 0:
                level = "Fresher"
            elif 1 <= total_exp <= 3:
                level = "Intermediate"
            else:
                level = "Experienced"
            st.success(f"Level: {level} ({total_exp} Years Experience)")

            # Education Check
            st.subheader("Resume Improvement Suggestions")
            degrees = data.get('degree')
            colleges = data.get('college_name')

            if not degrees:
                st.warning("⚠️ *Missing Degree:* We couldn't detect a degree. Please ensure you clearly mention your degree (e.g., B.Tech, BCA, BSc) in your Education section.")
            else:
                degree_text = ', '.join(degrees) if isinstance(degrees, list) else degrees
                st.success(f"🎓 *Degree detected:* {degree_text}")

            if not colleges:
                st.warning("⚠️ *Missing College:* We couldn't detect your college name. We highly recommend adding your University or College name to strengthen your profile.")
            else:
                college_text = ', '.join(colleges) if isinstance(colleges, list) else colleges
                st.success(f"🏫 *College detected:* {college_text}")
                
            # START OF RECOMMENDATION LOGIC
            
            # 1. Get Skill Analysis
            skills = data.get('skills', [])
            field, rec_skills, courses, skills_lower = rc.get_skill_recommendations(skills)
            
            # 2. Perform Resume Audit UI and Logic
            rc.perform_resume_audit(text, data)
            
            # 3. Show Personalized Upgrades
            rc.show_skill_upgrades(skills_lower)
            
            # 4. Calculate Final Score
            num_skills = len(skills)
            score = rc.calculate_and_display_score(text, num_skills)
            
            # 5. Show Enhancement Tips
            rc.show_enhancement_tips(num_skills, rec_skills, field)

            # Save data securely via database.py
            ts = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            db.insert_data((
                secrets.token_urlsafe(12),
                name, email, phone,                    
                data.get('name', 'NA'),                
                data.get('email', 'NA'),               
                str(score), ts, 
                str(data.get('no_of_pages', 1)),       
                field, level, str(skills),             
                str(rec_skills), str(courses),
                file.name                              
            ))

    #feedback section
    elif menu == "Feedback":
        with st.form("form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            rating = st.slider("Rating",1,5)
            comment = st.text_input("Comment")

            if st.form_submit_button("Submit"):
                db.insert_feedback((name, email, rating, comment, str(datetime.datetime.now())))
                st.success("Saved")

    #admin section
    elif menu == "Admin":
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):
            if user == "Harshdeep" and pwd == "raharsh":
                st.success("Login Successful!")
                df = db.fetch_all_data()
                st.dataframe(df)
                st.markdown(get_csv_download_link(df, "data.csv", "Download"), unsafe_allow_html=True)
            else:
                st.error("Incorrect Username or Password. Please try again.")

    #about section
    else:
        st.write("AI Resume Analyzer using NLP to extract, analyze and recommend.")

#run app
if __name__ == "__main__":
    run()