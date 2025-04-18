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
st.set_page_config(page_title="Backtest Saham", layout="wide", initial_sidebar_state="expanded")


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
        dsma = st.checkbox("SMACross", value=True)

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


final_result = [
    # Total Trades
    {
        'Indicator': ['RSI', 'CCI', 'STO', 'SMACross', 'MACD'],
        'Total Trades': ['266', '211', '165', '101', '48']
    },
    # Max Drawdown
    {
        'Indicator': ['RSI', 'SMACross', 'CCI', 'STO', 'MACD'],
        'Max Drawdown': ['-2.29', '-2.86', '-3.31', '-5.03', '-7.81']
    },
    # Win Rate
    {
        'Indicator': ['STO', 'MACD', 'CCI', 'RSI', 'SMACross'],
        'Win Rate': ['85%', '78%', '77%', '76%', '59%']
    },
    # Return
    {
        'Indicator': ['STO', 'RSI', 'CCI', 'MACD', 'SMACross'],
        'Return': ['155%', '121%', '107%', '16%', '6%']
    },
    # Profit Factor
    {
        'Indicator': ['STO', 'RSI', 'CCI', 'MACD', 'SMACross'],
        'Return': ['1813', '695', '299', '124', '66']
    },
    # Sharpe Ratio
    {
        'Indicator': ['STO', 'RSI', 'MACD', 'CCI', 'SMACross'],
        'Sharpe Ratio': ['0.5', '0.37', '0.36', '0.34', '0.33']
    }
]
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

        Daftar Isi
        1) Pendahuluan: Mengapa Backtest Penting?
        2) Metodologi Backtest
        3) Curve-Fitting(Win rate 100%)
        4) Metriks Backtest
        5) Cara Memilih Indikator yang tepat untuk Anda!
        6) Kesimpulan & Rekomendasi (link download backtest lengkap)
        7) Cara Memasukan Indikator ke TradingView
        8) Proses Pembuatan Backtest & Terima Kasih
### 1. Pendahuluan: Mengapa Backtest Penting?

Laporan ini sepenuhnya berdasarkan teknikal analisis untuk mempelajari performa indikator teknikal. Sebagai trader, sering kali kita menggunakan indikator dengan pengaturan standar tanpa mengetahui apakah pengaturan tersebut memberikan hasil terbaik. Dengan melakukan backtest, kita dapat menguji indikator terhadap data historis saham untuk memahami performa dan sifatnya secara mendalam. 

Perlu saya tegaskan bahwa tujuan melakukan backtest bukan untuk mencari 1 indikator yang terbaik dari semuanya, melainkan untuk menemukan indikator yang paling sesuai dengan gaya trading, toleransi risiko, serta preferensi kita masing-masing trader.

Banyak orang mengalami kesalahpahaman tentang penggunaan indikator teknikal. Mayoritas trader hanya menggunakan indikator teknikal dengan parameter atau pengaturan yang umum digunakan. Sebagai contoh, Relative Strength Index (RSI) dengan parameter standar seperti 7, 30, 70, atau Moving Average Convergence Divergence (MACD) dengan parameter 12, 26, 9 merupakan indikator yang paling banyak digunakan oleh trader pemula. Akan tetapi, indikator dengan parameter standar tersebut belum tentu memiliki kinerja optimal.

Oleh sebab itu, diperlukan backtest atau pengujian kinerja indikator teknikal terhadap data saham historis untuk mengetahui performa dan keunggulan masing-masing indikator. Dengan mengacu pada hasil backtest, kita bisa memahami karakteristik indikator secara lebih mendalam. Misalnya, apakah Anda tahu bahwa parameter RSI dapat dimodifikasi agar menghasilkan jumlah sinyal trading yang lebih sedikit? Tahukah Anda bahwa mengurangi jumlah sinyal trading (Total Trades) dapat meningkatkan probabilitas keuntungan? Informasi semacam ini hanya bisa diperoleh melalui analisis statistik indikator tersebut dalam proses backtest. 

