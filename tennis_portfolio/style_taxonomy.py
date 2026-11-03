"""Official 13-style taxonomy for the tennis analysis MVP."""

from __future__ import annotations

import json


OFFICIAL_STYLE_ORDER = [
    "ALL_COURT_ELITE",
    "BIG_SERVER_BASELINER",
    "POWER_BASELINER",
    "OFFENSIVE_COUNTERPUNCHER",
    "CLAY_SPECIALIST",
    "SOLID_OFFENSIVE_SERVER",
    "SOLID_OFFENSIVE_RETURNER",
    "SOLID_OFFENSIVE_CORE",
    "BIG_SERVER",
    "TOPSPIN_BASELINER",
    "ERRATIC_ATTACKER",
    "SOLID_DEFENSIVE",
    "SERVE_AND_VOLLEY",
]


STYLE_DEFINITIONS = {
    "ALL_COURT_ELITE": {
        "label_fr": "All-Court Élite",
        "description": "Profil de tres haut niveau capable de gagner avec le service, le retour, l'attaque et la defense.",
        "maniere_de_jouer": "Adapte le plan de jeu au matchup, prend l'initiative sans perdre la solidite.",
        "profil_statistique_attendu": "Elo global eleve, Elo surface homogene, service fort, retour fort, peu de faiblesse majeure.",
        "forces": "Polyvalence, adaptation, niveau moyen tres haut.",
        "faiblesses": "Peut devenir moins dominant si une composante cle baisse.",
        "joueurs_typiques": ["Jannik Sinner", "Carlos Alcaraz", "Novak Djokovic"],
        "tags": ["elite", "balanced", "complete"],
    },
    "BIG_SERVER_BASELINER": {
        "label_fr": "Big Server + Baseliner",
        "description": "Service dominant, mais avec assez de jeu de fond pour ne pas dependre uniquement des aces.",
        "maniere_de_jouer": "Cherche des points courts au service puis impose en premiere frappe.",
        "profil_statistique_attendu": "Ace rate eleve, service games won eleve, retour correct, bon hard/grass.",
        "forces": "Points gratuits, pression constante sur les jeux de service.",
        "faiblesses": "Peut souffrir si le premier service baisse.",
        "joueurs_typiques": ["Taylor Fritz", "Hubert Hurkacz", "Milos Raonic"],
        "tags": ["serve", "baseline", "hard_grass"],
    },
    "POWER_BASELINER": {
        "label_fr": "Attaquant de Fond Power",
        "description": "Joueur qui cree l'avantage par puissance, cadence et prise d'initiative.",
        "maniere_de_jouer": "Accellere tot dans l'echange et cherche a dicter avec les coups de fond.",
        "profil_statistique_attendu": "Service/retour corrects, Elo eleve, variance moyenne a elevee.",
        "forces": "Pression offensive, capacite a prendre le match en main.",
        "faiblesses": "Peut donner des points si le timing baisse.",
        "joueurs_typiques": ["Jannik Sinner", "Andrey Rublev", "Tomas Berdych"],
        "tags": ["power", "baseline", "attack"],
    },
    "OFFENSIVE_COUNTERPUNCHER": {
        "label_fr": "Counter Puncher Offensif",
        "description": "Retourne fort, absorbe la vitesse adverse puis transforme la defense en attaque.",
        "maniere_de_jouer": "Met beaucoup de balles en jeu, contre vite, attaque les secondes balles.",
        "profil_statistique_attendu": "Return games won eleve, return points won eleve, break conversion elevee, service correct.",
        "forces": "Retour, relance, defense active.",
        "faiblesses": "Moins de points gratuits au service qu'un gros serveur.",
        "joueurs_typiques": ["Carlos Alcaraz", "Daniil Medvedev", "Lleyton Hewitt"],
        "tags": ["return", "counter", "offense"],
    },
    "CLAY_SPECIALIST": {
        "label_fr": "Pur Terrien",
        "description": "Profil dont le rendement sur terre battue est nettement meilleur que sur les autres surfaces.",
        "maniere_de_jouer": "Construit patiemment, utilise le lift, accepte les longs rallyes.",
        "profil_statistique_attendu": "Clay Elo ou clay winrate tres au-dessus du hard/grass.",
        "forces": "Terre battue, endurance, construction.",
        "faiblesses": "Surfaces rapides, points tres courts.",
        "joueurs_typiques": ["Casper Ruud", "Rafael Nadal", "Diego Schwartzman"],
        "tags": ["clay", "topspin", "patience"],
    },
    "SOLID_OFFENSIVE_SERVER": {
        "label_fr": "Solide Offensif Serveur",
        "description": "Service fiable qui lance l'attaque sans atteindre le profil big server pur.",
        "maniere_de_jouer": "Tient souvent ses engagements et cherche la premiere frappe.",
        "profil_statistique_attendu": "Hold eleve, first serve win rate eleve, retour moyen.",
        "forces": "Stabilite au service, points courts.",
        "faiblesses": "Break moins souvent les meilleurs relanceurs.",
        "joueurs_typiques": ["Grigor Dimitrov", "Karen Khachanov", "Matteo Berrettini"],
        "tags": ["serve", "offense", "stable"],
    },
    "SOLID_OFFENSIVE_RETURNER": {
        "label_fr": "Solide Offensif Retourneur",
        "description": "Profil qui gagne de la valeur en retour tout en restant capable d'attaquer.",
        "maniere_de_jouer": "Agresse les jeux de retour et cherche a prendre le controle rapidement.",
        "profil_statistique_attendu": "Return games won eleve, break rate eleve, service moyen ou correct.",
        "forces": "Pression en retour, creation d'occasions de break.",
        "faiblesses": "Service parfois moins dominant.",
        "joueurs_typiques": ["Alex de Minaur", "David Ferrer", "Kei Nishikori"],
        "tags": ["return", "offense", "pressure"],
    },
    "SOLID_OFFENSIVE_CORE": {
        "label_fr": "Solide Offensif Core",
        "description": "Joueur equilibre avec un niveau correct partout mais sans arme extreme.",
        "maniere_de_jouer": "Reste propre, prend l'initiative quand l'occasion est claire.",
        "profil_statistique_attendu": "Stats equilibrees, pas de point tres faible, pas de point extreme.",
        "forces": "Fiabilite, regularite.",
        "faiblesses": "Arme decisive limitee contre l'elite.",
        "joueurs_typiques": ["Roberto Bautista Agut", "Marin Cilic", "Borna Coric"],
        "tags": ["balanced", "solid", "offense"],
    },
    "BIG_SERVER": {
        "label_fr": "Big Server",
        "description": "Profil centre sur le service et la domination des jeux de service.",
        "maniere_de_jouer": "Cherche aces, services gagnants et tie-breaks.",
        "profil_statistique_attendu": "Ace rate tres eleve, hold tres eleve, retour faible.",
        "forces": "Aces, jeux de service, pression scoreboard.",
        "faiblesses": "Peu de marge en retour.",
        "joueurs_typiques": ["John Isner", "Ivo Karlovic", "Reilly Opelka"],
        "tags": ["serve", "aces", "tiebreak"],
    },
    "TOPSPIN_BASELINER": {
        "label_fr": "Attaquant de Fond Lift",
        "description": "Joueur de fond avec volume, lift et tolerance aux rallyes.",
        "maniere_de_jouer": "Use l'adversaire avec trajectoires hautes, lift et regularite.",
        "profil_statistique_attendu": "Clay boost, long rally strength, winrate terre solide.",
        "forces": "Volume, regularite, terre battue.",
        "faiblesses": "Peut etre pris de vitesse sur surface rapide.",
        "joueurs_typiques": ["Casper Ruud", "Rafael Nadal", "Albert Ramos"],
        "tags": ["topspin", "baseline", "clay"],
    },
    "ERRATIC_ATTACKER": {
        "label_fr": "Attaquant Irrégulier",
        "description": "Profil offensif a forte variance, capable de pics tres hauts et de passages faibles.",
        "maniere_de_jouer": "Prend beaucoup de risques, cherche les winners tot.",
        "profil_statistique_attendu": "Upset tendency, dominant wins et close losses eleves, coherence faible.",
        "forces": "Upside, agressivite, capacite a renverser un favori.",
        "faiblesses": "Instabilite, fautes, baisse de niveau brutale.",
        "joueurs_typiques": ["Nick Kyrgios", "Alexander Bublik", "Fabio Fognini"],
        "tags": ["variance", "attack", "risk"],
    },
    "SOLID_DEFENSIVE": {
        "label_fr": "Solide Défensif",
        "description": "Joueur qui prolonge, couvre le terrain et force l'adversaire a jouer un coup de plus.",
        "maniere_de_jouer": "Absorbe, remet, neutralise et attend la baisse adverse.",
        "profil_statistique_attendu": "Retour correct, rally tolerance forte, attaque limitee, faible variance.",
        "forces": "Regularite, defense, gestion des erreurs adverses.",
        "faiblesses": "Difficulte a finir contre joueurs tres puissants.",
        "joueurs_typiques": ["Gilles Simon", "Adrian Mannarino", "Francisco Cerundolo"],
        "tags": ["defense", "solid", "rally"],
    },
    "SERVE_AND_VOLLEY": {
        "label_fr": "Serve & Volleyeur",
        "description": "Profil qui utilise le service pour monter et finir au filet.",
        "maniere_de_jouer": "Raccourcit les points, prend le filet, varie les zones.",
        "profil_statistique_attendu": "Net rush eleve, net strength eleve, points courts, service utile.",
        "forces": "Filet, variation, pression temps.",
        "faiblesses": "Expose aux passings et aux retours bas.",
        "joueurs_typiques": ["Maxime Cressy", "Mischa Zverev", "Feliciano Lopez"],
        "tags": ["net", "serve", "short_points"],
    },
}


def get_style_definition(style_code: str) -> dict:
    """Return the official definition for a style code."""
    code = str(style_code or "SOLID_OFFENSIVE_CORE").upper()
    definition = STYLE_DEFINITIONS.get(code, STYLE_DEFINITIONS["SOLID_OFFENSIVE_CORE"]).copy()
    definition["style_code"] = code if code in STYLE_DEFINITIONS else "SOLID_OFFENSIVE_CORE"
    return definition


def get_style_label(style_code: str) -> str:
    """Return the official French label for a style code."""
    return get_style_definition(style_code)["label_fr"]


def main() -> None:
    """Print the taxonomy as JSON lines."""
    for style in OFFICIAL_STYLE_ORDER:
        print(json.dumps(get_style_definition(style), ensure_ascii=False))


if __name__ == "__main__":
    main()
