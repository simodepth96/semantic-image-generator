import pandas as pd
import streamlit as st
from io import BytesIO
import base64

def generate_rel_canonical_link(image_url, preload_images, lazy_load_images):
    img_loading = 'eager" fetchpriority="high' if preload_images else 'lazy' if lazy_load_images else 'auto'
    return (
        '<picture>\n'
        '  <source media="(min-width:1400px)" srcset="/1080.jpg 1x, /1440.jpg 1.5x, /2160.jpg 2x">\n'
        '  <source media="(min-width:700px)" srcset="/720.jpg 1x, /1080.jpg 1.5x, /1440.jpg 2x">\n'
        '  <source media="(min-width:500px)" srcset="/540.jpg 1x, /720.jpg 1.5x, /1080.jpg 2x">\n'
        '  <source media="(max-width:500px)" srcset="/360.jpg 1x, /540.jpg 1.5x, /720.jpg 2x">\n'
        f'  <img loading="{img_loading}" src="{image_url}" width="800" height="600" alt="Image #1">\n'
        '</picture>'
    )

st.title("Semantic Pictures Generator")
st.write(
    "A tool grounded in basic Python to convert image URLs into state-of-the-art semantic HTML attributes to enhance search engine understanding of your visual content.")
st.write(
    "Once the input file has been uploaded you can choose between eagerly loading images or lazy loading them according to your needs")

st.sidebar.subheader(
    "🎯 How to Use"
)
st.sidebar.markdown(
    """
    - Upload an XLSX/CSV file exported from Screaming Frog.
    - Navigate to Images > Missing Images > Export in Screaming Frog.
    - Open the file and eliminate all headers except for "Address"
    - Rename the "Address" column as "URL".
    - Upload the modified file to the app.
    """
)

# File uploader
uploaded_file = st.file_uploader("Upload a CSV or XLSX file", type=["csv", "xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)

    # Display the dataframe
    st.dataframe(df.head())

    # User options
    preload_images = st.checkbox("Preload Images", value=True)
    lazy_load_images = st.checkbox("Lazy Load Images", value=False)

    if preload_images and lazy_load_images:
        st.warning("Please choose only one option: Preload Images OR Lazy Load Images.")
    elif st.button("Generate Semantic Images"):
        # Generate "rel=canonical" links
        df["Semantic Images"] = df["URL"].apply(
            lambda image_url: generate_rel_canonical_link(image_url, preload_images, lazy_load_images)
        )

        # Save output to Excel
        output_filename = "semantic_pictures.xlsx"
        output_excel = BytesIO()
        df.to_excel(output_excel, index=False, engine='openpyxl')
        output_excel.seek(0)

        # Create a link for downloading the Excel file
        b64 = base64.b64encode(output_excel.read()).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{output_filename}">Download {output_filename}</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    pass
