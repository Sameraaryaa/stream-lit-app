import streamlit as st
import json
from pathlib import Path
from datetime import datetime

# Initialize profile storage
PROFILE_PATH = Path("data/profile.json")

def load_profile():
    if PROFILE_PATH.exists():
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)
    return {
        "name": "",
        "email": "",
        "institution": "",
        "research_interests": [],
        "expertise": [],
        "education": [],
        "publications": []
    }

def save_profile(profile_data):
    PROFILE_PATH.parent.mkdir(exist_ok=True)
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile_data, f)

def main():
    st.title("👤 Research Profile")

    profile = load_profile()

    # Basic Information
    st.header("Basic Information")
    profile["name"] = st.text_input("Full Name", profile.get("name", ""))
    profile["email"] = st.text_input("Email", profile.get("email", ""))
    profile["institution"] = st.text_input("Institution", profile.get("institution", ""))

    # Research Interests
    st.header("Research Interests")
    interests = st.text_area(
        "Enter research interests (one per line)",
        "\n".join(profile.get("research_interests", [])),
    )
    profile["research_interests"] = [x.strip() for x in interests.split("\n") if x.strip()]

    # Expertise
    st.header("Areas of Expertise")
    expertise = st.text_area(
        "Enter areas of expertise (one per line)",
        "\n".join(profile.get("expertise", [])),
    )
    profile["expertise"] = [x.strip() for x in expertise.split("\n") if x.strip()]

    # Education
    st.header("Education")
    if "education" not in profile:
        profile["education"] = []
    
    for i, edu in enumerate(profile["education"]):
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            profile["education"][i]["institution"] = st.text_input(
                "Institution", edu.get("institution", ""), key=f"edu_inst_{i}"
            )
        with col2:
            profile["education"][i]["degree"] = st.text_input(
                "Degree", edu.get("degree", ""), key=f"edu_deg_{i}"
            )
        with col3:
            profile["education"][i]["year"] = st.text_input(
                "Year", edu.get("year", ""), key=f"edu_year_{i}"
            )

    if st.button("Add Education"):
        profile["education"].append({"institution": "", "degree": "", "year": ""})

    # Publications
    st.header("Publications")
    if "publications" not in profile:
        profile["publications"] = []
    
    for i, pub in enumerate(profile["publications"]):
        col1, col2 = st.columns([4, 1])
        with col1:
            profile["publications"][i]["citation"] = st.text_area(
                "Citation", pub.get("citation", ""), key=f"pub_{i}"
            )
        with col2:
            profile["publications"][i]["year"] = st.text_input(
                "Year", pub.get("year", ""), key=f"pub_year_{i}"
            )

    if st.button("Add Publication"):
        profile["publications"].append({"citation": "", "year": ""})

    # Save Profile
    if st.button("Save Profile"):
        save_profile(profile)
        st.success("Profile saved successfully!")

if __name__ == "__main__":
    main()
