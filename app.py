import asyncio

import pandas as pd
import streamlit as st

from scrapers.kabum import scrape_kabum

st.set_page_config(page_title="Price Tracker", page_icon="💰", layout="wide")

st.title("💰 Price Tracker")
st.caption("Kabum")

produto = st.text_input(
    "Buscar produto", placeholder="ex: rtx 4060, iphone 15, notebook..."
)

if st.button("Buscar") and produto:
    with st.spinner("Buscando no Kabum..."):
        df = asyncio.run(scrape_kabum(produto))

    df = df.sort_values("price").reset_index(drop=True)

    col1, col2 = st.columns(2)
    col1.metric("Resultados encontrados", len(df))
    col2.metric("Menor preço", f"R$ {df['price'].min():,.2f}")

    st.divider()
    st.subheader("Resultados")

    st.dataframe(
        df[["title", "price", "Store", "link"]],
        column_config={
            "title": "Produto",
            "price": st.column_config.NumberColumn("Preço", format="R$ %.2f"),
            "Store": "Loja",
            "link": st.column_config.LinkColumn("Link"),
        },
        width="stretch",
        hide_index=True,
    )

    st.divider()
    st.subheader("Distribuição de preços")
    st.bar_chart(df.set_index("title")["price"].head(10))
