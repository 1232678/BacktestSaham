import streamlit as st
import pandas as pd
import duckdb

# Running Streamlit as Python Module -> python3 -m streamlit run main.py

conn = duckdb.connect()
df = conn.execute("""
    SELECT *
    FROM 'TOP10000.csv'
""").df()
pd.set_option("styler.render.max_elements", 4393590)


# Streamlit layout
st.set_page_config(page_title="Backtest Saham", layout="wide", initial_sidebar_state="expanded", )


st.title('Backtest Saham Indonesia🔥📈')
st.markdown(
    """
    Selamat datang di platform BacktestSaham! 🎉📊
Website ini dirancang khusus untuk membantu kamu mengevaluasi performa berbagai indikator teknikal terhadap saham-saham Indonesia selama 10 tahun terakhir. Dengan dashboard interaktif ini, kamu dapat mengeksplorasi, menyaring (filter), dan mengurutkan hasil backtest berdasarkan berbagai metrik seperti Sharpe Ratio, Max Drawdown, Win Rate, Profit Factor, dan banyak lagi. Tersedia juga preset filter seperti “Long Term” untuk mempercepat proses pencarian strategi yang sesuai. Hasil dari 50.000 simulasi backtest akan membantumu menemukan parameter terbaik yang paling sesuai dengan gaya trading dan toleransi risiko kamu.
    """
)


# Sidebar for filters
with st.sidebar.form("form_key"):

    st.header("Filters")
    col1, col2 = st.columns(2)
    with col1:
        cci = st.checkbox("CCI", value=True)
        macd = st.checkbox("MACD", value=True)
        dsma = st.checkbox("D_SMA", value=True)

    with col2:
        sto = st.checkbox("STO", value=True)
        rsi = st.checkbox("RSI", value=True)

    pre_defined_filters = {
    "No Filter": {
        "return_range": (0, 200),
        "returnAnn_range": (0, 10),
        "sharpe_range": (0.0, 1.0),
        "drawdown_range": (-70, 0),
        "trades_range": (0, 300),
        "win_rate_range": (0, 90),
        "profit_factor_range": (0, 2000),
        "avg_trade_range": (0, 50),
    },
    "Short Term": {
        "return_range": (51, 200),
        "returnAnn_range": (2, 10),
        "sharpe_range": (0.2, 1.0),
        "drawdown_range": (-50, 0),
        "trades_range": (150, 300),
        "win_rate_range": (50, 90),
        "profit_factor_range": (0, 2000),
        "avg_trade_range": (0, 50),
    },
    "Long Term": {
        "return_range": (100, 200),
        "returnAnn_range": (3, 10),
        "sharpe_range": (0.3, 1.0),
        "drawdown_range": (-70, 0),
        "trades_range": (0, 120),
        "win_rate_range": (60, 90),
        "profit_factor_range": (300, 2000),
        "avg_trade_range": (25, 50),
    },
    }

    selected_filter = st.selectbox(
        "Select Preset Filters",
        options=pre_defined_filters.keys(),
        help="Choose a pre-defined filter or start with no filter."
    )

    filters = pre_defined_filters[selected_filter]

    trades_range = st.slider(
        "**Total Trades**",
        min_value=0,
        max_value=300,
        value=filters['trades_range'],
        step=10,
    )

    drawdown_range = st.slider(
        "**Max Drawdown [%]**",
        min_value=-70,
        max_value=0,
        value=filters['drawdown_range'],
        step=1,
    )

    win_rate_range = st.slider(
        "**Win Rate [%]**",
        min_value=0,
        max_value=90,
        value=filters['win_rate_range'],
        step=1,
    )

    return_range = st.slider(
        "**Return [%]**",
        min_value=0,
        max_value=200,
        value=filters['return_range'],
        step=1,
    )

    sharpe_range = st.slider(
        "**Sharpe Ratio**",
        min_value=0.0,
        max_value=1.0,
        value=filters['sharpe_range'],
        step=0.01,
    )

    profit_factor_range = st.slider(
        "**Profit Factor**",
        min_value=0,
        max_value=2000,
        value=filters['profit_factor_range'],
        step=10,
    )

    returnAnn_range = st.slider(
        "**Return Ann [%]**",
        min_value=0,
        max_value=10,
        value=filters['returnAnn_range'],
        step=1,
    )
    avg_trade_range = st.slider(
        "**Avg Trade [%]**",
        min_value=0,
        max_value=50,
        value=filters['avg_trade_range'],
        step=1,
    )

    pressed = st.form_submit_button("Apply Filters")


tab1, tab2 = st.tabs(["Backtest", "Laporan"])

with tab1:
    if pressed == False:
        filtered_df = pd.DataFrame()
        st.subheader("Hasil Backtest")
        st.write("Menampilkan 50000 backtest dari 50000 backtest")
        df.reset_index(drop=True, inplace=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
        "*hanya menampilkan 10.000 data teratas dari setiap indikator diurutkan berdasarkan Sharpe Ratio"
    if pressed: 
        selected_indicators = []
        if cci:
            selected_indicators.append("CCI")
        if rsi:
            selected_indicators.append("RSI")
        if macd:
            selected_indicators.append("MACD")
        if sto:
            selected_indicators.append("STO")
        if dsma:
            selected_indicators.append("SMACross")


        if len(selected_indicators) > 0:
            indicator_condition = f"REGEXP_MATCHES(\"Indicator Settings\", '{'|'.join(selected_indicators)}', 'i')"
        else:
            indicator_condition = "TRUE"  # Match all rows if no indicators are selected
        query = f""" 
        SELECT * 
        FROM df 
        WHERE 
            "Return [%]" BETWEEN {return_range[0]} AND {return_range[1]} AND
            "Return Ann [%]" BETWEEN {returnAnn_range[0]} AND {returnAnn_range[1]} AND
            "Sharpe Ratio" BETWEEN {sharpe_range[0]} AND {sharpe_range[1]} AND
            "Max Drawdown [%]" BETWEEN {drawdown_range[0]} AND {drawdown_range[1]} AND
            "Total Trades" BETWEEN {trades_range[0]} AND {trades_range[1]} AND
            "Win Rate [%]" BETWEEN {win_rate_range[0]} AND {win_rate_range[1]} AND
            "Profit Factor" BETWEEN {profit_factor_range[0]} AND {profit_factor_range[1]} AND
            "Avg Trade [%]" BETWEEN {avg_trade_range[0]} AND {avg_trade_range[1]} AND
            {indicator_condition}
        """
        filtered_df = duckdb.sql(query).df()


        st.subheader("Hasil Filter Backtest")
        st.write(f"Menampilkan {len(filtered_df)} backtest dari 50000 backtest")
        filtered_df.reset_index(drop=True, inplace=True)
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        "*hanya menampilkan 10.000 data teratas dari setiap indikator diurutkan berdasarkan Sharpe Ratio"

with tab2:
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        '''# Laporan Backtest

    '''
    st.write(f'''
        <a target="_blank" href="https://youtube.com">
            <button style='
                background-color: #FFFFFF;
                border: 1px solid #3E4451;
                border-radius: 8px;
                padding: 10px 20px;
                color: black;
                font-weight: bold;
                text-align: center;
                cursor: pointer;
            ' >
                DOWNLOAD VERSI LENGKAP BACKTEST
            </button>
        </a>
        ''',
        unsafe_allow_html=True
    )