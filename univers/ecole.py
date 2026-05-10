# DOSSIER ÉCOLE - VERSION BLINDÉE (MAXIMUM DE LIGNES)
ECOLE_DATA = {
    "🔢 COMPTER (0 à 100)": [str(i) for i in range(101)],
    
    "🔤 L'ALPHABET (A-Z)": {
        "A": "A", "B": "B", "C": "C", "D": "D", "E": "E", "F": "F", "G": "G", "H": "H", "I": "I", "J": "J",
        "K": "K", "L": "L", "M": "M", "N": "N", "O": "O", "P": "P", "Q": "Q", "R": "R", "S": "S", "T": "T",
        "U": "U", "V": "V", "W": "W", "X": "X", "Y": "Y", "Z": "Z"
    },

    "➕ LES MATHS": {
        "➕ LES DOUBLES (1 à 50)": {f"{i} + {i}": str(i*2) for i in range(1, 51)},
        "✖️ TABLES DE MULTIPLICATION": {
            f"Table de {n}": {f"{n} x {i}": str(n*i) for i in range(1, 11)} for n in range(1, 11)
        }
    },

    "🍎 LE MARCHÉ GÉANT": {
        "🍓 TOUS LES FRUITS": {
            "Abricot 🍑": "Abricot", "Airelle 🔴": "Airelle", "Amande 🫘": "Amande", "Ananas 🍍": "Ananas", 
            "Avocat 🥑": "Avocat", "Banane 🍌": "Banane", "Cacao 🍫": "Cacao", "Cassis 🫐": "Cassis", 
            "Cerise 🍒": "Cerise", "Châtaigne 🌰": "Châtaigne", "Citron 🍋": "Citron", "Citron Vert 🍋": "Lime", 
            "Clémentine 🍊": "Clémentine", "Coing 🍐": "Coing", "Datte 🏺": "Datte", "Figue 🍮": "Figue", 
            "Fraise 🍓": "Fraise", "Framboise 🍓": "Framboise", "Fruit du dragon 🌵": "Pitaya", 
            "Fruit de la passion 🍇": "Maracudja", "Goyave 🍈": "Goyave", "Grenade 🍉": "Grenade", 
            "Groseille 🔴": "Groseille", "Kaki 🥭": "Kaki", "Kiwi 🥝": "Kiwi", "Litchi 🎈": "Litchi", 
            "Mandarine 🍊": "Mandarine", "Mangue 🥭": "Mangue", "Melon 🍈": "Melon", "Mirabelle 🟡": "Mirabelle", 
            "Mûre 🍇": "Mûre", "Myrtille 🫐": "Myrtille", "Noisette 🌰": "Noisette", "Noix 🥥": "Noix", 
            "Noix de coco 🥥": "Noix de coco", "Orange 🍊": "Orange", "Pamplemousse 🍊": "Pamplemousse", 
            "Papaye 🍈": "Papaye", "Pastèque 🍉": "Pastèque", "Pêche 🍑": "Pêche", "Poire 🍐": "Poire", 
            "Pomme 🍎": "Pomme", "Prune 🟣": "Prune", "Raisin 🍇": "Raisin", "Rhubarbe 🌿": "Rhubarbe"
        },
        "🥦 TOUS LES LÉGUMES": {
            "Ail 🧄": "Ail", "Artichaut 🌵": "Artichaut", "Asperge 🎋": "Asperge", "Aubergine 🍆": "Aubergine", 
            "Betterave 🔴": "Betterave", "Blette 🥬": "Blette", "Brocoli 🥦": "Brocoli", "Carotte 🥕": "Carotte", 
            "Céleri 🌿": "Céleri", "Champignon 🍄": "Champignon", "Chou 🥦": "Chou", "Chou-fleur 🥦": "Chou-fleur", 
            "Chou de Bruxelles 🥦": "Chou de Bruxelles", "Ciboulette 🌿": "Ciboulette", "Citrouille 🎃": "Citrouille", 
            "Concombre 🥒": "Concombre", "Courgette 🥒": "Courgette", "Cresson 🌿": "Cresson", "Échalote 🧅": "Échalote", 
            "Endive 🥬": "Endive", "Épinards 🥬": "Épinards", "Fenouil 🌿": "Fenouil", "Fève 🫛": "Fève", 
            "Gingembre 🫚": "Gingembre", "Haricot vert 🫛": "Haricot vert", "Lentilles 🫘": "Lentilles", 
            "Maïs 🌽": "Maïs", "Manioc 🪵": "Manioc", "Navet 🧅": "Navet", "Oignon 🧅": "Oignon", 
            "Panais 🥕": "Panais", "Patate douce 🍠": "Patate douce", "Persil 🌿": "Persil", 
            "Petit pois 🫛": "Petit pois", "Poireau 🥬": "Poireau", "Poivron 🫑": "Poivron", 
            "Pomme de terre 🥔": "Pomme de terre", "Potiron 🎃": "Potiron", "Radis 🔴": "Radis", 
            "Radis noir 🌚": "Radis noir", "Salade 🥗": "Salade", "Topinambour 🥔": "Topinambour", "Tomate 🍅": "Tomate"
        }
    },

    "📅 LE CALENDRIER": {
        "🗓️ LES JOURS": {
            "1️⃣ Lundi": "Lundi", "2️⃣ Mardi": "Mardi", "3️⃣ Mercredi": "Mercredi", 
            "4️⃣ Jeudi": "Jeudi", "5️⃣ Vendredi": "Vendredi", "6️⃣ Samedi": "Samedi", 
            "7️⃣ Dimanche": "Dimanche"
        },
        "📅 LES MOIS": {
            "1 Janvier": "Janvier", "2 Février": "Février", "3 Mars": "Mars", "4 Avril": "Avril",
            "5 Mai": "Mai", "6 Juin": "Juin", "7 Juillet": "Juillet", "8 Août": "Août",
            "9 Septembre": "Septembre", "10 Octobre": "Octobre", "11 Novembre": "Novembre", "12 Décembre": "Décembre"
        },
        "🌸 LES SAISONS": {
            "🌸 Printemps": "C'est le Printemps", "☀️ Été": "C'est l'Été", 
            "🍁 Automne": "C'est l'Automne", "❄️ Hiver": "C'est l'Hiver"
        }
    }
}
