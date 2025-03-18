import streamlit as st
import json
from pathlib import Path

def load_settings():
    settings_path = Path("data/settings.json")
    if settings_path.exists():
        with open(settings_path, "r") as f:
            return json.load(f)
    return {
        "citation_style": "APA",
        "date_format": "%Y-%m-%d",
        "default_analysis_plots": ["histogram", "box"],
        "auto_save": True,
        "notifications": True
    }

def save_settings(settings):
    settings_path = Path("data/settings.json")
    settings_path.parent.mkdir(exist_ok=True)
    with open(settings_path, "w") as f:
        json.dump(settings, f)

def main():
    st.title("⚙️ Settings")
    
    settings = load_settings()
    
    # Citation Settings
    st.header("Citation Settings")
    settings['citation_style'] = st.selectbox(
        "Default Citation Style",
        options=["APA", "MLA", "Chicago"],
        index=["APA", "MLA", "Chicago"].index(settings.get('citation_style', "APA"))
    )
    
    # Date Format Settings
    st.header("Date Format")
    settings['date_format'] = st.selectbox(
        "Default Date Format",
        options=["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"],
        index=["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"].index(settings.get('date_format', "%Y-%m-%d"))
    )
    
    # Analysis Settings
    st.header("Analysis Settings")
    settings['default_analysis_plots'] = st.multiselect(
        "Default Analysis Plots",
        options=["histogram", "box", "violin", "scatter"],
        default=settings.get('default_analysis_plots', ["histogram", "box"])
    )
    
    # Application Settings
    st.header("Application Settings")
    settings['auto_save'] = st.toggle(
        "Auto-save projects",
        value=settings.get('auto_save', True)
    )
    settings['notifications'] = st.toggle(
        "Enable notifications",
        value=settings.get('notifications', True)
    )
    
    # Save Settings
    if st.button("Save Settings"):
        save_settings(settings)
        st.success("Settings saved successfully!")
    
    # Reset Settings
    if st.button("Reset to Defaults"):
        settings = {
            "citation_style": "APA",
            "date_format": "%Y-%m-%d",
            "default_analysis_plots": ["histogram", "box"],
            "auto_save": True,
            "notifications": True
        }
        save_settings(settings)
        st.success("Settings reset to defaults!")
        st.rerun()

if __name__ == "__main__":
    main()
