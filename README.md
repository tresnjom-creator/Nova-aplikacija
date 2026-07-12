import streamlit as st
import numpy as np
from scipy.stats import poisson

# Podešavanje izgleda stranice
st.set_page_config(page_title="Hasimsport AI Simulator", layout="centered")

st.title("⚽ Hasimsport: AI Simulator Utakmica")
st.write("Predviđanje ishoda mečeva pomoću Poissonovog matematičkog modela.")

st.markdown("---")

# Lista ekipa sa njihovim simuliranim napadačkim i odbrambenim rejtinzima
# (Ovo služi kao baza dok kasnije ne spojimo pravi API)
podaci_o_ekipama = {
    "Argentina": {"napad": 2.2, "odbrana": 0.8},
    "Francuska": {"napad": 2.1, "odbrana": 0.9},
    "Brazil": {"napad": 1.9, "odbrana": 1.0},
    "Engleska": {"napad": 1.8, "odbrana": 0.7},
    "Španija": {"napad": 2.0, "odbrana": 1.1},
    "Njemačka": {"napad": 1.7, "odbrana": 1.2}
}

ekipe = list(podaci_o_ekipama.keys())

# Izbor timova na telefonu
col1, col2 = st.columns(2)
with col1:
    domacin = st.selectbox("Domaćin:", ekipe, index=0)
with col2:
    gost = st.selectbox("Gost:", ekipe, index=1)

st.markdown("---")

# Funkcija koja računa vjerovatnoće za 1, X, 2 i golove
def simuliraj_mec(tim1, tim2):
    # Računamo očekivani broj golova na meču
    # Očekivani golovi domaćina = napad domaćina * odbrana gosta
    lambda_domacin = podaci_o_ekipama[tim1]["napad"] * podaci_o_ekipama[tim2]["odbrana"]
    lambda_gost = podaci_o_ekipama[tim2]["napad"] * podaci_o_ekipama[tim1]["odbrana"]
    
    # Matrica za rezultate (od 0 do 5 golova za svakog)
    pob_domacin = 0
    remi = 0
    pob_gost = 0
    preko_2_5 = 0
    
    for i in range(6): # Golovi domaćina
        for j in range(6): # Golovi gosta
            # Vjerovatnoća tačnog rezultata (npr. 2:1)
            p_rezultat = poisson.pmf(i, lambda_domacin) * poisson.pmf(j, lambda_gost)
            
            if i > j:
                pob_domacin += p_rezultat
            elif i == j:
                remi += p_rezultat
            else:
                pob_gost += p_rezultat
                
            if (i + j) > 2.5:
                preko_2_5 += p_rezultat
                
    return pob_domacin * 100, remi * 100, pob_gost * 100, preko_2_5 * 100

# Dugme za pokretanje analize
if st.button("Pokreni AI Simulaciju 🚀"):
    if domacin == gost:
        st.warning("Izaberi dva različita tima!")
    else:
        p1, px, p2, over25 = simuliraj_mec(domacin, gost)
        
        st.success(f"### Rezultati simulacije za: {domacin} vs {gost}")
        
        # Prikaz procenata u kolonama
        k1, k2, k3 = st.columns(3)
        k1.metric(label="Pobjeda Domaćina (1)", value=f"{p1:.1f}%")
        k2.metric(label="Nerešeno (X)", value=f"{px:.1f}%")
        k3.metric(label="Pobjeda Gosta (2)", value=f"{p2:.1f}%")
        
        st.markdown("---")
        
        # Statika za golove, ključna stvar za tikete
        st.subheader("📊 Golovi statistika")
        st.write(f"Šansa za **Više od 2.5 gola** na meču: **{over25:.1f}%**")
