/* Importing the Orbitron font from Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500&display=swap');

/* General styling */
body {
    background-color: black;
    color: #00FF00; /* Bright green for text */
    margin: 0;
    padding: 0;
}

/* Orbitron font for headings */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Orbitron', sans-serif;
    color: #00FF00; /* Green for headings */
}

/* Control Dashboard Animation */
@keyframes fadeIn {
    0% { opacity: 0; transform: translateY(-20px); }
    100% { opacity: 1; transform: translateY(0); }
}

.title {
    font-family: 'Orbitron', sans-serif;
    font-size: 50px;
    color: #00FF00;
    animation: fadeIn 2s ease-out;
    text-align: center;
    margin-bottom: 20px;
}

.subtitle {
    font-size: 20px;
    color: #FFFFFF;
    animation: fadeIn 2s ease-out;
    text-align: center;
}

/* Selected Markdown Styling */
.stMarkdown > div {
    color: #00FF00 !important; /* Ensure selected markdown stays green */
}

/* Streamlit background */
.stApp {
    background-color: black;
}

/* Sidebar Styling */
.stSidebar {
    background-color: black;
}