Sebagai analogi, proses ini mirip dengan saat kita ingin membeli mobil untuk kendaraan pribadi. Mungkin sebagian dari kita lebih memilih mobil dengan kapasitas mesin (cc) besar karena memiliki kelebihan seperti bodi mobil yang besar sehingga bisa menampung lebih banyak penumpang serta memberikan performa mesin yang lebih cepat dan kuat, meskipun memiliki kelemahan yaitu konsumsi bahan bakar yang sangat boros. Namun ada juga sebagian orang yang lebih memilih mobil dengan kapasitas mesin (cc) kecil karena lebih hemat bahan bakar, meskipun memiliki kelemahan yaitu bodi mobil yang lebih kecil dan kapasitas penumpang yang terbatas. Oleh karena itu, melalui pengujian dan perbandingan performa, kita bisa menentukan mobil mana yang paling sesuai dengan kebutuhan dan preferensi masing-masing.

Semoga dari laporan backtest ini dapat menjadi landasan dalam memilih indikator teknikal saham yang paling cocok dengan gaya trading dan preferensi kita masing-masing.



### 2. Metodologi Backtest
Data historis yang digunakan dalam backtest ini mencakup periode selama 10 tahun, mulai Januari 2012 hingga Desember 2022. Periode ini dipilih karena mencakup berbagai kondisi pasar, baik bullish maupun bearish, sehingga performa dan kualitas indikator teknikal dapat diuji secara menyeluruh. Biaya transaksi dalam laporan ini diabaikan karena nilainya relatif sangat kecil sehingga tidak memberikan dampak signifikan terhadap hasil akhir backtest. 

Indeks IDX Composite digunakan sebagai tolok ukur utama atau benchmark untuk membandingkan kinerja semua indikator teknikal yang diuji. Perbandingan dilakukan terhadap pergerakan indeks selama periode 10 tahun, yaitu dari Januari 2012 hingga Desember 2022, untuk memastikan evaluasi performa yang relevan dan mencerminkan berbagai kondisi pasar di Indonesia.

Dalam laporan ini, digunakan 15 saham yaitu ADRO, AKRA, ASII, BBCA, BBRI, BBNI, BMRI, INCO, INDF, ITMG, MAPI, MEDC, PTBA, TLKM, dan UNTR. Mayoritas saham tersebut dipilih dari indeks LQ45 karena memiliki likuiditas tinggi dan fundamental yang kuat. Saham-saham "gorengan" sengaja dihindari karena fluktuasi harganya yang tidak stabil dapat mengganggu sinyal indikator dan membuat hasil backtest kurang kredibel. Penting ditekankan bahwa backtest ini tidak dirancang untuk day trading karena data yang digunakan adalah data historis harian (daily) dengan harga penutupan (closing price). Pertimbangan ini diambil karena kebanyakan trader retail tidak memiliki waktu untuk memantau pasar sepanjang hari, mengingat kesibukan lain seperti bekerja, kuliah, atau sekolah. Oleh karena itu, dalam laporan ini hanya dilakukan maksimal 1 order per saham per hari. 

Jumlah backtest secara keseluruhan(seluruh variasi indikator) yang diuji dalam laporan ini mencapai kurang lebih 447562 simulasi. Indikator yang tidak menghasilkan sinyal trading sama sekali secara otomatis tidak disertakan dalam laporan akhir. Buy and Sell Signal Setiap backtest menggunakan modal awal sebesar Rp100.000.000 dengan alokasi modal per transaksi sebesar 5% dari total modal. Jika modal yang tersisa tidak mencukupi untuk melakukan transaksi, maka transaksi tersebut tidak dieksekusi. Jika trade tidak pernah ditutup(close) sampai akhir periode backtest maka akan otomatis terjual. Backtest ini tidak menerapkan position sizing maupun stop loss.

Dalam menentukan indikator yang diuji, saya memilih 5 indikator teknikal yang cukup populer di kalangan trader retail khususnya di Indonesia. Kelima indikator ini banyak dibahas dan direkomendasikan oleh artikel-artikel investasi maupun influencer investasi di YouTube. Indikator yang diuji adalah Commodity Channel Index (CCI), Moving Average Convergence Divergence (MACD), Double Simple Moving Average (Double SMA), Relative Strength Index (RSI), dan Full Stochastic Oscillator (STO). Sebagai catatan, kelima indikator ini hanya menggunakan data harga saham untuk menghasilkan sinyal buy/sell, tanpa menggunakan data volume.


