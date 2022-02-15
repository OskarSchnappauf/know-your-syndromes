from PIL import Image
import pandas as pd
import streamlit as st

im = Image.open('DNA.jpeg')
st.set_page_config(page_title='Genetic Syndromes', page_icon=im)
image = Image.open('NIH.png')
st.image(image)
st.header('Medical Genetics Training Program')
st.subheader('Know your syndromes')
st.markdown('by Oskar Schnappauf')
df_syndromes = pd.read_csv('Syndromes_for_df_png.csv', sep=';')

df_syndromes.fillna('no information', inplace=True)
df_syndromes['Genetics'] = df_syndromes['Genetics'].str.strip(', ')
df_syndromes['Clinical findings/Dysmorphic features'] = df_syndromes['Clinical findings/Dysmorphic features'].str.strip(', ')
df_syndromes['Etiology'] = df_syndromes['Etiology'].str.strip(', ')
df_syndromes['Pathogenesis'] = df_syndromes['Pathogenesis'].str.strip(', ')
df_syndromes['Genetic testing/diagnosis'] = df_syndromes['Genetic testing/diagnosis'].str.strip(', ')
df_syndromes['Others'] = df_syndromes['Others'].str.strip(', ')

df_syndromes['Genetics'] = df_syndromes['Genetics'].str.replace(", -","\n\n-")
df_syndromes['Clinical findings/Dysmorphic features'] = df_syndromes['Clinical findings/Dysmorphic features'].str.replace(", -","\n\n-")
df_syndromes['Etiology'] = df_syndromes['Etiology'].str.replace(", -","\n\n-")
df_syndromes['Pathogenesis'] = df_syndromes['Pathogenesis'].str.replace(", -","\n\n-")
df_syndromes['Genetic testing/diagnosis'] = df_syndromes['Genetic testing/diagnosis'].str.replace(", -","\n\n-")
df_syndromes['Others'] = df_syndromes['Others'].str.replace(", -","\n\n-")

categories = df_syndromes['Category'].unique()
options = st.sidebar.multiselect('Choose a category',sorted(categories))
df_filtered = df_syndromes[df_syndromes['Category'].isin(options)]

syndromes = sorted(df_filtered['Syndrome name'])
user_syndrome = st.sidebar.selectbox(f'Choose one of {len(syndromes)} syndromes', ['-'] + syndromes)
#image = Image.open(df_filtered.iloc[0]['png links'])
#st.sidebar.image(image, caption=user_syndrome)
if user_syndrome != '-':
#    user_choice = st.radio("What do you want to do", ('Study', 'Get info'))
#    if user_choice == 'Get info':
    df_filtered = df_syndromes[df_syndromes['Syndrome name'] == user_syndrome]
    try:
        image = Image.open(df_filtered.iloc[0]['png links'])
        st.sidebar.image(image, caption=user_syndrome)
    except FileNotFoundError:
        pass
    st.subheader(user_syndrome)
    expander_genetics = st.expander('Genetics')
    expander_clinical_findings = st.expander('Clinical findings/Dysmorphic features')
    expander_etiology = st.expander('Etiology')
    expander_pathogenesis = st.expander('Pathogenesis')
    expander_genetic_testing = st.expander('Genetic testing/diagnosis')
    expander_others = st.expander('Others')

    with expander_genetics:
        st.markdown(f"{df_filtered.iloc[0]['Genetics']}")
    with expander_clinical_findings:
        st.markdown(f"{df_filtered.iloc[0]['Clinical findings/Dysmorphic features']}")
    with expander_etiology:
        st.markdown(f"{df_filtered.iloc[0]['Etiology']}")
    with expander_pathogenesis:
        st.markdown(f"{df_filtered.iloc[0]['Pathogenesis']}")
    with expander_genetic_testing:
        st.markdown(f"{df_filtered.iloc[0]['Genetic testing/diagnosis']}")
    with expander_others:
        st.markdown(f"{df_filtered.iloc[0]['Others']}")