# DOSSIER ÉCOLE - VERSION AVEC RÉSULTATS VOCAUX CORRIGÉS
ECOLE_DATA = {
    "🔢 COMPTER (0 à 100)": [str(i) for i in range(101)],
    
    "🔤 L'ALPHABET (A-Z)": {
        "A": "A", "B": "B", "C": "C", "D": "D", "E": "E", "F": "F", "G": "G", "H": "H", "I": "I", "J": "J",
        "K": "K", "L": "L", "M": "M", "N": "N", "O": "O", "P": "P", "Q": "Q", "R": "R", "S": "S", "T": "T",
        "U": "U", "V": "V", "W": "W", "X": "X", "Y": "Y", "Z": "Z"
    },

    "➕ LES MATHS": {
        "➕ LES DOUBLES (1 à 50)": {
            # Ici on affiche "1 + 1" sur le bouton, et l'appli dira "2"
            f"{i} + {i}": str(i*2) for i in range(1, 51)
        },
        "✖️ TABLES DE MULTIPLICATION": {
            # On crée un dossier par table
            f"Table de {n}": {
                # Sur le bouton "2 x 3", l'appli dira "6"
                f"{n} x {i}": str(n*i) for i in range(1, 11)
            } for n in range(1, 11)
        }
    },

    "🍎 LE MARCHÉ GÉANT": {
        "🍓 TOUS LES FRUITS": {
            "Abricot 🍑": "Abricot", "Ananas 🍍": "Ananas", "Banane 🍌": "Banane", 
            "Cassis 🫐": "Cassis", "Cerise 🍒": "Cerise", "Citron 🍋": "Citron", 
            "Clémentine 🍊": "Clémentine", "Datte 🏺": "Datte", "Figue 🍮": "Figue", 
            "Fraise 🍓": "Fraise", "Framboise 🍓": "Framboise", "Kiwi 🥝": "Kiwi", 
            "Litchi 🎈": "Litchi", "Mangue 🥭": "Mangue", "Melon 🍈": "Melon", 
            "Mûre 🍇": "Mûre", "Myrtille 🫐": "Myrtille", "Noix de coco 🥥": "Noix de coco", 
            "Orange 🍊": "Orange", "Pastèque 🍉": "Pastèque", "Pêche 🍑": "Pêche", 
            "Poire 🍐": "Poire", "Pomme 🍎": "Pomme", "Raisin 🍇": "Raisin"
        },
        "🥦 TOUS LES LÉGUMES": {
            "Ail 🧄": "Ail", "Artichaut 🌵": "Artichaut", "Asperge 🎋": "Asperge", 
            "Aubergine 🍆": "Aubergine", "Betterave 🔴": "Betterave", "Brocoli 🥦": "Brocoli", 
            "Carotte 🥕": "Carotte", "Champignon 🍄": "Champignon", "Chou 🥦": "Chou", 
            "Citrouille 🎃": "Citrouille", "Concombre 🥒": "Concombre", "Courgette 🥒": "Courgette",
            "Épinards 🥬": "Épinards", "Haricot vert 🫛": "Haricot vert", "Maïs 🌽": "Maïs", 
            "Oignon 🧅": "Oignon", "Petit pois 🫛": "Petit pois", "Poivron 🫑": "Poivron", 
            "Pomme de terre 🥔": "Pomme de terre", "Radis 🔴": "Radis", "Salade 🥗": "Salade", 
            "Tomate 🍅": "Tomate"
        }
    },

    "📅 LE CALENDRIER": {
        "🗓️ LES JOURS": {
            "1️⃣ Lundi": "Lundi", "2️⃣ Mardi": "Mardi", "3️⃣ Mercredi": "Mercredi", 
            "4️⃣ Jeudi": "Jeudi", "5️⃣ Vendredi": "Vendredi", "6️⃣ Samedi": "Samedi", 
            "7️⃣ Dimanche": "Dimanche"
        },
        "📅 LES MOIS": {
            "1 Janvier": "Janvier", "2 Février": "Février", "3 Mars": "Mars", 
            "4 Avril": "Avril", "5 Mai": "Mai", "6 Juin": "Juin", 
            "7 Juillet": "Juillet", "8 Août": "Août", "9 Septembre": "Septembre", 
            "10 Octobre": "Octobre", "11 Novembre": "Novembre", "12 Décembre": "Décembre"
        },
        "🌸 LES SAISONS": {
            "🌸 Printemps": "C'est le Printemps", "☀️ Été": "C'est l'Été", 
            "🍁 Automne": "C'est l'Automne", "❄️ Hiver": "C'est l'Hiver"
        }
    }
}