### 3. Curve-Fitting (win rate 100%)
Seperti yang sudah kita ketahui tidak ada indikator saham yang sempurna(memiliki win rate 100% ). Setiap indikator pasti memiliki kelebihan dan kekurangannya maupun itu total trades besar dengan win rate yang kecil atau total trades yang kecil tetapi win rate yang besar. Semua memiliki kelebihan dan kekurangannya masing-masing. Walaupun itu pada backtest yang saya lakukan, saya menemukan beberapa kasus dimana indikator mempunyai win rate 100%. Hal ini seperti yang telah dijelaskan pada bab pendahuluan merupakan hasil dari Curve-Fitting. 

Curve-fitting atau “menyesuaikan kurva” adalah kondisi di mana strategi atau indikator terlalu diatur agar terlihat sangat cocok dengan data historis(data yang digunakan untuk backtest), padahal pada kenyataannya sama sekali tidak efektif kalau digunakan di kondisi pasar yang sebenarnya. Tujuan backtest adalah memahami karakter indikator secara realistis, bukan membuat strategi yang hanya bagus di masa lalu tapi gagal di masa depan.

Pada backtest ini, semua kasus dimana parameter memiliki win rate 100% (curve-fitting) telah disaring dan tidak dimasukkan ke dalam laporan akhir karena dianggap tidak mewakili performa yang realistis di kondisi pasar sesungguhnya.

### 4. Metriks Backtest
Berikut penjelasan masing-masing metrik yang digunakan dalam backtest ini:

- Equity Final (Rp): Total nilai modal akhir setelah periode backtest selesai.
- Return (%): Persentase keuntungan atau kerugian terhadap modal awal.
- Return Ann (%): Persentase keuntungan atau kerugian terhadap modal pertahunnya.
- Sharpe Ratio: Mengukur tingkat keuntungan dibandingkan risiko total. 
- Sortino Ratio: Mengukur tingkat keuntungan dibandingkan risiko downside (risiko kerugian saja). 
- Calmar Ratio: Mengukur tingkat keuntungan dibandingkan dengan risiko maksimum penurunan (max drawdown). 
- Max Drawdown (%): Penurunan maksimum nilai portofolio dari titik tertinggi ke titik terendah selama periode backtest.
- Max Drawdown Duration: Lama waktu yang dibutuhkan portofolio untuk pulih dari kondisi drawdown terbesar hingga mencapai nilai sebelumnya.
- Total Trades: Jumlah total transaksi yang dieksekusi selama periode backtest.
- Win Rate (%): Persentase transaksi yang menghasilkan keuntungan dibanding total transaksi.
- Profit Factor: Rasio total keuntungan dari transaksi yang untung terhadap total kerugian dari transaksi yang rugi.
- Avg Trade (%): Persentase rata-rata keuntungan atau kerugian per transaksi.
- Best Trade (%): Keuntungan terbesar dalam satu transaksi selama periode backtest.
- Worst Trade (%): Kerugian terbesar dalam satu transaksi selama periode backtest.

Sharpe Ratio merupakan salah satu metrik penting yang perlu diperhatikan dalam menilai performa sebuah indikator. Sebuah indikator dapat dianggap cukup baik apabila nilai Sharpe Ratio-nya lebih tinggi dari Sharpe Ratio indeks IDX Composite selama periode 2012 hingga 2022, yaitu sebesar 0,31(bisa dilihat dibawah). Sharpe Ratio juga merupakan rasio backtest yang paling umum digunakan dibandingkan Sortino Ratio dan Calmar Ratio, karena perhitungannya mencakup return dan volatilitas (bukan max drawdown seperti yang tertulis sebelumnya), yang mewakili keseluruhan fluktuasi risiko. Sementara itu, Sortino dan Calmar Ratio lebih fokus pada sisi negatif dari risiko, seperti penurunan nilai atau kerugian (downside risk).

Secara sederhana, Sharpe Ratio dapat diartikan sebagai CAGR (Compound Annual Growth Rate — yaitu tingkat pertumbuhan tahunan majemuk, yang berbeda dari annual return biasa) dibagi dengan volatilitas. Mengapa volatilitas dapat dianggap serupa dengan risiko seperti drawdown? Karena volatilitas umumnya meningkat saat pasar mengalami penurunan tajam akibat panic selling, dan cenderung menurun ketika pasar sedang berada dalam tren naik yang stabil. Oleh karena itu, jika kita mengurutkan hasil backtest berdasarkan nilai Sharpe Ratio, kita akan melihat bahwa semakin tinggi posisinya, umumnya berarti return yang tinggi disertai drawdown yang lebih kecil. Sebaliknya, indikator dengan nilai Sharpe Ratio yang rendah cenderung memiliki return yang kecil dan risiko drawdown yang besar.

