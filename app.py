import streamlit as st
import pandas as pd

# --- Configuração da Página ---
st.set_page_config(
    page_title="Busca de Valores de Convênios",
    page_icon="⚕️",
    layout="wide"
)

# --- Funções ---
@st.cache_data
def carregar_dados():
    """ Carrega os dados da tabela unificada de convênios. """
    try:
        # Garante que o ficheiro CSV está a ser lido corretamente
        df = pd.read_csv('tabela_unificada_convenios.csv', sep=';', decimal=',')
        return df
    except FileNotFoundError:
        st.error("Ficheiro 'tabela_unificada_convenios.csv' não encontrado. Certifique-se de que o ficheiro está na mesma pasta que a aplicação.")
        return None
    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar os dados: {e}")
        return None


def buscar_procedimento(df, nome_procedimento):
    """ Busca por um procedimento no DataFrame de convênios. """
    if df is not None and nome_procedimento:
        # Busca por correspondências parciais, ignorando maiúsculas/minúsculas
        resultados = df[df['Descricao'].str.contains(nome_procedimento, case=False, na=False)]
        return resultados.sort_values(by='Valor_HM', ascending=False)
    return pd.DataFrame() # Retorna um DataFrame vazio se não houver busca

# --- Interface da Aplicação ---

# Título da Aplicação
st.title("⚕️ Busca de Valores de Convênios")
st.markdown("Bem-vindo à sua ferramenta de busca de valores de procedimentos por convênio. "
            "Digite o nome do procedimento no campo abaixo para ver os valores correspondentes em cada tabela.")

# Carregar os dados
df_convenios = carregar_dados()

if df_convenios is not None:
    # Campo de busca
    termo_busca = st.text_input("Digite o nome do procedimento que deseja buscar:", placeholder="Ex: Consulta, Holter, Eletrocardiograma...")

    if termo_busca:
        resultados = buscar_procedimento(df_convenios, termo_busca)

        st.subheader(f"Resultados da busca por: '{termo_busca}'")

        if not resultados.empty:
            # Formatação dos resultados para exibição
            resultados_formatados = resultados.copy()
            # Formata a coluna de valor como moeda (Real Brasileiro)
            resultados_formatados['Valor_HM'] = resultados_formatados['Valor_HM'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

            # Exibe os resultados numa tabela interativa
            st.dataframe(resultados_formatados.reset_index(drop=True), use_container_width=True)

            # Opcional: Gráfico com os 10 maiores valores
            st.subheader("Top 10 Maiores Valores")
            top_10 = resultados.head(10).sort_values(by='Valor_HM', ascending=True)
            if not top_10.empty:
                st.bar_chart(top_10.set_index('Convenio')['Valor_HM'])
        else:
            st.warning("Nenhum resultado encontrado para o termo buscado.")

# Rodapé
st.markdown("---")
st.markdown("Desenvolvido para si pelo seu Parceiro de Programação.")