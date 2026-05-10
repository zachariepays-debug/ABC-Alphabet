st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');

    /* Fond dégradé pastel animé */
    .stApp {{ 
        background: linear-gradient(-45deg, #FFD6E8, #C9F2FF, #D8FFF1, #FFF2B2);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }}

    @keyframes gradient {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* TITRE PRINCIPAL - VIOLET FLASHY */
    .titre-enfant {{ 
        text-align: center; 
        color: #8A63FF !important; /* Violet qui claque */
        font-size: 42px; 
        font-family: 'Fredoka One', cursive;
        text-shadow: 2px 2px 0px #FFFFFF, 4px 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 5px;
    }}

    /* SLOGAN - ROSE FLUO */
    .slogan {{
        text-align: center;
        color: #FF1493 !important; /* Rose foncé */
        font-size: 20px;
        font-family: 'Fredoka One', cursive;
        margin-bottom: 25px;
        text-shadow: 1px 1px 0px #FFF;
    }}

    /* BOUTONS DOSSIERS - TEXTE ORANGE FONCÉ */
    .btn-dossier button {{
        background: #FFF2B2 !important; 
        border: 5px solid #FFCC00 !important;
        height: 120px !important; 
        font-size: 28px !important; 
        border-radius: 40px !important;
        color: #D35400 !important; /* Orange foncé pour la lecture */
        margin-bottom: 15px !important;
        box-shadow: 0px 10px 0px #FFB300 !important;
        font-family: 'Fredoka One', cursive !important;
    }}
    
    /* BOUTONS OBJETS - TEXTE GRIS TRÈS FONCÉ */
    .btn-objet button {{
        height: 100px !important; 
        font-size: 26px !important; 
        border-radius: 35px !important;
        color: #2C3E50 !important; /* Bleu nuit presque noir pour que ça ressorte */
        margin-bottom: 15px !important;
        font-family: 'Fredoka One', cursive !important;
        font-weight: bold !important;
    }}

    /* Couleurs des boutons (on garde tes pastels mais avec texte sombre) */
    .btn-objet:nth-child(5n+1) button {{ background: #FFD6E8 !important; border: 4px solid #FF85B3 !important; box-shadow: 0px 8px 0px #FF5C9D !important; }}
    .btn-objet:nth-child(5n+2) button {{ background: #C9F2FF !important; border: 4px solid #70D1F4 !important; box-shadow: 0px 8px 0px #3EADE2 !important; }}
    .btn-objet:nth-child(5n+3) button {{ background: #D8FFF1 !important; border: 4px solid #85E3B3 !important; box-shadow: 0px 8px 0px #5BCB8E !important; }}
    .btn-objet:nth-child(5n+4) button {{ background: #E5D9FF !important; border: 4px solid #B194FF !important; box-shadow: 0px 8px 0px #8A63FF !important; }}
    .btn-objet:nth-child(5n+5) button {{ background: #FFF2B2 !important; border: 4px solid #F4D03F !important; box-shadow: 0px 8px 0px #D4AC0D !important; }}

    /* BOUTON RETOUR */
    .btn-retour button {{
        background: #FF1493 !important; 
        color: white !important;
        height: 70px !important; 
        border-radius: 50px !important;
        font-size: 22px !important;
        border: 4px solid white !important;
        font-family: 'Fredoka One', cursive !important;
    }}
    
    .nav-bar {{ 
        background: rgba(255,255,255,0.8); 
        padding: 15px; 
        border-radius: 60px; 
        display: flex; 
        justify-content: center; 
        gap: 15px; 
        box-shadow: 0px 10px 30px rgba(0,0,0,0.1); 
        margin-bottom: 30px; 
    }}
    </style>
    """, unsafe_allow_html=True)
