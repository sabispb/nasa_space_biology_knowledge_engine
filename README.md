# NASA Space Apps Challenge 🪐✨

This project is the contribution of the team **Overcooked** to the [**Build a Space Biology Knowledge Engine**](https://www.spaceappschallenge.org/2025/challenges/build-a-space-biology-knowledge-engine/) challenge of the [**2025 NASA Space Apps Challenge**](https://www.spaceappschallenge.org/).

This project supports NASA's vision for safe and efficient human exploration of the Moon and Mars by developing a dynamic AI-powered dashboard that organizes, summarizes, and visualizes decades of space biology research. NASA's Biological and Physical Sciences Division has produced over 600 bioscience publications detailing experiments on how living systems respond to the space environment. However, the sheer volume and diversity of this information make it challenging to navigate.

This tool leverages data analytics and artificial intelligence to extract key insights, reveal research trends and gaps, and enable scientists, program managers, and mission planners to explore the impacts and outcomes of past space experiments through an interactive and accessible web interface.

The dashboard is available here: **https://93.189.89.7/nasa_challenge/**

## 🌒 Project setup

1. Install the Python package manager [uv](vhttps://pypi.org/project/uv/).

2. Clone repository:
    ```
    git@github.com:sabispb/nasa_space_biology_knowledge_engine.git
    ````

3. Enter the repository folder and create environment:
    ```
    cd nasa_space_biology_knowledge_engine/
    uv sync
    ```

4. Activate the environment:
    ```
    source .venv/bin/activate
    ```


## 🚀 Data recollection and enhancement

All the datasets of the project should be stored in the `data` folder of the repository. The following sections explain how to get or create them.

### Original dataset

A list of full-text open-access Space Biology, available here:
- [**SB_publication_PMC.csv**](https://github.com/jgalazka/SB_publications/tree/main)

### Corrections dataset

A manual review of the original dataset revealed that some of the links were incorrect. Therefore, a correction file with the necessary fixes was created and is available here:

- [**SB_publication_PMC_corrections.csv**](https://drive.google.com/file/d/1ICgjp5-dnOKF2vNTJVsLgMsdzDHlijko/view?usp=sharing)

### Clean dataset

The project page claimed that 608 full-text open-access Space Biology publications were available. However, it was found that some of these publications were duplicated or not open-access. Some of the provided links were also incorrect.

After fixing some of the invalid links and discarding those for which the correct link was not found, a dataset of 546 publications was obtained.

To generate the **SB_publication_PMC_clean.csv** file use the [**src/data_retrieval/clean_sb_publications_pmc.ipynb**](src/data_retrieval/clean_sb_publications_pmc.ipynb) notebook.\
⚙️ To execute this notebook, ensure that both the **original** and **corrections datasets** are placed inside the `data` folder.\
Additional datasets will be generated automatically as part of the process.

### XML data from articles

Run the notebook [**src/data_retrieval/retrieve_xmls.ipynb**](src/data_retrieval/retrieve_xmls.ipynb) to obtain the **SB_publication_PMC_with_xmls.parquet** file, which contains an XML object for each publication.

In the function `retrieve_xml` of the notebook, a valid e-mail address must be introduced.

### Dataset with metadata fields

Run the notebook [**src/data_retrieval/extract_fields_from_xml.ipynb**](src/data_retrieval/extract_fields_from_xml.ipynb) to obtain the file **SB_publication_PMC_data.csv**. This file contains, for each publications:
- Article type
- Language
- Journal
- Publisher
- Publication year

### Dataset with disciplines

Run the notebook [**src/data_retrieval/extract_disciplines_from_xml.ipynb**](src/data_retrieval/extract_disciplines_from_xml.ipynb) to obtain the file **SB_publication_PMC_disciplines.csv** containing the disciplines each publication belongs to.

### Data set with texts

Run the notebook [**src/data_retrieval/extract_plain_text_from_xml.ipynb**](src/data_retrieval/extract_plain_text_from_xml.ipynb) to obtain the file **SB_publication_PMC_texts.parquet** containing the abstract and the full text of the publications when available.

## ✨ AI features

### Generate simplified abstract of abstract

The model [**haining/scientific_abstract_simplification**](https://huggingface.co/haining/scientific_abstract_simplification) was used to summarize, simplify, and contextualize the abstracts of all publications, providing accessible summaries of each publication. This model is based on a fine-tuned T5 architecture trained for scientific text simplification.

To generate the simplified abstracts, run the [**src/ai/abstract_model.ipynb**](src/ai/abstract_model.ipynb) notebook. The resulting file **SB_publication_PMC_texts_simplified.parquet** will be created.

### Generate main ideas of articles

The LLM [**Magistral Small 1.2**](https://docs.mistral.ai/getting-started/models/models_overview/) (magistral-small-2509) was used to summarize the main ideas of all publications for which the full text of the article was available.

To obtain these summaries, run the [**src/ai/generate_main_ideas.ipynb**](src/ai/generate_main_ideas.ipynb) notebook. Note that a valid [**Mistral AI**](https://mistral.ai/) `api_key` is required for the code to run. The file **SB_publication_PMC_texts_main_ideas.parquet** will be generated.

### Generate embeddings and find similar articles

A vector database was created to find the top 5 similar publications for each publication in the dataset. The title, abstract and chunked text of all publications (when available) were embedded using the  **all-MiniLM-L6-v2 Sentence Transformers**(https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) model.

To obtain these top-5 recommended articles, run the [**src/ai/generate_embeddings.ipynb**](src/ai/generate_embeddings.ipynb) notebook.The file **SB_publication_PMC_recommendations.csv** will be generated. 

### Publication searcher

The notebook [**src/ai/publication_searcher.ipynb**](src/ai/publication_searcher.ipynb) contains an example of how to use the generated embeddings to look for publications associated to any given query.

## 🛰️ Interactive Dashboard

The interactive dashboard was built using [**Streamlit**](https://streamlit.io/).  
It is organized as a **multi-page app**, combining **pages** and **tabs** to let users explore publications from multiple perspectives — such as data overviews, highlights, topic browsing, and AI-generated summaries.  

The Streamlit configuration (theme, server, browser) is stored in the `.streamlit/` folder.  
All the scripts are located in the **dashboard** folder of the project.  

To launch the application, run the following command from the project root:  

    ```
    streamlit run dashboard/Home.py
    ```

## 👩‍🚀 Contributors

| Name           | Email                 | GitHub |
|----------------|-----------------------|--------|
| Sabina Planas Bonell | sabinaplanas@gmail.com | @sabispb
| Didac Fortuny Almiñana | dacfortuny@gmail.com | @dacfortuny

## 🔭 Licenses

This project uses the following models:

- [**haining/scientific_abstract_simplification**](https://huggingface.co/haining/scientific_abstract_simplification)  
  © 2023 Haining — released under the MIT License  

- [**Magistral Small 1.2**](https://docs.mistral.ai/getting-started/models/models_overview/)  
  © 2024 Mistral AI — released under the Apache License 2.0  

- [**all-MiniLM-L6-v2**](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)  
  © 2021 Sentence Transformers / UKPLab — released under the Apache License 2.0
