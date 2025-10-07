import streamlit as st
import chromadb
import pandas as pd
from PIL import Image

st.set_page_config(layout='wide',
                    page_title="Space Biology Publications: Browse by Topic",
                    page_icon="🪐")

st.markdown("# 🔭 Browse by Topic")

st.divider()

CHROMADB_PATH = "data/chroma"
DATA_FILE = "data/SB_publication_PMC_data.csv"

data = pd.read_csv(DATA_FILE, sep="|")

client = chromadb.PersistentClient(path=CHROMADB_PATH)

def retrieve_similar_documents(query, n_results=10):
    collection = client.get_collection(name="publications")
    results = collection.query(query_texts=[query], n_results=100)
    pmcs = []
    seen = set()
    for meta in results["metadatas"][0]:
        pmc = meta["pmc"]
        if pmc not in seen:
            pmcs.append(pmc)
            seen.add(pmc)
        if len(pmcs) == n_results:
            break
    return pmcs

st.caption("Find publications related to your topic of interest. This tool lets you search for Space Biology publications by topic using a semantic search engine — meaning it looks for publications with similar meanings, not just exact words.")

st.markdown("###")

st.subheader("Enter a topic to search")

text_search = st.text_input("Search topic", value="", placeholder="Example: effects of microgravity on human cells", label_visibility="collapsed")

similar_pmcs = retrieve_similar_documents(text_search, n_results=10)
similar_pmcs = [int(pmc) for pmc in similar_pmcs]
data_filtered = data[data["pmc"].isin(similar_pmcs)].reset_index(drop=True)

data_filtered = data_filtered.rename(columns={
    "pmc": "PMID",
    "article_type": "Article Type",
    "journal": "Journal",
    "publication_year": "Year",
    "title": "Title",
    })

if text_search:
    # --- Display filtered DataFrame ---
    st.dataframe(data=data_filtered,
                hide_index=True,
                width="stretch",
                column_order=['Title', 'Journal', 'Article Type', 'Year', 'PMID', 'link'],
                column_config={"link": st.column_config.LinkColumn(display_text="Open in PubMed")},)
    
st.divider()




