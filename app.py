st.markdown("""
    <style>
    .stApp { background-color: #000; }
    .titre-enfant { 
        text-align: center; 
        color: #FF00FF; 
        font-size: 32px; 
        font-weight: 900; 
        text-shadow: 2px 2px #00FBFF;
        margin-bottom: 20px; 
    }
    
    /* Boutons Dossiers - Gris Anthracite et Néon */
    .btn-dossier button {
        background-color: #1A1A1A !important; 
        border: 4px solid #555 !important;
        height: 110px !important; 
        font-size: 24px !important; 
        border-radius: 30px !important;
        color: #FFF !important; 
        margin-bottom: 12px !important;
    }
    
    /* Boutons Objets - EFFET ARC-EN-CIEL */
    .btn-objet:nth-child(5n+1) button { background: linear-gradient(135deg, #FF0055, #FF5500) !important; } /* Rouge/Orange */
    .btn-objet:nth-child(5n+2) button { background: linear-gradient(135deg, #00FBFF, #0077FF) !important; } /* Bleu/Cyan */
    .btn-objet:nth-child(5n+3) button { background: linear-gradient(135deg, #AA00FF, #FF00FF) !important; } /* Violet/Rose */
    .btn-objet:nth-child(5n+4) button { background: linear-gradient(135deg, #00FF00, #008800) !important; } /* Vert */
    .btn-objet:nth-child(5n+5) button { background: linear-gradient(135deg, #FFD700, #FF8C00) !important; } /* Jaune/Or */

    .btn-objet button {
        height: 100px !important; 
        font-size: 24px !important; 
        border-radius: 25px !important;
        color: white !important; 
        border: 3px solid rgba(255,255,255,0.3) !important;
        margin-bottom: 12px !important;
        font-weight: bold !important;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.5) !important;
    }

    .btn-retour button {
        background: #FF0055 !important; 
        height: 60px !important; 
        border-radius: 50px !important;
        font-weight: 900 !important;
    }
    </style>
    """, unsafe_allow_html=True)
