# styles.py

def load_css(file_path):
    """Load external CSS for the Streamlit app."""
    with open(file_path) as f:
        return f"<style>{f.read()}</style>"

