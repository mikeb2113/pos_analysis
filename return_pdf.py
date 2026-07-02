import streamlit as st
import fitz

with st.sidebar:
    original_doc = st.file_uploader(
        "pdfs/ClassOverlapping",
        accept_multiple_files=False,
        type="pdf"
    )

    text_lookup = st.text_input("classification", max_chars=50)

if original_doc:
    with fitz.open(stream=original_doc.getvalue(), filetype="pdf") as doc:

        for i in range(doc.page_count):
            page = doc.load_page(i)

            if text_lookup:
                areas = page.search_for(text_lookup)

                st.write(f"Page {i + 1}: found {len(areas)} matches")

                for area in areas:
                    page.draw_rect(
                        area,
                        color=(1, 0, 0),
                        width=2
                    )

            pix = page.get_pixmap(dpi=120)

            st.subheader(f"Page {i + 1}")
            st.image(
                pix.tobytes("png"),
                use_container_width=True
            )