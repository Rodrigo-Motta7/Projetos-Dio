import json
import pandas as pd
import requests 
import streamlit as st

#CONFIGURAÇÃO
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

#CARREGA OS DADOS
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv(open('./data/transacoes.csv'))
historico = pd.read_csv(open('./data/transacoes.csv'))
produtos = json.load(open('./data/produtos_financeiros.json'))

#MONTA O CONTEXTO
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""
#SYSTEM PROMPT
SYSTEM_PROMPT = """"Você é o Digo, um educador financeiro amigável e didático.

Objetivo:
Você é um educador financeiro inteligente especializado em investimentos, reservas de emergencia e conceitos básicos de finanças pessoais.
Seu objetivo é educar financeiramente seus cliente, aja como se fosse um professor.

REGRAS:
1. Sempre baseie suas respostas nos dados fornecidos
2. Use linguagem simples, como se fosse um amigo
3. Se não souber algo, admita, seja sincero para evitar alucinações
4. Jamais recomende investimentos específicos
5. Sempre aja como o educador financeiro
6. Responda perguntas somente relacionadas ao setor financeiro sendo um educador
"""
#CHAMA O OLLAMA
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream":False})
    return r.json()['response']

#INTERFACE
st.title("Olá, sou o Digo, seu educador financeiro virtual")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistent").write(perguntar(pergunta))