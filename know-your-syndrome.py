from PIL import Image
import pandas as pd
import streamlit as st

im = Image.open('DNA.jpeg')
st.set_page_config(page_title='Genetic Syndromes', page_icon=im)
image = Image.open('NIH.png')
st.sidebar.image(image)
st.sidebar.header('Medical Genetics Training Program')
df_syndromes = pd.read_csv('df_for_app.csv', sep=',', usecols=['Genetics', 'Clinical findings/Dysmorphic features',
                                                               'Etiology', 'Pathogenesis', 'Genetic testing/diagnosis',
                                                               'Others', 'Syndrome name',
                                                               'Category', 'png links', 'figure'])

st.header('Know your syndromes')
st.markdown(f"**This app currently contains {len(df_syndromes['Syndrome name'])} genetic conditions**")
st.markdown('by Oskar Schnappauf')

df_syndromes.fillna('no information', inplace=True)
df_syndromes['Genetics'] = df_syndromes['Genetics'].str.strip(', ')
df_syndromes['Clinical findings/Dysmorphic features'] = df_syndromes['Clinical findings/Dysmorphic features'].str.strip(', ')
df_syndromes['Etiology'] = df_syndromes['Etiology'].str.strip(', ')
df_syndromes['Pathogenesis'] = df_syndromes['Pathogenesis'].str.strip(', ')
df_syndromes['Genetic testing/diagnosis'] = df_syndromes['Genetic testing/diagnosis'].str.strip(', ')
df_syndromes['Others'] = df_syndromes['Others'].str.strip(', ')

df_syndromes['Genetics'] = df_syndromes['Genetics'].str.replace(", -", "\n\n-")
df_syndromes['Clinical findings/Dysmorphic features'] = df_syndromes['Clinical findings/Dysmorphic features'].str.replace(", -", "\n\n-")
df_syndromes['Etiology'] = df_syndromes['Etiology'].str.replace(", -", "\n\n-")
df_syndromes['Pathogenesis'] = df_syndromes['Pathogenesis'].str.replace(", -", "\n\n-")
df_syndromes['Genetic testing/diagnosis'] = df_syndromes['Genetic testing/diagnosis'].str.replace(", -", "\n\n-")
df_syndromes['Others'] = df_syndromes['Others'].str.replace(", -", "\n\n-")

df_all = df_syndromes[['Syndrome name', 'Category']].sort_values('Syndrome name')

st.subheader('All syndromes')
main_search = st.text_input('Search all syndromes', key='main_search')
main_category = st.multiselect('Filter by category (optional)', sorted(df_syndromes['Category'].unique()), key='main_category')

df_main = df_all
if main_search:
    df_main = df_main[df_main['Syndrome name'].str.contains(main_search, case=False, na=False)]
if main_category:
    df_main = df_main[df_main['Category'].isin(main_category)]

st.dataframe(df_main, use_container_width=True, hide_index=True)
main_choice = st.selectbox(f'View details for one of {len(df_main)} syndromes', ['-'] + df_main['Syndrome name'].tolist(), key='main_choice')
if main_choice != '-':
    df_final = df_syndromes[df_syndromes['Syndrome name'] == main_choice]
    show_syndrome(main_choice, df_final)


def show_syndrome(user_syndrome, df):
    st.subheader(user_syndrome)
    try:
        image_syn = Image.open(df.iloc[0]['png links'])
        st.sidebar.image(image_syn, caption=user_syndrome)
    except FileNotFoundError:
        pass
    expander_figure = st.expander('Figure')
    expander_genetics = st.expander('Genetics')
    expander_clinical_findings = st.expander('Clinical findings/Dysmorphic features')
    expander_etiology = st.expander('Etiology')
    expander_pathogenesis = st.expander('Pathogenesis')
    expander_genetic_testing = st.expander('Genetic testing/diagnosis')
    expander_others = st.expander('Others')

    with expander_figure:
        try:
            image_syn = Image.open(df.iloc[0]['figure'])
            st.image(image_syn, caption=user_syndrome)
        except FileNotFoundError:
            pass
    with expander_genetics:
        st.markdown(f"{df.iloc[0]['Genetics']}")
    with expander_clinical_findings:
        st.markdown(f"{df.iloc[0]['Clinical findings/Dysmorphic features']}")
    with expander_etiology:
        st.markdown(f"{df.iloc[0]['Etiology']}")
    with expander_pathogenesis:
        st.markdown(f"{df.iloc[0]['Pathogenesis']}")
    with expander_genetic_testing:
        st.markdown(f"{df.iloc[0]['Genetic testing/diagnosis']}")
    with expander_others:
        st.markdown(f"{df.iloc[0]['Others']}")


keyword = st.sidebar.text_input('Find syndrome by keyword')
st.sidebar.markdown(f'or')
category = st.sidebar.multiselect('Find syndrome by category', sorted(df_syndromes['Category'].unique()))

if keyword and category:
    df_1 = df_syndromes[df_syndromes.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
    df_2 = df_syndromes[df_syndromes['Category'].isin(category)]
    df_merged = pd.concat([df_1, df_2], axis=0)
    syndromes = sorted(df_merged['Syndrome name'])
    user_syndrome_both = st.sidebar.selectbox(f'Choose one of {len(syndromes)} syndromes', ['-'] + syndromes)
    df_final = df_merged[df_merged['Syndrome name'] == user_syndrome_both]
    if user_syndrome_both != '-':
        show_syndrome(user_syndrome_both, df_final)

elif keyword:
    df_filtered_keyword = df_syndromes[df_syndromes.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
    syndromes = sorted(df_filtered_keyword['Syndrome name'])
    user_syndrome_keyword = st.sidebar.selectbox(f'Choose one of {len(syndromes)} syndromes', ['-'] + syndromes)
    df_final = df_filtered_keyword[df_filtered_keyword['Syndrome name'] == user_syndrome_keyword]
    if user_syndrome_keyword != '-':
        show_syndrome(user_syndrome_keyword, df_final)

elif category:
    df_filtered_category = df_syndromes[df_syndromes['Category'].isin(category)]
    syndromes = sorted(df_filtered_category['Syndrome name'])
    user_syndrome_category = st.sidebar.selectbox(f'Choose one of {len(syndromes)} syndromes', ['-'] + syndromes)
    df_final = df_filtered_category[df_filtered_category['Syndrome name'] == user_syndrome_category]
    if user_syndrome_category != '-':
        show_syndrome(user_syndrome_category, df_final)