Dengan menggunakan 14 metrik backtest yang tersedia, laporan ini memberikan gambaran menyeluruh mengenai kelebihan dan kekurangan dari masing-masing indikator, sehingga trader dapat memilih indikator yang paling sesuai dengan gaya dan kebutuhan trading mereka.


### 5. Cara Memilih Indikator yang tepat untuk Anda!
Seperti yang dapat dilihat pada bagian filter presets di menu Filters, terdapat dua pilihan utama, yaitu Short Term dan Long Term. Short Term ditujukan bagi trader yang lebih menyukai bertransaksi dalam jangka pendek, seperti harian hingga mingguan. Sementara itu, Long Term ditujukan bagi trader yang memiliki gaya transaksi jangka panjang, mulai dari bulanan hingga tahunan. Dari sini kita bisa menyimpulkan bahwa indikator yang “terbaik” bukanlah yang memberikan return tertinggi, melainkan yang paling sesuai dengan gaya trading masing-masing, apakah itu jangka pendek atau panjang.

Lalu, bagaimana cara kita mengetahui apakah sebuah indikator termasuk kategori short-term atau long-term? Salah satu cara termudah adalah dengan melihat jumlah total trades (jumlah transaksi) yang dihasilkan oleh indikator tersebut. Indikator yang termasuk long-term cenderung memiliki total trades yang kecil karena sinyal beli/jual yang dihasilkan lebih jarang. Sebaliknya, indikator short-term akan menghasilkan total trades yang lebih banyak karena lebih sering memberi sinyal transaksi.

Pada indikator long-term, karena frekuensi sinyalnya rendah, saham yang dibeli biasanya ditahan dalam jangka waktu yang lebih lama. Hal ini menyebabkan nilai max drawdown (kerugian maksimum) menjadi lebih besar. Namun, dengan total trades yang lebih sedikit dan waktu penahanan yang lebih lama, peluang untuk memperoleh keuntungan juga meningkat karena secara historis, harga saham cenderung naik dalam jangka panjang. Inilah yang menyebabkan indikator long-term cenderung memiliki win rate dan return yang lebih tinggi.

Sementara itu, pada indikator short-term yang lebih sering memberi sinyal beli/jual, posisi saham biasanya tidak ditahan terlalu lama. Hal ini membuat nilai max drawdown menjadi lebih kecil. Akan tetapi, karena saham dijual lebih cepat, kemungkinan untuk mencapai titik keuntungan maksimal pun berkurang, sehingga win rate dan return dari indikator short-term cenderung lebih kecil.

##### Sebagai kesimpulan:
- Indikator long-term memiliki total trades kecil, max drawdown besar, win rate tinggi, dan return tinggi.

- Indikator short-term memiliki total trades besar, max drawdown kecil, win rate rendah, dan return yang lebih rendah.

Mungkin sebagian dari Anda bertanya, “Kalau begitu, kenapa kita tidak langsung saja menggunakan indikator long-term yang punya return paling besar?” Jawabannya adalah: indikator long-term memang memiliki potensi return yang lebih tinggi, tetapi juga disertai dengan risiko drawdown yang lebih besar. Pertanyaannya sekarang, apakah Anda sanggup menahan kerugian hingga -10% sampai -20%? Jika tidak, mungkin Anda perlu mempertimbangkan ulang.

Seperti yang telah dijelaskan sebelumnya, setiap jenis indikator — baik long-term maupun short-term — memiliki kelebihan dan kekurangannya masing-masing. Tidak ada indikator yang sempurna. Prinsip ini selaras dengan hukum alam: kita tidak bisa mendapatkan segalanya. Jika suatu strategi memberikan keuntungan tinggi, biasanya risiko yang ditanggung juga tinggi. Sebaliknya, jika kita ingin mengurangi risiko, maka imbal hasil yang diperoleh pun akan ikut menurun. Dengan kata lain, semuanya kembali pada prinsip keseimbangan dan keadilan — high return selalu datang bersama high risk.

