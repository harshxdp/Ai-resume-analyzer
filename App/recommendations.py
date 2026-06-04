import streamlit as st

def get_skill_recommendations(skills):
    """Analyzes skills and returns the field, recommended skills, and courses."""
    skills_lower = [skill.lower() for skill in skills] if skills else []
    
    courses = []

    if any(s in skills_lower for s in ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep learning', 'data analysis']):
        field = "Data Science & AI"
        rec_skills = ['MLOps', 'Computer Vision', 'NLP', 'Apache Spark', 'Tableau', 'AWS SageMaker']
    elif any(s in skills_lower for s in ['react', 'django', 'node.js', 'html', 'css', 'javascript', 'flask']):
        field = "Web Development"
        rec_skills = ['TypeScript', 'Next.js', 'GraphQL', 'Docker', 'WebSockets', 'Tailwind CSS']
    elif any(s in skills_lower for s in ['java', 'c++', 'python', 'c#', 'spring boot', 'software development', 'algorithms']):
        field = "Software Engineering"
        rec_skills = ['System Design', 'Kubernetes', 'Microservices', 'CI/CD', 'Cloud Architecture', 'Go (Golang)']
    elif any(s in skills_lower for s in ['android', 'kotlin', 'ios', 'swift', 'flutter', 'react native']):
        field = "Mobile Development"
        rec_skills = ['Firebase', 'Jetpack Compose', 'SwiftUI', 'Mobile UI/UX', 'App Store Optimization (ASO)']
    elif any(s in skills_lower for s in ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'linux']):
        field = "Cloud & DevOps"
        rec_skills = ['Terraform', 'Ansible', 'Prometheus', 'Grafana', 'Serverless Architecture']
    elif any(s in skills_lower for s in ['security', 'penetration testing', 'firewalls', 'malware', 'cryptography', 'network security']):
        field = "Cybersecurity"
        rec_skills = ['Ethical Hacking', 'CISSP Certification', 'SIEM', 'Cloud Security', 'Incident Response']
    elif any(s in skills_lower for s in ['figma', 'adobe xd', 'sketch', 'wireframing', 'user interface', 'user experience']):
        field = "UI / UX Design"
        rec_skills = ['Prototyping', 'Usability Testing', 'Interaction Design', 'CSS/SASS', 'Design Systems']
    elif any(s in skills_lower for s in ['seo', 'google analytics', 'social media', 'content marketing', 'sem', 'digital marketing']):
        field = "Digital Marketing"
        rec_skills = ['Conversion Rate Optimization (CRO)', 'A/B Testing', 'Email Automation', 'HubSpot', 'Copywriting']
    elif any(s in skills_lower for s in ['accounting', 'excel', 'financial analysis', 'reconciliation', 'auditing', 'tax']):
        field = "Finance & Accounting"
        rec_skills = ['Financial Modeling', 'Python (for Finance)', 'Power BI', 'SAP FI/CO', 'Risk Management']
    elif any(s in skills_lower for s in ['logistics', 'supply chain', 'warehouse', 'inventory', 'procurement']):
        field = "Operations & Supply Chain"
        rec_skills = ['SAP', 'Advanced Data Analysis', 'Six Sigma', 'Vendor Management', 'Demand Forecasting']
    else:
        field = "General / Unspecified"
        rec_skills = []

    return field, rec_skills, courses, skills_lower

