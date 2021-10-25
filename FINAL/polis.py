#bibliotecas:
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from datetime import datetime
import plotly.graph_objects as go


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Polis", page_icon=":bar_chart:", layout="wide")


@st.cache(allow_output_mutation=True)
def get_data(path):
    df = pd.read_csv( "dados_gerais.csv" , sep=",", encoding="ISO-8859-1" )

    return df

def set_feature( df ):
    df['1° Dose']        = np.where(df['nova_dose'] == '1 Dose', 1, 0)
    df['2° Dose']        = np.where(df['nova_dose'] == '2 Dose', 1, 0)
    df['Dose Única']     = np.where(df['nova_dose'] == 'Dose Unica', 1, 0)
    df['Dose Adicional'] = np.where(df['nova_dose'] == 'Dose Adicional', 1, 0)

    df['Feminino']  = np.where(df['paciente_enumsexobiologico'] == 'Feminino', 1, 0)
    df['Masculino'] = np.where(df['paciente_enumsexobiologico'] == 'Masculino', 1, 0)

    df['Covishield']  = np.where(df['vacina_nome'] == 'Covishield', 1, 0)
    df['Pfizer']      = np.where(df['vacina_nome'] == 'Pfizer', 1, 0)
    df['Coronavac']   = np.where(df['vacina_nome'] == 'Coronavac', 1, 0)
    df['Janssen']     = np.where(df['vacina_nome'] == 'Janssen', 1, 0)
    df['AstraZeneca'] = np.where(df['vacina_nome'] == 'AstraZeneca', 1, 0)

    df['BRANCA']         = np.where(df['paciente_racacor_valor'] == 'BRANCA', 1, 0)
    df['PRETA']          = np.where(df['paciente_racacor_valor'] == 'PRETA', 1, 0)
    df['PARDA']          = np.where(df['paciente_racacor_valor'] == 'PARDA', 1, 0)
    df['AMARELA']        = np.where(df['paciente_racacor_valor'] == 'AMARELA', 1, 0)
    df['INDIGENA']       = np.where(df['paciente_racacor_valor'] == 'INDIGENA', 1, 0)
    df['SEM INFORMACAO'] = np.where(df['paciente_racacor_valor'] == 'SEM INFORMACAO', 1, 0)

    df_selection = df

    return df_selection



# --------------------------------------------------------------- TOP ----
def overview_data( df_selection ):

    st.title("Polis - Visualização e Análise de Dados Abertos")
    st.markdown("""###""")
    st.markdown("""---""")

    return None

# 1 - Análise da Vacinação contra COVID-19 em Florianópolis - SC ------------------------------

# 1.1 - Proporção da População Vacinada --------------------------------------------------------

def pie3_popvac( df_selection ):
    st.header("1 - Análise da Campanha de Vacinação contra COVID-19 em Florianópolis - SC")
    st.markdown("""---""")
    st.subheader("1.0 - Descrição dos Dados")
    st.markdown("Os dashboards a seguir apresenta os Dados referentes à **Campanha de Vacinação contra Covid-19,"
                "da população residente em Florianópolis/SC**, sendo dispníbilizados neste formato para vizualização, análise e aprofundamento da sociedade. "
                "*Link para os Dados Abertos no rodapé*")
    st.markdown("""---""")
    st.subheader("1.1 - Proporção da População Vacinada")
    st.markdown("""###""")
    c1, c2, c3 = st.columns((1, 1, 1))

# DECLARAÇÂO DE VARIAVEIS - 1.1A - População sem Nenhuma Dose ------------------------------------
    popul_residente = int(516524)
    vacinados_1dose = int(df_selection['1° Dose'].sum())
    vacinados = int(df_selection['1° Dose'].sum() + df_selection['Dose Única'].sum())
    vacinados_completo = int(df_selection['2° Dose'].sum() + df_selection['Dose Única'].sum())

    pop_sem_vac = (popul_residente - vacinados_1dose + df_selection['Dose Única'].sum())
    pop_sem_1dose = (popul_residente - vacinados_1dose)
    pop_sem_2dose = (popul_residente - vacinados_completo)

    labels1 = ['População com alguma Dose da Vacina','População sem Dose da Vacina']
    colors1 = ['#4169E1', '#D70270'] # roualblue / magenta

