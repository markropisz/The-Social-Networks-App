import streamlit as st

import pandas as pd

import pickle

import networkx as nx

from networkx.algorithms.community import greedy_modularity_communities
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, 'dataset.xlsx')



df = pd.read_excel(file_path, index_col=0, header=0) 

G = nx.from_pandas_edgelist(df, "Osoby", "Pliki")

Wierzcholki = pd.DataFrame(list(G.nodes()))

Wierzcholki = Wierzcholki[~Wierzcholki.isin([0, 1, 2, 3, 4, 5])]

Wierzcholki = Wierzcholki.dropna()

Wierzcholki = Wierzcholki.astype(int)




st.set_page_config(page_title='The Social Networks App',

    layout='wide')
st.write("The person you added belongs to the community number:")

with st.sidebar.header('Parametry'):

    parameter_nodes = st.multiselect("Downloaded files", Wierzcholki)


with st.sidebar.header('Parametry'):

    parameter_person = st.number_input('Person ID', min_value=6, max_value=999, value=6, label_visibility="visible")

st.sidebar.header("Instructions")
st.sidebar.markdown("""
This application will review a newly added person and check which community will that person be asigned to based on chosen files. To try it perform the following steps
- Step 1: Input your Person ID (or leave as default)
- Step 2: Select the list of downloaded files
- Step 3: Review the results
""")

if(len(parameter_nodes) > 0):
    parameter_person = [parameter_person] * len(parameter_nodes)

    data = list(zip(parameter_person, parameter_nodes))
    
    nowa = pd.DataFrame(data, columns=['Osoby', 'Pliki'])

    df_2 = df.append(nowa, ignore_index = True)

    G_2 = nx.from_pandas_edgelist(df_2, "Osoby", "Pliki")

    gmc = greedy_modularity_communities(G_2)

    for i in range(len(gmc)):
        if parameter_person[0] in list(gmc[i]):
            st.write(i)