### 6. Kesimpulan & Rekomendasi
'''
        col1, col2 = st.columns([3, 1])
        with col1: 
            "##### Benchmark COMPOSITE 2012-2022"
            st.image('images/benchmark.png')
        with col2: 
            st.image('images/composite_stats.png')
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1: 
            "##### Total Trades Rata-Rata"
            st.table(final_result[0]) 
            "##### Maximum Drawdown Terkecil"
            st.table(final_result[1]) 
        with col2:
            "##### Win Rate Tertinggi"
            st.table(final_result[2]) 
            "##### Return Tertinggi"
            st.table(final_result[3]) 
        with col3: 
            "##### Profit Factor Tertinggi"
            st.table(final_result[4]) 
            "##### Sharpe Ratio Tertinggi"
            st.table(final_result[5]) 
        st.write(f'''
            <div style='display: flex; justify-content: center;margin-bottom: 30px;'>
                <a target="_blank" href="https://drive.google.com/file/d/1h41UtWotCXUa7fecAByTH2SjhDgNjS6Q/view?usp=sharing">
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
            </div>
            ''',
            unsafe_allow_html=True
        )
        '''
        Dari hasil backtest yang telah dilakukan, dapat kita lihat bahwa setiap indikator memiliki karakteristik dan kecenderungannya masing-masing. Tiga indikator yang menunjukkan performa cukup baik dan layak dipertimbangkan dalam analisis teknikal adalah Stochastics (155%), RSI (121%), dan CCI (107%), berdasarkan persentase return yang dihasilkan. Ketiganya memberikan hasil yang jauh lebih tinggi dibandingkan dengan MACD dan SMA Cross, yang hanya menghasilkan return sebesar 16% dan 6%. Cukup mengejutkan bahwa indikator SMA Cross atau Double SMA, yang sering digunakan oleh para trader pemula dan biasanya menjadi indikator teknikal pertama yang kita pelajari, ternyata memiliki performa yang kurang optimal dan tidak bisa berdiri sendiri. Meskipun pada dasarnya Double SMA cukup baik untuk mengidentifikasi arah trend pasar, indikator ini sebaiknya dikombinasikan dengan indikator lain seperti RSI atau Stochastics agar menghasilkan sinyal yang lebih akurat dan hasil yang lebih maksimal.

        Selain itu, hasil backtest juga menunjukkan bahwa setiap indikator memiliki kecenderungan tertentu dalam hal jangka waktu penggunaan. Sebagai contoh, indikator Stochastics cenderung lebih cocok digunakan dalam strategi jangka panjang, karena jumlah transaksi (total trades) yang dihasilkan relatif sedikit dibandingkan dengan RSI dan CCI. Karakteristik ini membuat Stochastics menghasilkan return tertinggi, win rate tertinggi, profit factor tertinggi, serta Sharpe ratio tertinggi. Namun, perlu dicatat bahwa indikator ini juga memiliki max drawdown yang paling besar, sebagaimana telah dijelaskan sebelumnya.

        Secara keseluruhan, dari hasil backtest terhadap lima indikator teknikal pada saham-saham Indonesia, dapat disimpulkan bahwa strategi long-term berpotensi memberikan keuntungan yang lebih besar, namun juga menuntut kemampuan untuk menahan risiko yang lebih tinggi. Sebagai rekomendasi, berdasarkan hasil filter dan penyortiran pada website ini, indikator Stochastics 32,8,6 (86,24) terbukti menjadi pilihan terbaik untuk strategi jangka panjang, sedangkan RSI 5,39,91 menjadi pilihan terbaik untuk strategi jangka pendek. Pemilihan kedua indikator ini didasarkan pada data yang tersedia di website ini. Saya sangat merekomendasikan anda untuk mengunduh hasil backtest lengkap untuk mengeksplorasi indikator lain yang mungkin lebih sesuai dengan gaya trading Anda!

        ### 7. Cara memasukan Indikator ke TradingView 
    '''

        col1, col2, col3, col4= st.columns([1, 1, 1, 1])
        with col1: 
            st.image('images/cci.jpeg')
        with col2: 
            st.image('images/macd.jpeg')
        with col3: 
            st.image('images/rsi.jpeg')
        with col4: 
            st.image('images/sto.jpeg')

        '''
        Penting untuk memperhatikan cara menerapkan kelima indikator ini di TradingView dengan benar. Jika tidak dilakukan dengan tepat, maka indikator yang tampil di platform charting tersebut tidak akan sesuai dengan metrik dan performa yang telah dihasilkan dalam backtest, sehingga hasil analisis bisa menjadi tidak akurat.

        Cara menginput parameter indikator dapat dilihat pada screenshot yang tersedia. Tanda panah menunjukkan bahwa input tersebut wajib disesuaikan seperti yang ditunjukkan, sedangkan simbol bintang menandakan bahwa parameter tersebut harus diubah melalui Pine Script.

        Sebagai contoh, pada indikator MACD, jika parameter yang digunakan terlalu besar hingga melebihi batas maksimum input di TradingView, maka batas maksimum tersebut (max value) dapat disesuaikan secara manual melalui pengeditan kode indikator menggunakan Pine Script.

        Untuk indikator Stochastics, perlu dilakukan penggantian garis %K dan %D dari SMA (Simple Moving Average) menjadi EMA (Exponential Moving Average), karena itulah yang digunakan pada saat proses backtest. Namun, indikator Stochastics bawaan di TradingView tidak menyediakan opsi untuk mengganti jenis moving average tersebut secara langsung. Oleh karena itu, kita perlu memodifikasi kode indikatornya sendiri menggunakan Pine Script agar hasilnya sesuai dengan pengujian yang dilakukan.

        Cara memasukkan parameter telah ditunjukkan pada screenshot. Untuk input lainnya yang tidak memerlukan modifikasi khusus, Anda dapat mengisi parameter indikator seperti biasa melalui menu pengaturan indikator di TradingView.

        ### 8. Proses Pembuatan Backtest & Terima Kasih 

        Proses pembuatan backtest ini tentu tidak mudah, terutama dengan jadwal sekolah yang sangat padat, ditambah puluhan jam yang saya habiskan untuk melakukan backtest serta berbagai kendala dan error yang saya hadapi. Salah satu tantangan terbesar dalam membuat backtest ini adalah ketika saya keliru menentukan interval parameter untuk indikator CCI yang akan diuji. Pada awalnya, saya belum mengetahui seberapa rapat interval parameter yang sebaiknya digunakan. Jika intervalnya terlalu sempit, ada kemungkinan beberapa parameter potensial yang sebenarnya menghasilkan performa baik justru terlewat. Namun, jika intervalnya terlalu lebar, proses backtest menjadi sangat lama — bahkan bisa memakan waktu hingga 20 jam!

        Meskipun penuh tantangan, saya justru memperoleh banyak pelajaran dari proyek ini. Dengan minat saya di bidang trading dan juga programming, saya merasa sangat antusias dan penasaran saat mengerjakan backtest ini. Saya juga belajar banyak tentang konsep backtesting dan penerapan data science dengan Python.

        Bagi teman-teman programmer yang ingin tahu lebih lanjut, backtest ini dibuat menggunakan bahasa pemrograman Python dengan Backtrader.py sebagai mesin backtesting, serta TA-Lib sebagai library utama untuk berbagai indikator teknikal. Selain itu, saya juga menggunakan library umum dalam data science seperti pandas, numpy, dan duckdb untuk mengolah data dalam format CSV. Website yang sedang Anda lihat saat ini dibangun dan di-host menggunakan Streamlit.py, yang juga berbasis Python. Karena website ini di-host melalui Streamlit tanpa server backend khusus, terdapat keterbatasan performa yang mengharuskan saya untuk hanya menampilkan 50.000 hasil backtest dari total keseluruhan sebanyak 447.562 backtest.

        Sebagai penutup, saya ucapkan terima kasih sebesar-besarnya kepada Anda yang telah membaca sampai akhir! Saya menyadari bahwa laporan ini mungkin terasa cukup panjang — bahkan ini adalah esai terpanjang yang pernah saya tulis sepanjang hidup saya. Namun, tujuan saya hanyalah ingin memberikan laporan yang sekomprehensif dan selengkap mungkin, agar dapat benar-benar membantu kita semua dalam memahami dan mengevaluasi indikator teknikal secara lebih mendalam. Semoga hasil backtest ini dapat membantu kita semua dalam mengembangkan kemampuan trading dan tentunya — meningkatkan cuan! 🚀📈

        '''
    