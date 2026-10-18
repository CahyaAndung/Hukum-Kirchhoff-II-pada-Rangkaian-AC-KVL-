
import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# 1. KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="Simulasi Hukum Kirchhoff II (KVL)",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY = "#17365D"
BLUE = "#3678B8"
TEAL = "#168A85"
ORANGE = "#E59B3B"
MUTED = "#667085"
BORDER = "#E4E9F0"
LIGHT = "#F5F8FC"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: #FFFFFF;
        color: #182230;
    }}
    .block-container {{
        max-width: 1240px;
        padding-top: 1.7rem;
        padding-bottom: 3rem;
    }}
    [data-testid="stSidebar"] {{
        background: #F5F8FC;
        border-right: 1px solid {BORDER};
    }}
    .hero {{
        background: linear-gradient(120deg, #F2F6FC, #FFFFFF);
        border: 1px solid {BORDER};
        border-radius: 17px;
        padding: 28px;
        margin-bottom: 22px;
    }}
    .eyebrow {{
        color: {BLUE};
        font-size: .76rem;
        font-weight: 750;
        letter-spacing: 1.5px;
        margin-bottom: 10px;
    }}
    .hero-title {{
        color: {NAVY};
        font-size: clamp(1.7rem, 3.5vw, 2.55rem);
        line-height: 1.2;
        font-weight: 800;
        margin-bottom: 12px;
    }}
    .hero-subtitle {{
        color: #536276;
        font-size: 1rem;
        line-height: 1.8;
        max-width: 900px;
    }}
    .section-heading {{
        color: {NAVY};
        font-size: 1.3rem;
        font-weight: 750;
        margin-top: 1.5rem;
        margin-bottom: .3rem;
    }}
    .section-desc {{
        color: {MUTED};
        font-size: .9rem;
        line-height: 1.7;
        margin-bottom: 1rem;
    }}
    .metric-box {{
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 15px;
        background: white;
        min-height: 112px;
    }}
    .metric-label {{
        color: {MUTED};
        font-size: .82rem;
        margin-bottom: 8px;
    }}
    .metric-value {{
        color: {NAVY};
        font-size: 1.38rem;
        font-weight: 780;
        overflow-wrap: anywhere;
    }}
    .metric-foot {{
        color: {MUTED};
        font-size: .77rem;
        margin-top: 7px;
        line-height: 1.4;
    }}
    .info-box {{
        background: {LIGHT};
        border: 1px solid {BORDER};
        border-left: 4px solid {BLUE};
        border-radius: 9px;
        padding: 13px 16px;
        line-height: 1.8;
        color: #344054;
        margin: 10px 0 16px;
    }}
    .footer {{
        color: {MUTED};
        text-align: center;
        font-size: .82rem;
        line-height: 1.8;
        padding: 12px 0;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


def section(title, description=""):
    st.markdown(
        f'<div class="section-heading">{title}</div>',
        unsafe_allow_html=True,
    )
    if description:
        st.markdown(
            f'<div class="section-desc">{description}</div>',
            unsafe_allow_html=True,
        )


def metric_card(label, value, foot=""):
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-foot">{foot}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_chart(fig, height=360):
    fig.update_layout(
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Arial", color="#344054", size=12),
        margin=dict(l=15, r=20, t=30, b=20),
        hoverlabel=dict(bgcolor="white"),
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="#EDF1F6",
        zerolinecolor="#D8E0EA",
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#EDF1F6",
        zerolinecolor="#D8E0EA",
    )
    return fig


# =========================================================
# 2. JUDUL DAN SUBJUDUL
# =========================================================
st.markdown(
    """
    <div class="hero">
     <div class="hero-title">
            Simulasi Hukum Kirchhoff II pada Rangkaian AC (KVL)
        </div>
        <div class="hero-subtitle">
            Simulasi interaktif rangkaian RLC seri arus bolak-balik
            untuk mempelajari hubungan tegangan, arus, impedansi,
            dan sudut fase. Ubah parameter komponen, amati perubahan
            karakteristik rangkaian, dan verifikasi Hukum Kirchhoff II
            melalui perhitungan serta visualisasi.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 3. PARAMETER RANGKAIAN
# =========================================================
with st.sidebar:
    st.markdown("## ⚙️ Parameter Rangkaian")
    st.caption("Sesuaikan nilai berikut untuk menjalankan simulasi.")

    V = st.slider(
        "Tegangan sumber (V RMS)",
        min_value=10,
        max_value=240,
        value=100,
        step=5,
    )

    f = st.slider(
        "Frekuensi sumber (Hz)",
        min_value=10,
        max_value=200,
        value=50,
        step=5,
    )

    R = st.slider(
        "Resistansi R (Ω)",
        min_value=10,
        max_value=200,
        value=60,
        step=5,
    )

    L_mH = st.slider(
        "Induktansi L (mH)",
        min_value=10,
        max_value=500,
        value=200,
        step=10,
    )

    C_uF = st.slider(
        "Kapasitansi C (µF)",
        min_value=10,
        max_value=500,
        value=100,
        step=10,
    )

    st.divider()
    st.markdown("### Cara menggunakan")
    st.caption(
        "1. Atur parameter rangkaian.\n\n"
        "2. Amati nilai dan grafik.\n\n"
        "3. Pelajari verifikasi KVL.\n\n"
        "4. Unduh hasil di bagian akhir."
    )


# =========================================================
# 4. PERHITUNGAN RLC SERI
# =========================================================
L = L_mH / 1000
C = C_uF / 1_000_000

w = 2 * np.pi * f
Vp = V * np.sqrt(2)

XL = w * L
XC = 1 / (w * C)
X = XL - XC

Z = np.sqrt(R**2 + X**2)
I = V / Z
Ip = I * np.sqrt(2)

phi = math.atan2(X, R)
phi_deg = math.degrees(phi)
pf = math.cos(phi)

VR = I * R
VL = I * XL
VC = I * XC

V_kvl = np.sqrt(VR**2 + (VL - VC)**2)
kvl_error = abs(V - V_kvl)

f0 = 1 / (2 * np.pi * np.sqrt(L * C))

P = I**2 * R
Q = I**2 * X
S = V * I

if abs(X) < 1e-9:
    sifat = "Resistif"
    sifat_detail = "XL dan XC hampir sama."
elif X > 0:
    sifat = "Induktif"
    sifat_detail = "XL lebih besar daripada XC."
else:
    sifat = "Kapasitif"
    sifat_detail = "XC lebih besar daripada XL."


# =========================================================
# 5. RINGKASAN HASIL
# =========================================================
section(
    "01 · Ringkasan Hasil Simulasi",
    "Ikhtisar nilai listrik yang dihitung dari parameter rangkaian saat ini.",
)

cols = st.columns(4)

with cols[0]:
    metric_card("Arus RMS", f"{I:.3f} A", "I = V / Z")

with cols[1]:
    metric_card("Impedansi", f"{Z:.2f} Ω", "Z = √(R² + X²)")

with cols[2]:
    metric_card("Sudut fase", f"{phi_deg:.2f}°", "φ = tan⁻¹(X/R)")

with cols[3]:
    metric_card("Faktor daya", f"{pf:.3f}", "cos φ")

st.write("")

cols = st.columns(4)

with cols[0]:
    metric_card("Daya aktif", f"{P:.2f} W", "P = I²R")

with cols[1]:
    metric_card("Daya reaktif", f"{Q:.2f} VAR", "Q = I²X")

with cols[2]:
    metric_card("Daya semu", f"{S:.2f} VA", "S = VI")

with cols[3]:
    metric_card("Karakter rangkaian", sifat, sifat_detail)


# =========================================================
# 6. SKEMA RANGKAIAN DENGAN ANIMASI ARUS
# =========================================================
section(
    "02 · Skema Rangkaian RLC Seri",
    "R, L, dan C tersusun dalam satu lintasan sehingga arus yang sama "
    "mengalir melalui setiap komponen. Titik bergerak merupakan ilustrasi "
    "arah arus konvensional.",
)

circuit_html = f"""
<div style="font-family:Arial,sans-serif;border:1px solid #E4E9F0;
border-radius:14px;background:#fff;padding:12px">
<svg viewBox="0 0 850 335" width="100%"
     role="img" aria-label="Skema RLC seri AC">

  <defs>
    <marker id="currentArrow" markerWidth="8" markerHeight="8"
            refX="5" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="#3678B8"/>
    </marker>
  </defs>

  <g stroke="#17365D" stroke-width="3" fill="none"
     stroke-linecap="round" stroke-linejoin="round">

    <path d="M135 88 H255"/>
    <path d="M335 88 H380"/>
    <path d="M490 88 H670 V240 H135"/>
    <path d="M135 88 V125"/>
    <path d="M135 183 V240"/>

    <circle cx="135" cy="154" r="29" fill="#FFFFFF"/>
    <path d="M119 154 C125 137 132 137 138 154
             S151 171 157 154"
          stroke="#3678B8" stroke-width="2.5"/>

    <rect x="255" y="72" width="80" height="32" fill="#FFFFFF"/>

    <path d="M380 88
             c0 -22 22 -22 22 0
             c0 -22 22 -22 22 0
             c0 -22 22 -22 22 0
             c0 -22 22 -22 22 0"/>

    <path d="M670 88 V133
             M653 133 H687
             M653 154 H687
             M670 154 V240"/>
  </g>

  <path d="M174 55 H233" stroke="#3678B8" stroke-width="2.5"
        fill="none" marker-end="url(#currentArrow)"/>
  <text x="203" y="43" font-size="14" text-anchor="middle"
        fill="#3678B8">i(t)</text>

  <g fill="#17365D" font-size="16" font-weight="600">
    <text x="135" y="38" text-anchor="middle">Sumber AC</text>
    <text x="295" y="47" text-anchor="middle">Resistor</text>
    <text x="435" y="47" text-anchor="middle">Induktor</text>
    <text x="713" y="139">Kapasitor</text>
  </g>

  <g fill="#667085" font-size="14">
    <text x="135" y="291" text-anchor="middle">Vs = {V} V RMS</text>
    <text x="295" y="126" text-anchor="middle">R = {R} Ω</text>
    <text x="435" y="126" text-anchor="middle">L = {L_mH} mH</text>
    <text x="713" y="166">C = {C_uF} µF</text>
    <text x="420" y="291" text-anchor="middle">f = {f} Hz</text>
  </g>

  <circle r="5" fill="#3678B8">
    <animateMotion dur="3s" repeatCount="indefinite"
      path="M135 88 H670 V240 H135 V88"/>
  </circle>
  <circle r="4" fill="#168A85">
    <animateMotion dur="3s" begin="-1s" repeatCount="indefinite"
      path="M135 88 H670 V240 H135 V88"/>
  </circle>
  <circle r="3.5" fill="#E59B3B">
    <animateMotion dur="3s" begin="-2s" repeatCount="indefinite"
      path="M135 88 H670 V240 H135 V88"/>
  </circle>

  <text x="420" y="321" text-anchor="middle"
        font-size="12" fill="#667085">
    Diagram ilustratif rangkaian RLC seri AC
  </text>
</svg>
</div>
"""
components.html(circuit_html, height=365, scrolling=False)

st.markdown(
    f"""
    <div class="info-box">
    <b>Interpretasi:</b> rangkaian bersifat {sifat.lower()}.
    Reaktansi induktif XL = <b>{XL:.2f} Ω</b>, sedangkan reaktansi
    kapasitif XC = <b>{XC:.2f} Ω</b>. Selisih keduanya adalah
    <b>{X:.2f} Ω</b> dan menentukan sifat reaktif rangkaian.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 7. TEGANGAN SETIAP KOMPONEN
# =========================================================
section(
    "03 · Analisis Tegangan Komponen",
    "Bandingkan tegangan RMS pada resistor, induktor, dan kapasitor. "
    "Tegangan sumber merupakan resultan fasor, bukan penjumlahan "
    "aritmetika langsung seluruh nilai tegangan.",
)

voltage_df = pd.DataFrame({
    "Komponen": ["Resistor (VR)", "Induktor (VL)", "Kapasitor (VC)"],
    "Tegangan RMS (V)": [VR, VL, VC],
})

fig_v = go.Figure()

fig_v.add_trace(
    go.Bar(
        x=voltage_df["Komponen"],
        y=voltage_df["Tegangan RMS (V)"],
        marker_color=[BLUE, TEAL, ORANGE],
        text=[f"{x:.2f} V" for x in [VR, VL, VC]],
        textposition="outside",
        hovertemplate="%{x}<br>Tegangan: %{y:.3f} V<extra></extra>",
    )
)

fig_v.update_layout(
    yaxis_title="Tegangan RMS (V)",
    showlegend=False,
)
fig_v = style_chart(fig_v, 350)

st.plotly_chart(fig_v, use_container_width=True)

st.dataframe(
    voltage_df.style.format({"Tegangan RMS (V)": "{:.3f}"}),
    hide_index=True,
    use_container_width=True,
)

st.markdown(
    f"""
    <div class="info-box">
    Tegangan reaktif bersih adalah VL − VC =
    <b>{VL - VC:.3f} V</b>. Tegangan sumber dihitung dari
    Vs = √[VR² + (VL − VC)²] = <b>{V_kvl:.3f} V</b>.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 8. VERIFIKASI HUKUM KIRCHHOFF II
# =========================================================
section(
    "04 · Verifikasi Hukum Kirchhoff II (KVL)",
    "Pada rangkaian AC, Hukum Kirchhoff II diterapkan menggunakan "
    "penjumlahan tegangan dalam bentuk fasor.",
)

st.latex(
    r"\underline{V}_s = "
    r"\underline{V}_R + \underline{V}_L + \underline{V}_C"
)

st.latex(
    r"V_s = \sqrt{V_R^2 + (V_L - V_C)^2}"
)

cols = st.columns(3)

with cols[0]:
    st.metric("Tegangan sumber", f"{V:.4f} V")

with cols[1]:
    st.metric("Hasil perhitungan KVL", f"{V_kvl:.4f} V")

with cols[2]:
    st.metric("Selisih absolut", f"{kvl_error:.8f} V")

if kvl_error < 1e-6:
    st.success(
        "KVL terverifikasi secara numerik: hasil resultan tegangan "
        "sesuai dengan tegangan sumber."
    )
else:
    st.warning("Terdapat selisih numerik pada hasil perhitungan KVL.")

kvl_df = pd.DataFrame({
    "Besaran": ["VR", "VL", "VC", "VL − VC", "Vs hasil KVL"],
    "Nilai": [VR, VL, VC, VL - VC, V_kvl],
    "Satuan": ["V", "V", "V", "V", "V"],
})

st.dataframe(
    kvl_df.style.format({"Nilai": "{:.5f}"}),
    hide_index=True,
    use_container_width=True,
)

st.markdown(
    """
    <div class="info-box">
    <b>Konsep penting:</b> tegangan resistor sefase dengan arus,
    tegangan induktor mendahului arus sebesar 90°, dan tegangan kapasitor
    tertinggal dari arus sebesar 90°. Oleh sebab itu, tegangan induktor
    dan kapasitor berlawanan arah pada sumbu reaktif.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 9. GELOMBANG TEGANGAN DAN ARUS
# =========================================================
section(
    "05 · Visualisasi Gelombang AC",
    "Grafik berikut menunjukkan tegangan sesaat sumber dan masing-masing "
    "komponen selama dua periode. Arah pergeseran gelombang menggambarkan "
    "perbedaan fase.",
)

period = 1 / f
t = np.linspace(0, 2 * period, 1000)
time_ms = t * 1000

vs_t = Vp * np.sin(w * t)
i_t = Ip * np.sin(w * t - phi)
vr_t = Ip * R * np.sin(w * t - phi)
vl_t = Ip * XL * np.sin(w * t - phi + np.pi / 2)
vc_t = Ip * XC * np.sin(w * t - phi - np.pi / 2)

fig_wave = go.Figure()

for name, values, color in [
    ("Tegangan sumber Vs", vs_t, NAVY),
    ("Tegangan resistor VR", vr_t, BLUE),
    ("Tegangan induktor VL", vl_t, TEAL),
    ("Tegangan kapasitor VC", vc_t, ORANGE),
]:
    fig_wave.add_trace(
        go.Scatter(
            x=time_ms,
            y=values,
            name=name,
            mode="lines",
            line=dict(width=2.2, color=color),
            hovertemplate=(
                "Waktu: %{x:.3f} ms<br>"
                "Tegangan: %{y:.3f} V<extra>" + name + "</extra>"
            ),
        )
    )

fig_wave.update_layout(
    xaxis_title="Waktu (ms)",
    yaxis_title="Tegangan sesaat (V)",
    hovermode="x unified",
    legend=dict(orientation="h", y=-0.27),
)
fig_wave = style_chart(fig_wave, 430)

st.plotly_chart(fig_wave, use_container_width=True)

st.markdown("**Gelombang arus rangkaian**")

fig_i = go.Figure()

fig_i.add_trace(
    go.Scatter(
        x=time_ms,
        y=i_t,
        mode="lines",
        name="Arus i(t)",
        line=dict(width=2.5, color=BLUE),
        fill="tozeroy",
        fillcolor="rgba(54,120,184,0.08)",
    )
)

fig_i.update_layout(
    xaxis_title="Waktu (ms)",
    yaxis_title="Arus sesaat (A)",
    showlegend=False,
)
fig_i = style_chart(fig_i, 290)

st.plotly_chart(fig_i, use_container_width=True)

if X > 1e-9:
    phase_text = (
        f"Rangkaian bersifat induktif. Arus tertinggal terhadap "
        f"tegangan sumber sebesar {abs(phi_deg):.2f}°."
    )
elif X < -1e-9:
    phase_text = (
        f"Rangkaian bersifat kapasitif. Arus mendahului "
        f"tegangan sumber sebesar {abs(phi_deg):.2f}°."
    )
else:
    phase_text = "Arus dan tegangan sumber sefase."

st.markdown(
    f'<div class="info-box">{phase_text}</div>',
    unsafe_allow_html=True,
)


# =========================================================
# 10. DIAGRAM FASOR
# =========================================================
section(
    "06 · Diagram Fasor Tegangan",
    "Fasor memvisualisasikan hubungan fase. Tegangan resistor menjadi "
    "referensi horizontal, sedangkan tegangan reaktif bersih berada "
    "pada sumbu vertikal.",
)

fig_ph = go.Figure()

fig_ph.add_trace(
    go.Scatter(
        x=[0, VR],
        y=[0, 0],
        mode="lines+markers",
        name="VR",
        line=dict(color=BLUE, width=3),
        marker=dict(size=7),
    )
)

fig_ph.add_trace(
    go.Scatter(
        x=[VR, VR],
        y=[0, VL - VC],
        mode="lines+markers",
        name="VL − VC",
        line=dict(color=TEAL, width=3),
        marker=dict(size=7),
    )
)

fig_ph.add_trace(
    go.Scatter(
        x=[0, VR],
        y=[0, VL - VC],
        mode="lines+markers",
        name="Vs",
        line=dict(color=ORANGE, width=3),
        marker=dict(size=7),
    )
)

fig_ph.add_annotation(
    x=VR / 2,
    y=0,
    text=f"VR = {VR:.2f} V",
    showarrow=False,
    yshift=15,
)

fig_ph.add_annotation(
    x=VR,
    y=(VL - VC) / 2,
    text=f"VL − VC = {VL - VC:.2f} V",
    showarrow=False,
    xshift=55,
)

fig_ph.add_annotation(
    x=VR / 2,
    y=(VL - VC) / 2,
    text=f"Vs = {V_kvl:.2f} V",
    showarrow=False,
    yshift=16,
)

fig_ph.update_layout(
    xaxis_title="Sumbu sefase arus (V)",
    yaxis_title="Sumbu reaktif (V)",
    legend=dict(orientation="h", y=-0.27),
)
fig_ph.update_yaxes(scaleanchor="x", scaleratio=1)
fig_ph = style_chart(fig_ph, 450)

st.plotly_chart(fig_ph, use_container_width=True)

st.markdown(
    f"""
    <div class="info-box">
    Sudut fase diperoleh dari φ = tan⁻¹[(XL − XC)/R],
    yaitu <b>{phi_deg:.2f}°</b>. Sudut positif menunjukkan sifat
    induktif, sedangkan sudut negatif menunjukkan sifat kapasitif.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 11. RESONANSI DAN DAYA
# =========================================================
section(
    "07 · Resonansi dan Analisis Daya",
    "Kurva menunjukkan respons arus terhadap perubahan frekuensi "
    "dengan R, L, C, dan tegangan sumber tetap.",
)

cols = st.columns(2)

with cols[0]:
    metric_card(
        "Frekuensi resonansi",
        f"{f0:.2f} Hz",
        "f₀ = 1 / (2π√LC)",
    )

with cols[1]:
    metric_card(
        "Frekuensi sumber",
        f"{f:.2f} Hz",
        f"Selisih dari f₀: {abs(f - f0):.2f} Hz",
    )

f_values = np.linspace(max(1, f0 * 0.2), f0 * 2.5, 600)

XL_values = 2 * np.pi * f_values * L
XC_values = 1 / (2 * np.pi * f_values * C)

Z_values = np.sqrt(R**2 + (XL_values - XC_values)**2)
I_values = V / Z_values

fig_res = go.Figure()

fig_res.add_trace(
    go.Scatter(
        x=f_values,
        y=I_values,
        mode="lines",
        name="Arus RMS",
        line=dict(color=BLUE, width=2.7),
        hovertemplate=(
            "Frekuensi: %{x:.2f} Hz<br>"
            "Arus RMS: %{y:.3f} A<extra></extra>"
        ),
    )
)

fig_res.add_vline(
    x=f0,
    line_dash="dash",
    line_color=ORANGE,
    annotation_text=f"f₀ = {f0:.2f} Hz",
)

fig_res.add_vline(
    x=f,
    line_dash="dot",
    line_color=TEAL,
    annotation_text=f"f = {f} Hz",
)

fig_res.update_layout(
    xaxis_title="Frekuensi (Hz)",
    yaxis_title="Arus RMS (A)",
    showlegend=False,
)
fig_res = style_chart(fig_res, 370)

st.plotly_chart(fig_res, use_container_width=True)

power_df = pd.DataFrame({
    "Parameter": [
        "Daya aktif (P)",
        "Daya reaktif (Q)",
        "Daya semu (S)",
        "Faktor daya",
    ],
    "Nilai": [P, Q, S, pf],
    "Satuan": ["W", "VAR", "VA", "—"],
    "Rumus": ["I²R", "I²(XL − XC)", "VI", "cos φ"],
})

st.dataframe(
    power_df.style.format({"Nilai": "{:.4f}"}),
    hide_index=True,
    use_container_width=True,
)

st.markdown(
    f"""
    <div class="info-box">
    <b>Interpretasi:</b> frekuensi resonansi teoritis adalah
    <b>{f0:.2f} Hz</b>. Pada resonansi seri ideal, XL = XC,
    impedansi menjadi minimum (Z = R), arus mencapai maksimum,
    dan faktor daya bernilai 1. Pada frekuensi sumber saat ini,
    rangkaian bersifat <b>{sifat.lower()}</b>.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 12. EKSPOR DATA
# =========================================================
section(
    "08 · Ekspor Data Simulasi",
    "Tabel ini merangkum parameter masukan dan hasil perhitungan. "
    "Unduh file CSV untuk dokumentasi, laporan, atau analisis lanjutan.",
)

export_df = pd.DataFrame(
    [
        ("Tegangan sumber RMS", V, "V"),
        ("Frekuensi sumber", f, "Hz"),
        ("Resistansi", R, "Ω"),
        ("Induktansi", L_mH, "mH"),
        ("Kapasitansi", C_uF, "µF"),
        ("Reaktansi induktif", XL, "Ω"),
        ("Reaktansi kapasitif", XC, "Ω"),
        ("Reaktansi bersih", X, "Ω"),
        ("Impedansi", Z, "Ω"),
        ("Arus RMS", I, "A"),
        ("Arus puncak", Ip, "A"),
        ("Tegangan resistor", VR, "V"),
        ("Tegangan induktor", VL, "V"),
        ("Tegangan kapasitor", VC, "V"),
        ("Tegangan hasil KVL", V_kvl, "V"),
        ("Selisih KVL", kvl_error, "V"),
        ("Sudut fase", phi_deg, "derajat"),
        ("Faktor daya", pf, "—"),
        ("Frekuensi resonansi", f0, "Hz"),
        ("Daya aktif", P, "W"),
        ("Daya reaktif", Q, "VAR"),
        ("Daya semu", S, "VA"),
    ],
    columns=["Parameter", "Nilai", "Satuan"],
)

st.dataframe(
    export_df.style.format({"Nilai": "{:.6f}"}),
    hide_index=True,
    use_container_width=True,
)

csv_data = export_df.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    label="↓  Unduh Hasil Simulasi (CSV)",
    data=csv_data,
    file_name="hasil_simulasi_kirchhoff_rlc_ac.csv",
    mime="text/csv",
)

st.divider()

st.markdown(
    """
    <div class="footer">
        <b style="color:#17365D">Cahya Andung Kusuma</b><br>
        Simulasi Hukum Kirchhoff II pada Rangkaian AC (KVL)<br>
        Media pembelajaran rangkaian listrik dengan model RLC seri ideal.
    </div>
    """,
    unsafe_allow_html=True,
)