def perform_resume_audit(text, data):
    """Displays the detailed resume audit UI and calculates the health score."""
    st.markdown("---")
    st.subheader("💡 Detailed Resume Audit")
    resume_score = 0
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 📋 Content Checklist")
        
        if 'objective' in text.lower() or 'summary' in text.lower() or 'profile' in text.lower():
            st.markdown("✅ **Objective / Summary:** Included")
            resume_score += 10
        else:
            st.markdown("⚠️ **Objective / Summary:** Missing. *Add a brief overview of your career goals.*")

        if 'education' in text.lower() or data.get('degree') or data.get('college_name'):
            st.markdown("✅ **Education Details:** Included")
            resume_score += 10
        else:
            st.markdown("⚠️ **Education Details:** Missing. *Crucial for recruiters to see your academic background.*")

        if 'experience' in text.lower() or data.get('total_experience', 0) > 0:
            st.markdown("✅ **Work Experience:** Included")
            resume_score += 10
        else:
            st.markdown("⚠️ **Work Experience:** Missing. *Add professional, academic, or freelance experience.*")

        if 'internship' in text.lower() or 'intern' in text.lower():
            st.markdown("✅ **Internships:** Included")
            resume_score += 10
        else:
            st.markdown("⚠️ **Internships:** Missing. *Highly recommended for freshers to show practical skills.*")

        if data.get('skills'):
            st.markdown("✅ **Technical Skills:** Included")
            resume_score += 10
        else:
            st.markdown("⚠️ **Technical Skills:** Missing. *This is the most critical section for ATS software.*")

        if 'hobbies' in text.lower() or 'hobby' in text.lower():
            st.markdown("✅ **Hobbies:** Included")
            resume_score += 10
        else:
            st.markdown("⚠️ **Hobbies:** Missing. *Helps show your personality and cultural fit.*")

        if 'interest' in text.lower() or 'interests' in text.lower():
            st.markdown("✅ **Interests:** Included")
            resume_score += 10
        else:
            st.markdown("⚠️ **Interests:** Missing. *Shows passion outside of standard work hours.*")

        if 'achievement' in text.lower() or 'achievements' in text.lower() or 'awards' in text.lower():
            st.markdown("✅ **Achievements / Awards:** Included")
            resume_score += 10
        else:
            st.markdown("⚠️ **Achievements:** Missing. *Demonstrates your capability to excel.*")

        if 'certification' in text.lower() or 'certifications' in text.lower() or 'certificate' in text.lower():
            st.markdown("✅ **Certifications:** Included")
            resume_score += 10
        else:
            st.markdown("⚠️ **Certifications:** Missing. *Shows dedication to continuous learning.*")

        if 'project' in text.lower() or 'projects' in text.lower():
            st.markdown("✅ **Projects:** Included")
            resume_score += 10
        else:
            st.markdown("⚠️ **Projects:** Missing. *Proves you can apply theoretical knowledge to real problems.*")

    with col2:
        st.markdown("#### 🎯 Final Score")
        st.metric(label="Resume Health", value=f"{resume_score} / 100")
        st.progress(resume_score)
        
        if resume_score >= 80:
            st.success("🔥 **Outstanding Resume!** You are highly competitive.")
            st.balloons()
        elif resume_score >= 60:
            st.warning("📈 **Good, but has room to grow.** Review the warnings on the left.")
        else:
            st.error("🛠️ **Needs major improvements.** Please add the missing sections.")
            
    return resume_score

def show_skill_upgrades(skills_lower):
    """Displays 1-to-1 skill upgrades based on existing skills."""
    skill_upgrades = {
        'javascript': 'TypeScript',
        'html': 'React.js or Vue.js',
        'css': 'Tailwind CSS',
        'react': 'Next.js',
        'python': 'Django or FastAPI',
        'java': 'Spring Boot & Microservices',
        'sql': 'NoSQL (MongoDB) or PostgreSQL',
        'machine learning': 'MLOps & AWS SageMaker',
        'data analysis': 'Power BI & Tableau',
        'android': 'Jetpack Compose',
        'manual testing': 'Selenium (Automation)'
    }

    personalized_upgrades = []
    for skill in skills_lower:
        if skill in skill_upgrades:
            personalized_upgrades.append(f"🔹 Since you know **{skill.title()}**, you should learn **{skill_upgrades[skill]}** next.")

    st.markdown("### 🚀 Personalized Skill Upgrades")
    if personalized_upgrades:
        st.success("We analyzed your specific toolkit. Here is how you can level up:")
        for upgrade in personalized_upgrades:
            st.markdown(upgrade)
    else:
        st.info("Keep adding more core technical skills to your resume to get personalized upgrade suggestions!")

def calculate_and_display_score(text, num_skills):
    """Calculates an alternative ATS-style score and displays it."""
    score = 0
    keywords = ["Objective", "Education", "Experience", "Projects"]
    for k in keywords:
        if k.lower() in text.lower():
            score += 20 
            
    if num_skills > 0:
        if num_skills <= 5:
            score += 10
        elif 6 <= num_skills <= 10:
            score += 15
        else: 
            score += 20

    score = min(score, 100)
    st.markdown("### 🎯 Resume Score")
    st.progress(score)
    st.success(f"**Final Score: {score} / 100**")
    
    return score

def show_enhancement_tips(num_skills, rec_skills, field):
    """Displays tips to enhance the resume based on missing skills."""
    st.markdown("### 💡 How to Enhance Your Resume")
    if num_skills == 0:
        st.error("⚠️ **No skills detected!** Please add a dedicated 'Skills' section with relevant keywords.")
    else:
        st.info(f"✅ We detected **{num_skills} skills** in your resume.")
        if rec_skills:
            st.success(f"**To grow your resume and stand out in {field}, consider learning and adding these skills:**")
            for skill in rec_skills:
                st.markdown(f"🔹 {skill}")
        else:
            st.warning("Add more niche, technical keywords relevant to your target job to get specific skill recommendations!")