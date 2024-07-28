import streamlit as st
import requests

# Set up the Streamlit interface
st.title("Job Description to Candidate Matching")
st.write("Enter a job description to find matching candidates.")

# Input box for job description
job_description = st.text_area("Job Description", "")

if st.button("Find Candidates"):
    # Call the Flask API to get matched candidates
    response = requests.get("http://localhost:5000/find_candidates",  params={'job_description': job_description})
    # print(response, 'kkkkkkkk')
    candidates = response.json()
    
    # Display the matched candidates
    if candidates:
        for candidate in candidates:
            st.subheader(candidate['Name'])
            st.write(f"**Skills:** {candidate['Job Skills']}")
            st.write(f"**Experience:** {candidate['Experience']} years")
            st.write(f"**Projects:** {candidate['Projects']}")
            st.write(f"**Comments:** {candidate['Comments']}\n")
    else:
        st.write("No matching candidates found.")