# PLOTAGEM GRÀFICO DE PIZZA - 1.1A: --------------------------------------------------------------
    fig1 = go.Figure(data=[go.Pie(labels=labels1,
                                  values=[vacinados, pop_sem_vac],
                                  textinfo='percent', textfont_size=20,
                                  marker=dict(colors=colors1,
                                              line=dict(color='#000010', width=2)))])
    fig1.update_traces(hole=.4, hoverinfo="label+percent+value")
    fig1.update_layout(
        title="1.1A - População sem Nenhuma Dose:",
        title_font_size=20, legend_font_size=14,
        template="plotly_dark",
        width=500, height=500,
        legend=dict(
            x=0.0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'))

# DECLARAÇÂO DE VARIAVEIS - 1.1B - Vacinados com 1° Dose: ---------------------------------------
    labels2 = ['População com 1° Dose' , "População sem 1° Dose"]
    colors2 = ['#D70270','#4169E1']

# PLOTAGEM GRÀFICO DE PIZZA - 1.1B: --------------------------------------------------------------
    fig2 = go.Figure(data=[go.Pie(labels=labels2,
                      values=[vacinados_1dose, pop_sem_1dose],
                      textinfo='percent', textfont_size=20,
                      marker=dict(colors=colors2,
                                  line=dict(color='#000010', width=2)))])
    fig2.update_traces(hole=.4, hoverinfo="label+percent+value")
    fig2.update_layout(
        title_text="1.1B - População com 1° Dose:",
        title_font_size=20, legend_font_size=14,
        template="plotly_dark",
        width=500, height=500,
        legend=dict(
            x=0.0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'))

# DECLARAÇÂO DE VARIAVEIS - 1.1C - Vacinados Completamente: ---------------------------------------
    labels3 = ['Vacinados Completamente','Não Vacinados Completamente']
    colors3 = ['#D70270','#4169E1']

# PLOTAGEM GRÀFICO DE PIZZA - 1.1B: ---------------------------------------------------------------
    fig3 = go.Figure(data=[go.Pie(labels=labels3,
                      values=[vacinados_completo, pop_sem_2dose],
                      textinfo='percent', textfont_size=20,
                      marker=dict(colors=colors3,
                                  line=dict(color=' #000010', width=2)))])
    fig3.update_traces(hole=.4, hoverinfo="label+percent+value")
    fig3.update_layout(
        title_text="1.1C - População Vacinada Completamente:",
        title_font_size=20, legend_font_size=14,
        template="plotly_dark",
        width=500, height=500,
        legend=dict(
            x=0.0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'))

    c1.plotly_chart(fig1, use_container_width=True)
    c2.plotly_chart(fig2, use_container_width=True)
    c3.plotly_chart(fig3, use_container_width=True)
    st.markdown("""---""")
    st.markdown("""###""")

    return None

# 1.2 - Análise Temporal das Doses Aplicadas Durante a Vacinação

def temp_dose( df_selection ):
    st.subheader("1.2 - Análise Temporal das Doses Aplicadas Durante a Vacinação")
    c1, c2 = st.columns((1, 1))

# ------------------- PREPARAÇÂO DOS DADOS - 1.2A - Variação Mensal da Aplicação das Doses:
    df_line = df_selection.groupby(['meses_aplicacao']).sum().reset_index()

# ------------------- PLOTAGEM GRÀFICO DE LINHA - 1.2A:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
         x= df_line['meses_aplicacao'],
         y =df_line['1° Dose'],
         name ='1° Dose',
         mode ='lines',
         line=dict(width=3, color='royalblue')))
    fig1.add_trace(go.Scatter(
         x=df_line['meses_aplicacao'],
         y=df_line['2° Dose'],
         name='2° Dose',
         mode='lines',
         line=dict(width=3, color='magenta')))
    fig1.add_trace(go.Scatter(
         x=df_line['meses_aplicacao'],
         y=df_line['Dose Única'],
         name='Dose Única',
         mode='lines',
         line=dict(width=3, color='darkviolet')))
    fig1.add_trace(go.Scatter(
         x=df_line['meses_aplicacao'],
         y=df_line['Dose Adicional'],
         name='Dose Adicional',
         mode='lines',
         line=dict(width=3, color='cyan')))
    fig1.update_layout(
         title="1.2A - Variação Mensal da Aplicação das Doses:",
         title_font_size=22, legend_font_size=14,
         template="plotly_dark",
         width=600, height=500,
         legend=dict(
         x=0.0,
         y=1.0,
         bgcolor='rgba(255, 255, 255, 0)',
         bordercolor='rgba(255, 255, 255, 0)'))
    fig1.update_xaxes(
         title_text='Mês da Aplicação da Vacina',
         title_font=dict(size=16, family='Sans-serif'),
         tickfont  =dict(size=12, family='Sans-serif'),
         rangeslider_visible=True)
    fig1.update_yaxes(
         title_text = "Número de Vacinados",
         title_font=dict(size=16, family='Sans-serif'),
         tickfont  =dict(size=12, family='Sans-serif'))

# ------------------- PREPARAÇÂO DOS DADOS - 1.2B - Variação Diária da Aplicação das Doses:
    df_area = df_selection.groupby(['vacina_dataaplicacao']).sum().reset_index()

# ------------------- PLOTAGEM GRÀFICO DE AREA - 1.2B:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
         x=df_area['vacina_dataaplicacao'],
         y=df_area['Dose Adicional'],
         name='Dose Adicional',
         mode='lines',
         line=dict(width=1, color='cyan'),
         stackgroup='four'))
    fig2.add_trace(go.Scatter(
        x=df_area['vacina_dataaplicacao'],
        y=df_area['Dose Única'],
        name='Dose Única',
        mode='lines',
        line=dict(width=1, color='darkviolet'),
        stackgroup='two'))
    fig2.add_trace(go.Scatter(
        x=df_area['vacina_dataaplicacao'],
        y=df_area['2° Dose'],
        name='2° Dose',
        mode='lines',
        line=dict(width=1, color='magenta'),
        stackgroup='three'))
    fig2.add_trace(go.Scatter(
         x=df_area['vacina_dataaplicacao'],
         y=df_area['1° Dose'],
         name='1° Dose',
         mode='lines',
         line=dict(width=1, color='royalblue'),
         stackgroup='one'))
    fig2.update_layout(
         title="1.2B - Variação Diária da Aplicação das Doses:",
         title_font_size=22, legend_font_size=14,
         template="plotly_dark",
         width=600, height=500,
         legend=dict(
         x=0.0,
         y=1.0,
         bgcolor='rgba(255, 255, 255, 0)',
         bordercolor='rgba(255, 255, 255, 0)' ))
    fig2.update_xaxes(
         title_text = 'Dia da Aplicação da Vacina',
         title_font=dict(family='Sans-serif', size=16),
         tickfont  =dict(family='Sans-serif', size=12),
         rangeslider_visible=True)
    fig2.update_yaxes(
         title_text = "Vacinados por Dose Aplicada",
         title_font=dict(family='Sans-serif', size=16),
         tickfont  =dict(family='Sans-serif', size=12))

    c1.plotly_chart(fig1, use_container_width=True)
    c2.plotly_chart(fig2, use_container_width=True)
    st.markdown("""---""")

    return None

# 1.3 - Análise das Vacinas Aplicadas -----------------------------------------------------------

def bar_fun_vacina( df_selection ):
    st.subheader("1.3 - Análise das Vacinas Aplicadas")
    c1, c2 = st.columns((1, 1))

# ------------------- PREPARAÇÂO DOS DADOS - 1.3A - Vacinas Aplicadas por Dose:
    df_selection['Covishield'] = np.where(df_selection['vacina_nome'] == 'Covishield', 1, 0)
    df_selection['Pfizer'] = np.where(df_selection['vacina_nome'] == 'Pfizer', 1, 0)
    df_selection['Coronavac'] = np.where(df_selection['vacina_nome'] == 'Coronavac', 1, 0)
    df_selection['Janssen'] = np.where(df_selection['vacina_nome'] == 'Janssen', 1, 0)
    df_selection['AstraZeneca'] = np.where(df_selection['vacina_nome'] == 'AstraZeneca', 1, 0)

    df = df_selection.groupby(['nova_dose']).sum().reset_index()

    values = ['1° Dose', '2° Dose', 'Dose Única', 'Dose Reforço']
    y_Covishield = [df['Covishield'][0], df['Covishield'][1], df['Covishield'][3], df['Covishield'][2]]
    y_Pfizer = [df['Pfizer'][0], df['Pfizer'][1], df['Pfizer'][3], df['Pfizer'][2]]
    y_AstraZeneca = [df['AstraZeneca'][0], df['AstraZeneca'][1], df['AstraZeneca'][3], df['AstraZeneca'][2]]
    y_Coronavac = [df['Coronavac'][0], df['Coronavac'][1], df['Coronavac'][3], df['Coronavac'][2]]
    y_Janssen = [df['Janssen'][0], df['Janssen'][1], df['Janssen'][3], df['Janssen'][2]]

# ------------------- PLOTAGEM GRÀFICO DE BARRA - 1.3A - Vacinas Aplicadas por Dose:
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name='Covishield', x=values, y=y_Covishield,
                         text=y_Covishield, textposition='auto',
                         marker_color=['#D70270', '#D70270', '#D70270', '#D70270', '#D70270'])) #magenta
    fig1.add_trace(go.Bar(name='Pfizer', x=values, y=y_Pfizer,
                         text=y_Pfizer, textposition='auto',
                         marker_color=['#4169E1', '#4169E1', '#4169E1', '#4169E1', '#4169E1'])) #royalazul
    fig1.add_trace(go.Bar(name='AstraZeneca', x=values, y=y_AstraZeneca,
                         text=y_AstraZeneca, textposition='auto',
                         marker_color=['#ADFF2F', '#ADFF2F', '#ADFF2F', '#ADFF2F', '#ADFF2F'])) #Navy
    fig1.add_trace(go.Bar(name='Coronavac', x=values, y=y_Coronavac,
                         text=y_Coronavac, textposition='auto',
                         marker_color=['#8A2BE2', '#8A2BE2', '#8A2BE2', '#8A2BE2', '#8A2BE2'])) #Purple
    fig1.add_trace(go.Bar(name='Janssen', x=values, y=y_Janssen,
                         text=y_Janssen, textposition='auto',
                         marker_color=['#00FFFF', '#00FFFF', '#00FFFF', '#00FFFF', '#00FFFF']))
    fig1.update_layout(
        title="1.3A - Vacinas Aplicadas por Dose:",
        title_font_size=20, legend_font_size=14,
        template="plotly_dark",
        barmode='stack',
        width=600, height=500,
        legend=dict(
            x=0.75,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'))
    fig1.update_xaxes(
        title_text='Doses Aplicadas',
        title_font=dict(family='Sans-serif', size=16),
        tickfont  =dict(family='Sans-serif', size=12))
    fig1.update_yaxes(
        title_text="Número de Vacinados",
        title_font=dict(family='Sans-serif', size=16),
        tickfont  =dict(family='Sans-serif', size=12))

# PREPARAÇÂO DOS DADOS - 1.3B - Vacinas Aplicadas por Dose: -------------------------------------
    y_Covishield = int(df_selection['Covishield'].sum())
    y_Pfizer = int(df_selection['Pfizer'].sum())
    y_Coronavac = int(df_selection['Coronavac'].sum())
    y_Janssen = int(df_selection['Janssen'].sum())
    y_AstraZeneca = int(df_selection['AstraZeneca'].sum())

    values = ["Covishield", "Pfizer", "Coronavac", "Janssen", "AstraZeneca"]
    y = [y_Covishield, y_Pfizer, y_Coronavac, y_Janssen, y_AstraZeneca]

# ------------------- PLOTAGEM GRÀFICO DE BARRA - 1.3B - Proporção das Vacinas Aplicadas:
    fig2 = go.Figure()
    fig2.add_trace(go.Funnel(
        y=values, x=y,
        textposition="inside",
        textinfo="value+percent total",
        opacity=1, marker={"color": ["#D70270", "#4169E1", "#8A2BE2", "#00FFFF", "#ADFF2F"],
                           "line": {"width": [2, 2, 2, 2, 2, 2],
                                    "color": ["black", "black", "black", "black", "black"]}},
        connector={"line": {"color": "black", "dash": "solid", "width": 2}}))
    fig2.update_layout(
        title="1.3B - Proporção das Vacinas Aplicadas:",
        title_font_size=20,
        template="plotly_dark",
        width=600, height=500)
    fig2.update_yaxes(
        tickfont=dict(family='Sans-serif', size=16))

    c1.plotly_chart(fig1, use_container_width=True)
    c2.plotly_chart(fig2, use_container_width=True)
    st.markdown("""---""")

    return None

# 1.4 - Análise Temporal das Vacinas Aplicadas -------------------------------

def line_temp_vacina( df_selection ):
    st.subheader("1.4 - Análise Temporal das Vacinas Aplicadas")
    st.markdown("""###""")
    c1, c2 = st.columns((1, 1))

# PREPARAÇÂO DOS DADOS - 1.4A - Variação Mensal da Aplicação da Vacinas: ----------------------------
    df_area = df_selection.groupby(['meses_aplicacao']).sum().reset_index()

# PLOTAGEM GRÀFICO DE BARRA - 1.4A - Variação Mensal da Aplicação da Vacinas: ------------------------
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df_area['meses_aplicacao'],
        y=df_area['Covishield'],
        name='Covishield',
        mode='lines',
        line=dict(width=2, color="#D70270")))
    fig1.add_trace(go.Scatter(
        x=df_area['meses_aplicacao'],
        y=df_area['Pfizer'],
        name='Pfizer',
        mode='lines',
        line=dict(width=2, color="#4169E1")))
    fig1.add_trace(go.Scatter(
        x=df_area['meses_aplicacao'],
        y=df_area['Coronavac'],
        name='Coronavac',
        mode='lines',
        line=dict(width=2, color='#8A2BE2')))
    fig1.add_trace(go.Scatter(
        x=df_area['meses_aplicacao'],
        y=df_area['Janssen'],
        name='Janssen',
        mode='lines',
        line=dict(width=2, color='#00FFFF')))
    fig1.add_trace(go.Scatter(
        x=df_area['meses_aplicacao'],
        y=df_area['AstraZeneca'],
        name='AstraZeneca',
        mode='lines',
        line=dict(width=2, color='#ADFF2F')))
    fig1.update_layout(
        title="1.4A - Variação Mensal da Aplicação das Vacinas:",
        title_font_size=20, legend_font_size=14,
        template="plotly_dark",
        width=600, height=500,
        legend=dict(
            x=0.0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'))
    fig1.update_xaxes(
        title_text='Mês da Aplicação da Vacina',
        title_font=dict(family='Sans-serif', size=16),
        tickfont  =dict(family='Sans-serif', size=12),
        rangeslider_visible=True)
    fig1.update_yaxes(
        title_text="Número de Vacinados",
        title_font=dict(family='Sans-serif', size=16),
        tickfont  =dict(family='Sans-serif', size=12))

# PREPARAÇÂO DOS DADOS - 1.4A - Variação Mensal da Aplicação da Vacinas: --------------------------
    df_area = df_selection.groupby(['vacina_dataaplicacao']).sum().reset_index()

# PLOTAGEM GRÀFICO DE BARRA - 1.4A - Variação Mensal da Aplicação da Vacinas: ----------------------
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df_area['vacina_dataaplicacao'],  # a name of a column in data_frame representing the timeline
        y=df_area['Covishield'],  # a name of a column in data_frame representing the statistic calculated
        name='Covishield',
        mode='lines',
        line=dict(width=1, color='#D70270'),
        stackgroup='one'))
    fig2.add_trace(go.Scatter(
        x=df_area['vacina_dataaplicacao'],
        y=df_area['Pfizer'],
        name='Pfizer',
        mode='lines',
        line=dict(width=1, color='#4169E1'),
        stackgroup='two'))
    fig2.add_trace(go.Scatter(
        x=df_area['vacina_dataaplicacao'],
        y=df_area['Coronavac'],
        name='Coronavac',
        mode='lines',
        line=dict(width=1, color='#8A2BE2'),
        stackgroup='four'))
    fig2.add_trace(go.Scatter(
        x=df_area['vacina_dataaplicacao'],
        y=df_area['Janssen'],
        name='Janssen',
        mode='lines',
        line=dict(width=1, color='#00FFFF'),
        stackgroup='five'))
    fig2.add_trace(go.Scatter(
        x=df_area['vacina_dataaplicacao'],
        y=df_area['AstraZeneca'],
        name='AstraZeneca',
        mode='lines',
        line=dict(width=1, color='#ADFF2F'),
        stackgroup='three'))
    fig2.update_layout(
        title="1.4B - Variação Diária da Aplicação das Vacinas:",
        title_font_size=20, legend_font_size=14,
        template="plotly_dark",
        width=600, height=500,
        legend=dict(
            x=0.0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'))
    fig2.update_xaxes(
        title_text='Dia da Aplicação da Vacina',
        title_font=dict(family='Sans-serif', size=16),
        tickfont  =dict(family='Sans-serif', size=12),
        rangeslider_visible=True)
    fig2.update_yaxes(
        title_text="Número de Vacinados",
        title_font=dict(family='Sans-serif', size=16),
        tickfont  =dict(family='Sans-serif', size=12))

    c1.plotly_chart(fig1, use_container_width=True)
    c2.plotly_chart(fig2, use_container_width=True)
    st.markdown("""---""")

    return None

# 2 - Características das População Vacinadas em Florianópolis - SC ------------------------------

def pie3_cacsexo( df_selection ):

    st.header("2 - Características da População Vacinada em Florianópolis/SC")
    st.markdown("""---""")
    st.subheader("2.0 - Coxtexto")
    st.markdown("""###""")
    st.markdown("Os dashboards a seguir apresentam as características documentadas durante a Campanha de Vacinação Contra Covid-19, dos  residentes de Florianópolis/SC.")
    st.markdown("Para melhor contraste e aprofundamento durante a análise, utilizou-se dos Dados do CENSO-2010 (IBGE) para estimar as características da população em 2020. As Informações que utilizam desta estimativa conterão - *")
    st.markdown("""###""")
    st.markdown("""---""")

# 2.1 - Proporção da População Vacinada --------------------------------------------------------
    st.markdown("""###""")
    st.subheader("2.1 - Sexo Biológico dos Vacinados")
    st.markdown("""###""")
    c1, c2, c3 = st.columns((1, 1, 1))

# DECLARAÇÂO DE VARIAVEIS - 2.1A - Proporção entre os Sexos: ------------------------------------
    df_selection1 = df_selection.drop_duplicates(subset=['paciente_id'], keep="last")

    popul_femi = int( 268592 )
    popul_masc = int( 247931 )
    vacinados_femi = int( df_selection1['Feminino'].sum() )
    vacinados_masc = int( df_selection1['Masculino'].sum() )
    pop_femi_sem = ( popul_femi - vacinados_femi)
    pop_masc_sem = ( popul_masc - vacinados_masc )

    labels1 = ['Sexo Feminino com 1°Dose ou Mais','Sexo Masculino com 1°Dose ou Mais']
    colors1 = ['#D70270', '#4169E1'] #  magenta | royalblue

# PLOTAGEM GRÀFICO DE PIZZA - 2.1A - Proporção entre os Sexos: --------------------------------------------------------------
    fig1 = go.Figure(data=[go.Pie(labels=labels1,
                      values=[vacinados_femi, vacinados_masc],
                      textinfo='percent', textfont_size=20,
                      marker=dict(colors=colors1,
                                  line=dict(color='#000010', width=2)))])
    fig1.update_traces(hole=.4, hoverinfo="label+percent+value")
    fig1.update_layout(
        title_text="2.1A - Proporção entre os Sexos:",
        title_font_size=20, legend_font_size=12,
        template="plotly_dark",
        width=600, height=500,
        legend=dict(
            x=0.0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'))

# DECLARAÇÂO DE VARIAVEIS - 2.1B - Sexo Feminino com 1° Dose ou Mais: ---------------------------------
    labels2 = ["Sexo Feminino sem Vacina", 'Sexo Feminino com 1°Dose ou Mais']
    colors2 = ['#4169E1', '#D70270'] # royalblue / magenta

# PLOTAGEM GRÀFICO DE PIZZA - 2.1B - Sexo Feminino com 1° Dose ou Mais: ---------------------------------------
    fig2 = go.Figure(data=[go.Pie(labels=labels2,
                      values=[pop_femi_sem, vacinados_femi],
                      textinfo='percent', textfont_size=20,
                      marker=dict(colors=colors2,
                                  line=dict(color='#000010', width=2)))])
    fig2.update_traces(hole=.4, hoverinfo="label+percent+value")
    fig2.update_layout(
        title_text="2.1B - Sexo Feminino com 1° Dose ou Mais:",
        title_font_size=20, legend_font_size=12,
        template="plotly_dark",
        width=600, height=500,
        legend=dict(
            x=0.0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'))

# DECLARAÇÂO DE VARIAVEIS - 2.1C - Sexo Masculino com 1° Dose ou Mais: ------------------------------------
    labels3 = ["Sexo Masculino sem Vacina", 'Sexo Masculino com 1°Dose ou Mais']
    colors3 = ['#4169E1', '#D70270'] # royalblue / magenta

# PLOTAGEM GRÀFICO DE PIZZA - 2.1C - Sexo Masculino com 1° Dose ou Mais: --------------------------------------------------------------
    fig3 = go.Figure(data=[go.Pie(labels=labels3,
                      values=[pop_masc_sem, vacinados_masc],
                      textinfo='percent', textfont_size=20,
                      marker=dict(colors=colors3,
                                  line=dict(color=' #000010', width=2)))])
    fig3.update_traces(hole=.4, hoverinfo="label+percent+value")
    fig3.update_layout(
        title_text="2.1C - Sexo Masculino com 1° Dose ou Mais:",
        title_font_size=20, legend_font_size=12,
        template="plotly_dark",
        width=600, height=500,
        legend=dict(
            x=0.0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'))

    c1.plotly_chart(fig1, use_container_width=True)
    c2.plotly_chart(fig2, use_container_width=True)
    c3.plotly_chart(fig3, use_container_width=True)
    st.markdown("""---""")
    st.markdown("""###""")

    return None

def bar_line_cor( df_selection ):
# 2.2 - Raça e Cor da População Vacinada  --------------------------------------------------------
    st.subheader("2.2 - Análise da Raça/Cor da População Vacinada em Florianópolis/SC")
    c1, c2 = st.columns((1, 1))

# 2.2 -  DECLARAÇÂO DE VARIAVEIS GERAIS ------------------------------------
    dados = df_selection.drop_duplicates(subset=['paciente_id'], keep="last")

    popul_branca = int(436722)
    popul_parda = int(50258)
    popul_preta = int(25568)
    popul_amarela = int(2686)
    popul_indigena = int(1239)
    vacinados_branca = int(dados['BRANCA'].sum())
    vacinados_parda = int(dados['PARDA'].sum())
    vacinados_preta = int(dados['PRETA'].sum())
    vacinados_amarela = int(dados['AMARELA'].sum())
    vacinados_indigena = int(dados['INDIGENA'].sum())
    vacinados_seminfo = int(dados['SEM INFORMACAO'].sum())

# 2.2A - Raça/Cor da População Residente e População Vacinada Completamente - DECLARAÇÂO DE VARIAVEIS ------------------------------------
    raca_vacina = ['Branca', 'Parda', 'Preta', 'Amarela', 'Indigena', 'Sem Informação']

    y_popul = [popul_branca, popul_preta, popul_parda, popul_amarela, popul_indigena, 0]
    y_vacina = [vacinados_branca, vacinados_preta, vacinados_parda, vacinados_amarela, vacinados_indigena,
                vacinados_seminfo]

# 2.2A - Raça/Cor da População Residente e População Vacinada Completamente - PLOTAGEM GRÀFICO DE BARRA - --------------------------------------------------------------
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name='População - Estimativa dos Residentes*', x=raca_vacina, y=y_popul,
               text=y_popul, textposition='outside',
               marker_color=['#4169E1', '#4169E1', '#4169E1', '#4169E1', '#4169E1', '#4169E1']))
    fig1.add_trace(go.Bar(name='População - Vacinada Alguma Dose', x=raca_vacina, y=y_vacina,
               text=y_vacina, textposition='outside',
               marker_color=['#D70270', '#D70270', '#D70270', '#D70270', '#D70270', '#D70270']))
    fig1.update_layout(
        title="2.2A - Raça/Cor da População Residente e População Vacinada:",
        title_font_size=20, legend_font_size=14,
        template="plotly_dark",
        barmode='group',
        width=600, height=500,
        legend=dict(
            x=0.35,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'))
    fig1.update_xaxes(
        title_text='Raça/Cor',
        title_font=dict(family='Sans-serif', size=16),
        tickfont  =dict(family='Sans-serif', size=12))
    fig1.update_yaxes(
        title_text="Número de Residentes/Vacinados",
        title_font=dict(family='Sans-serif', size=16),
        tickfont  =dict(family='Sans-serif', size=12))

# 2.2B - Distribuição da Idade dos Vacinados por Raça/Cor e Sexo Biológico - DECLARAÇÂO DE VARIAVEIS ------------------------------------

# 2.2B - Distribuição da Idade dos Vacinados por Raça/Cor e Sexo Biológico - PLOTAGEM GRÀFICO DE BARRA - --------------------------------------------------------------
    fig2 = go.Figure()
    fig2.add_trace(go.Violin(x=df_selection['paciente_racacor_valor'][df_selection['paciente_enumsexobiologico'] == 'Masculino'],
                            y=df_selection["paciente_idade"][df_selection['paciente_enumsexobiologico'] == 'Masculino'],
                            legendgroup='Masculino', scalegroup='Masculino', name='Masculino',
                            side='negative',
                            meanline_visible=True,
                            line_color='#4169E1',
                            fillcolor='#4169E1'))
    fig2.add_trace(go.Violin(x=df_selection['paciente_racacor_valor'][df_selection['paciente_enumsexobiologico'] == 'Feminino'],
                            y=df_selection["paciente_idade"][df_selection['paciente_enumsexobiologico'] == 'Feminino'],
                            legendgroup='Feminino', scalegroup='Feminino', name='Feminino',
                            side='positive',
                            meanline_visible=True,
                            line_color='#D70270',
                            fillcolor='#D70270'))
    fig2.update_layout(violingap=0, violinmode='overlay')
    fig2.update_layout(
        title="2.2B - Distribuição da Idade dos Vacinados por Raça/Cor e Sexo Biológico:",
        title_font_size=20,
        legend_font_size=14,
        template="plotly_dark",
        width=600, height=500,
        legend=dict(
            x=0.70,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'))
    fig2.update_xaxes(
        title_text='Raça/Cor',
        title_font=dict(family='Sans-serif', size=16),
        tickfont=dict(family='Sans-serif', size=9))
    fig2.update_yaxes(
        title_text="Idade dos Vacinados",
        title_font=dict(family='Sans-serif', size=16),
        tickfont=dict(family='Sans-serif', size=12))

    c1.plotly_chart(fig1, use_container_width=True)
    c2.plotly_chart(fig2, use_container_width=True)
    st.markdown("""---""")

    return None

def bar2_faixa( df_selection ):
# 2.3 - Análise da Faixa Etaria da População Vacinada em Florianópolis/SC
    st.subheader("2.3 - Análise da Faixa Etaria da População Vacinada em Florianópolis/SC")
    c1, c2 = st.columns((1, 1))

# 2.3 - DECLARAÇÂO DE VARIAVEIS GERAIS ------------------------------------
# 2.1B - Distribuição da Idade dos Vacinados por Raça/Cor e Sexo Biológico - PLOTAGEM GRÀFICO DE BARRA - --------------------------------------------------------------

    dados = df_selection.drop_duplicates(subset=['paciente_id'], keep="last")

    conditions = [
        (dados['paciente_idade'] <= 19),
        (dados['paciente_idade'] >= 20) & (dados['paciente_idade'] <= 39),
        (dados['paciente_idade'] >= 40) & (dados['paciente_idade'] <= 59),
        (dados['paciente_idade'] >= 60) & (dados['paciente_idade'] <= 79),
        (dados['paciente_idade'] >= 80)]
    values = ['menos 19 anos', '20 a 39 anos', '40 a 59 anos', '60 a 79 anos', 'mais 80 anos']
    dados['faixa_etaria'] = np.select(conditions, values)

    dados['menos 19 anos'] = np.where(dados['faixa_etaria'] == 'menos 19 anos', 1, 0)
    dados['20 a 39 anos'] = np.where(dados['faixa_etaria'] == '20 a 39 anos', 1, 0)
    dados['40 a 59 anos'] = np.where(dados['faixa_etaria'] == '40 a 59 anos', 1, 0)
    dados['60 a 79 anos'] = np.where(dados['faixa_etaria'] == '60 a 79 anos', 1, 0)
    dados['mais 80 anos'] = np.where(dados['faixa_etaria'] == 'mais 80 anos', 1, 0)

    df = dados.groupby(['faixa_etaria']).sum().reset_index()

# 2.3A - Faixa Etaria da População Residente e População Vacinada - DECLARAÇÂO DE VARIAVEIS ------------------------------------
    valuesf = ['menos 19 anos', '20 a 39 anos', '40 a 59 anos', '60 a 79 anos', 'mais 80 anos']
    y_pop = [132402, 191059, 133686, 51058, 8319]
    y_vac = [df['menos 19 anos'][4], df['20 a 39 anos'][0], df['40 a 59 anos'][1],
             df['60 a 79 anos'][2], df['mais 80 anos'][3]]

# 2.3A - Faixa Etaria da População Residente e População Vacinada - PLOTAGEM GRÀFICO DE BARRA - --------------------------------------------------------------
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name='População - Estimativa dos Residentes', x=valuesf, y=y_pop,
                         text=y_pop, textposition='outside',
                         marker_color=['#4169E1', '#4169E1',    '#4169E1', '#4169E1', '#4169E1']))
    fig1.add_trace(go.Bar(name='População - Vacinada Alguma Dose', x=values, y=y_vac,
                         text=y_vac, textposition='outside',
                         marker_color=['#D70270', '#D70270', '#D70270', '#D70270', '#D70270']))
    fig1.update_layout(
        title="2.3A - Faixa Etaria da População Residente e População Vacinada:",
        title_font_size=20, legend_font_size=14,
        template="plotly_dark",
        barmode='group',
        width=600, height=500,
        legend=dict(
            x=0.35,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'))
    fig1.update_xaxes(
        title_text='Faixa Etaria',
        title_font=dict(family='Sans-serif', size=16),
        tickfont  =dict(family='Sans-serif', size=12))
    fig1.update_yaxes(
        title_text="Número de Residentes/Vacinados",
        title_font=dict(family='Sans-serif', size=16),
        tickfont  =dict(family='Sans-serif', size=12))

# 2.3A - Faixa Etaria da População Residente e População Vacinada - DECLARAÇÂO DE VARIAVEIS ------------------------------------
    values = ['menos 19 anos', '20 a 39 anos', '40 a 59 anos', '60 a 79 anos', 'mais 80 anos']

    y_1dose = [df['1° Dose'][4], df['1° Dose'][0], df['1° Dose'][1], df['1° Dose'][2], df['1° Dose'][3]]
    y_2dose = [df['2° Dose'][4], df['2° Dose'][0], df['2° Dose'][1], df['2° Dose'][2], df['2° Dose'][3]]
    y_Udose = [df['Dose Única'][4], df['Dose Única'][0], df['Dose Única'][1], df['Dose Única'][2], df['Dose Única'][3]]
    y_Adose = [df['Dose Adicional'][4], df['Dose Adicional'][0], df['Dose Adicional'][1], df['Dose Adicional'][2],
               df['Dose Adicional'][3]]
# 2.3A - Faixa Etaria da População Residente e População Vacinada - PLOTAGEM GRÀFICO DE BARRA - --------------------------------------------------------------
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(name='1° Dose', x=values, y=y_1dose,
                         text=y_pop, textposition='inside',
                         marker_color=['#4169E1', '#4169E1', '#4169E1', '#4169E1', '#4169E1']))
    fig2.add_trace(go.Bar(name='2° Dose', x=values, y=y_2dose,
                         text=y_vac, textposition='inside',
                         marker_color=['#D70270', '#D70270', '#D70270', '#D70270', '#D70270']))
    fig2.add_trace(go.Bar(name='Dose Única', x=values, y=y_Udose,
                         text=y_vac, textposition='inside',
                         marker_color=['#4B0082', '#4B0082', '#4B0082', '#4B0082', '#4B0082']))

    fig2.add_trace(go.Bar(name='Dose Adicional', x=values, y=y_Adose,
                         text=y_vac, textposition='inside',
                         marker_color=['#00FFFF', '#00FFFF', '#00FFFF', '#00FFFF', '#00FFFF']))
    fig2.update_layout(
        title="2.2B - Doses Aplicada em cada Faixa Etaria:",
        title_font_size=20, legend_font_size=14,
        template="plotly_dark",
        barmode='stack',
        width=600, height=500,
        legend=dict(
            x=0.65,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'))
    fig2.update_xaxes(
        title_text='Faixa Etaria',
        title_font=dict(family='Sans-serif', size=16),
        tickfont  =dict(family='Sans-serif', size=12))
    fig2.update_yaxes(
        title_text="Número de Doses Aplicadas",
        title_font=dict(family='Sans-serif', size=16),
        tickfont  =dict(family='Sans-serif', size=12))

    c1.plotly_chart(fig1, use_container_width=True)
    c2.plotly_chart(fig2, use_container_width=True)
    st.markdown("""---""")

    return None

def notas( df_selection  ):

    st.markdown("""###""")
    st.subheader( "Notas e Observações:")
    st.markdown(
        """Observação¹ : a população total contabilizada segue o Censo 2010 do IBGE, os gráficou não representam a realidade de cada sexo vacinado em 2021, representam uma estimativa com base nos dados disponíveis""")
    st.markdown(
        """Para Mais Informações¹: https://cidades.ibge.gov.br/brasil/sc/florianopolis/pesquisa/23/24304?indicador=29455 """)

    return None


#---------- ETL
if __name__ == "__main__":

    # Extration ---------------
    path = "dados_gerais.csv"
    df = get_data( path )


    # Transformation -----------------
    df_selection = set_feature( df )


    overview_data( df_selection )

    pie3_popvac( df_selection )

    temp_dose( df_selection )

    bar_fun_vacina( df_selection )

    line_temp_vacina( df_selection )

    #map_( df_selection )

#-----------------------------------2

    pie3_cacsexo( df_selection )

    bar_line_cor( df_selection )

    bar2_faixa( df_selection )


    # Loading ------------------------


    notas( df_selection )