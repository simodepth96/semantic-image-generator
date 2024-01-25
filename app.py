import pandas as pd
import streamlit as st

def generate_rel_canonical_link(image_url, preload_images, lazy_load_images):
    img_loading = 'eager' if preload_images else 'lazy'
    return (
        '<picture>\n'
        '  <source media="(min-width:1400px)" srcset="/1080.jpg 1x, /1440.jpg 1.5x, /2160.jpg 2x">\n'
        '  <source media="(min-width:700px)" srcset="/720.jpg 1x, /1080.jpg 1.5x, /1440.jpg 2x">\n'
        '  <source media="(min-width:500px)" srcset="/540.jpg 1x, /720.jpg 1.5x, /1080.jpg 2x">\n'
        '  <source media="(max-width:500px)" srcset="/360.jpg 1x, /540.jpg 1.5x, /720.jpg 2x">\n'
        f'  <img loading="{img_loading}" src="{image_url}" width="800" height="600" alt="Image #1">\n'
        '</picture>'
    )

def main():
    st.title("Semantic Pictures Generator")

    # File uploader
    uploaded_file = st.file_uploader("Upload a CSV or XLSX file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)

        # Display the dataframe
        st.dataframe(df.head())

        # User options
        preload_images = st.checkbox("Preload Images", value=True)
        lazy_load_images = st.checkbox("Lazy Load Images", value=False)

        # Generate "rel=canonical" links
        df["Semantic Images"] = df["URL"].apply(
            lambda image_url: generate_rel_canonical_link(image_url, preload_images, lazy_load_images)
        )

        # Save output to Excel
        output_filename = "semantic_pictures.xlsx"
        output_excel = df.to_excel(index=False, engine='openpyxl')
        
        st.markdown(f"### Download Generated File: [{output_filename}](data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{output_excel})")

if __name__ == "__main__":
    main()
