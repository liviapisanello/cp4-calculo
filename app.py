
import pandas as pd
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.set_page_config(
    page_title="Análise de Desempenho da API",
    page_icon="⚡",
    layout="wide"
)

# a) Título, descrição do problema e identificação das variáveis
st.title("⚡ Simulação e Análise de Desempenho da API")
st.markdown("---")

st.markdown("""
### Contexto do Problema
Esta aplicação utiliza um modelo matemático para prever o tempo médio de resposta de uma API sob diferentes níveis de carga.
Conforme a taxa de requisições aumenta e se aproxima da capacidade máxima de processamento da infraestrutura (50 req/s),
o tempo de resposta cresce assintoticamente, podendo comprometer a operação e violar os acordos de nível de serviço (SLA).

**Variáveis do Modelo:**
* **Variável Independente ($x$):** Quantidade de requisições por segundo (unidade: `req/s`).
* **Variável Dependente ($f(x)$):** Tempo médio de resposta da API (unidade: `ms`).
* **Função do Modelo:** $f(x) = \\frac{1000}{50 - x}$.
""")

st.sidebar.header("⚙️ Painel de Controle de Carga")

# b) Controle interativo para informar a quantidade de requisições por segundo
carga = st.sidebar.slider(
    "Selecione a carga de requisições (req/s):",
    min_value=0.0,
    max_value=49.9,
    value=30.0,
    step=0.1,
    help="Escolha um valor dentro do domínio operacional seguro (0 a 49.9 req/s)."
)

# c) Cálculo do tempo de resposta previsto
if carga < 50:
    tempo_resposta = 1000 / (50 - carga)
else:
    tempo_resposta = float('inf')

st.subheader("📊 Diagnóstico da Operação")
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Carga Selecionada",
        value=f"{carga:.1f} req/s"
    )

with col2:
    if tempo_resposta != float('inf'):
        st.metric(
            label="Tempo de Resposta Previsto",
            value=f"{tempo_resposta:.2f} ms",
            delta=f"{(tempo_resposta - 20):.2f} ms acima da latência base"
        )
    else:
        st.metric(
            label="Tempo de Resposta Previsto",
            value="∞ ms (Saturação Total)"
        )

# f) Apresentação de referência de desempenho (SLA de Latência)
SLA_LIMITE_MS = 200.0

st.markdown("---")
# e) Indicação visual / mensagem de alerta referente à região crítica e SLA
if carga >= 45.0:
    st.error(f"🔴 **CRÍTICO - FORA DO SLA DE OPERAÇÃO!** Tempo de resposta de **{tempo_resposta:.2f} ms** excede significativamente o limite seguro de SLA ({SLA_LIMITE_MS} ms). Risco iminente de timeout e indisponibilidade do sistema.")
elif carga >= 40.0:
    st.warning(f"⚠️ **ATENÇÃO - REGIÃO CRÍTICA!** Carga no limiar de saturação ({carga:.1f} req/s). Tempo de resposta ({tempo_resposta:.2f} ms) aproxima-se do limite tolerável de SLA ({SLA_LIMITE_MS} ms).")
else:
    st.success(f"✅ **OPERAÇÃO NORMAL - DENTRO DO SLA.** O tempo de resposta ({tempo_resposta:.2f} ms) está abaixo da meta aceitável ({SLA_LIMITE_MS} ms).")

# d) Gráfico da função contendo a carga selecionada, a região crítica e a assíntota
x_vals = np.linspace(0, 49.8, 500)
y_vals = 1000 / (50 - x_vals)

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(x_vals, y_vals, label=r"$f(x) = \frac{1000}{50-x}$", color="blue", linewidth=2)
ax.scatter([carga], [tempo_resposta], color="red", s=100, zorder=5, label=f"Carga Selecionada: {carga:.1f} req/s ({tempo_resposta:.1f} ms)")
ax.axhline(y=SLA_LIMITE_MS, color="green", linestyle="--", linewidth=1.5, label=f"Meta SLA de Latência ({SLA_LIMITE_MS} ms)")
ax.axvspan(40, 50, color="orange", alpha=0.2, label="Região Crítica (Risco de Saturação)")
ax.axvline(x=50, color="red", linestyle=":", linewidth=2, label="Assíntota Vertical: Saturação (x = 50 req/s)")
ax.set_title("Comportamento do Tempo de Resposta vs. Carga de Requisições", fontsize=12)
ax.set_xlabel("Requisições por Segundo (req/s)", fontsize=10)
ax.set_ylabel("Tempo Médio de Resposta (ms)", fontsize=10)
ax.set_ylim(0, 600)
ax.set_xlim(0, 52)
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend(loc="upper left")

st.pyplot(fig)
