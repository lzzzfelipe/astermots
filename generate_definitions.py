"""
Generate basic French definitions for words that don't have one.
Uses morphological rules and hardcoded common words.
"""
import json, re

# --- Hardcoded definitions for very common function words ---
HARDCODED = {
    # Articles & determiners
    "le": ("déterminant", "Article masculin singulier", "Le chat dort."),
    "la": ("déterminant", "Article féminin singulier", "La fleur est belle."),
    "les": ("déterminant", "Article pluriel", "Les enfants jouent."),
    "un": ("déterminant", "Article indéfini masculin", "Un garçon arrive."),
    "une": ("déterminant", "Article indéfini féminin", "Une fille chante."),
    "des": ("déterminant", "Article indéfini pluriel", "Des oiseaux volent."),
    "du": ("déterminant", "Article partitif masculin", "Du pain frais."),
    "au": ("déterminant", "Contraction de 'à le'", "Je vais au parc."),
    "aux": ("déterminant", "Contraction de 'à les'", "Je parle aux enfants."),
    "ce": ("déterminant", "Déterminant démonstratif masculin", "Ce livre est bien."),
    "cet": ("déterminant", "Démonstratif masculin devant voyelle", "Cet arbre est grand."),
    "cette": ("déterminant", "Déterminant démonstratif féminin", "Cette maison est jolie."),
    "ces": ("déterminant", "Déterminant démonstratif pluriel", "Ces fleurs sentent bon."),
    "mon": ("déterminant", "Déterminant possessif (à moi)", "Mon chien est gentil."),
    "ma": ("déterminant", "Déterminant possessif féminin (à moi)", "Ma sœur est grande."),
    "mes": ("déterminant", "Déterminant possessif pluriel (à moi)", "Mes amis sont là."),
    "ton": ("déterminant", "Déterminant possessif (à toi)", "Ton cahier est bleu."),
    "ta": ("déterminant", "Déterminant possessif féminin (à toi)", "Ta chambre est propre."),
    "tes": ("déterminant", "Déterminant possessif pluriel (à toi)", "Tes jouets sont ici."),
    "son": ("déterminant", "Déterminant possessif (à lui/elle)", "Son frère est petit."),
    "sa": ("déterminant", "Déterminant possessif féminin (à lui/elle)", "Sa mère cuisine."),
    "ses": ("déterminant", "Déterminant possessif pluriel (à lui/elle)", "Ses chaussures sont neuves."),
    "notre": ("déterminant", "Déterminant possessif (à nous)", "Notre classe est grande."),
    "nos": ("déterminant", "Déterminant possessif pluriel (à nous)", "Nos parents arrivent."),
    "votre": ("déterminant", "Déterminant possessif (à vous)", "Votre maison est belle."),
    "vos": ("déterminant", "Déterminant possessif pluriel (à vous)", "Vos enfants grandissent."),
    "leur": ("déterminant", "Déterminant possessif (à eux)", "Leur chat dort."),
    "leurs": ("déterminant", "Déterminant possessif pluriel (à eux)", "Leurs amis jouent."),
    "tout": ("déterminant", "Chaque chose, l'ensemble", "Tout le monde rit."),
    "toute": ("déterminant", "Féminin de 'tout'", "Toute la journée."),
    "tous": ("déterminant", "Pluriel de 'tout'", "Tous les jours."),
    "toutes": ("déterminant", "Féminin pluriel de 'tout'", "Toutes les filles."),
    "chaque": ("déterminant", "Chacun, un par un", "Chaque jour est nouveau."),
    "quel": ("déterminant", "Mot pour poser une question", "Quel âge as-tu ?"),
    "quelle": ("déterminant", "Féminin de 'quel'", "Quelle heure est-il ?"),
    "quelque": ("déterminant", "Un certain nombre de", "Quelque chose de bien."),
    "aucun": ("déterminant", "Pas un seul", "Aucun problème."),
    "aucune": ("déterminant", "Pas une seule", "Aucune erreur."),
    "autre": ("déterminant", "Différent, pas le même", "Un autre jour."),
    "même": ("adjectif", "Pareil, identique", "Le même livre."),
    "tel": ("déterminant", "De cette sorte", "Un tel plaisir."),
    "telle": ("déterminant", "Féminin de 'tel'", "Une telle joie."),
    "plusieurs": ("déterminant", "Plus d'un", "Plusieurs amis."),
    "certain": ("déterminant", "Quelques-uns", "Un certain temps."),
    "certaine": ("déterminant", "Féminin de 'certain'", "Une certaine idée."),

    # Pronouns
    "je": ("pronom", "La personne qui parle", "Je suis content."),
    "tu": ("pronom", "La personne à qui on parle", "Tu es gentil."),
    "il": ("pronom", "Pronom masculin singulier", "Il court vite."),
    "elle": ("pronom", "Pronom féminin singulier", "Elle chante bien."),
    "on": ("pronom", "Quelqu'un, nous (familier)", "On va jouer !"),
    "nous": ("pronom", "Le groupe qui inclut celui qui parle", "Nous mangeons."),
    "vous": ("pronom", "La ou les personnes à qui on parle", "Vous êtes grands."),
    "ils": ("pronom", "Pronom masculin pluriel", "Ils jouent dehors."),
    "elles": ("pronom", "Pronom féminin pluriel", "Elles dansent."),
    "me": ("pronom", "Pronom complément (moi)", "Il me regarde."),
    "te": ("pronom", "Pronom complément (toi)", "Je te vois."),
    "se": ("pronom", "Pronom réfléchi", "Il se lave."),
    "le": ("pronom", "Pronom complément masculin", "Je le vois."),
    "lui": ("pronom", "Pronom complément indirect", "Je lui parle."),
    "moi": ("pronom", "Pronom tonique (1re personne)", "C'est pour moi."),
    "toi": ("pronom", "Pronom tonique (2e personne)", "C'est à toi."),
    "soi": ("pronom", "Pronom tonique réfléchi", "Chacun pour soi."),
    "eux": ("pronom", "Pronom tonique masculin pluriel", "C'est pour eux."),
    "qui": ("pronom", "Mot interrogatif pour une personne", "Qui est là ?"),
    "que": ("conjonction", "Mot de liaison entre deux idées", "Je sais que tu es là."),
    "quoi": ("pronom", "Mot interrogatif pour une chose", "Tu fais quoi ?"),
    "ça": ("pronom", "Cette chose-là (familier)", "Ça va bien."),
    "cela": ("pronom", "Cette chose-là", "Cela me plaît."),
    "ceci": ("pronom", "Cette chose-ci", "Prends ceci."),
    "celui": ("pronom", "Démonstratif masculin", "Celui qui rit."),
    "celle": ("pronom", "Démonstratif féminin", "Celle qui chante."),
    "ceux": ("pronom", "Démonstratif masculin pluriel", "Ceux qui jouent."),
    "rien": ("pronom", "Aucune chose", "Il n'y a rien."),
    "personne": ("pronom", "Aucune personne", "Personne ne vient."),
    "quelqu'un": ("pronom", "Une personne", "Quelqu'un frappe."),
    "chacun": ("pronom", "Chaque personne", "Chacun son tour."),
    "l'": ("pronom", "Pronom élidé (le ou la)", "Je l'aime."),
    "d'": ("préposition", "De (devant voyelle)", "Beaucoup d'amis."),
    "s'": ("pronom", "Se (devant voyelle)", "Il s'amuse."),
    "t'": ("pronom", "Te (devant voyelle)", "Je t'aime."),
    "y": ("pronom", "Pronom de lieu (là-bas)", "J'y vais."),
    "en": ("pronom", "Pronom partitif (de cela)", "J'en veux."),

    # Prepositions
    "de": ("préposition", "Mot qui indique l'origine ou l'appartenance", "Le livre de Marie."),
    "à": ("préposition", "Mot qui indique la direction ou le lieu", "Je vais à l'école."),
    "dans": ("préposition", "À l'intérieur de", "Dans la maison."),
    "pour": ("préposition", "Destiné à, en faveur de", "Un cadeau pour toi."),
    "avec": ("préposition", "En compagnie de", "Je joue avec mon ami."),
    "sur": ("préposition", "Au-dessus de, posé sur", "Le chat est sur la table."),
    "sous": ("préposition", "En dessous de", "Le chat est sous le lit."),
    "par": ("préposition", "À travers, au moyen de", "Passer par la porte."),
    "entre": ("préposition", "Au milieu de deux choses", "Entre toi et moi."),
    "vers": ("préposition", "En direction de", "Marcher vers l'école."),
    "chez": ("préposition", "À la maison de", "Chez mamie."),
    "sans": ("préposition", "L'absence de quelque chose", "Sans sucre."),
    "avant": ("préposition", "Plus tôt que", "Avant le dîner."),
    "après": ("préposition", "Plus tard que", "Après l'école."),
    "depuis": ("préposition", "À partir d'un moment", "Depuis ce matin."),
    "pendant": ("préposition", "Durant, au cours de", "Pendant la nuit."),
    "contre": ("préposition", "En opposition à", "Contre le mur."),
    "devant": ("préposition", "En face de, à l'avant", "Devant la porte."),
    "derrière": ("préposition", "À l'arrière de", "Derrière la maison."),
    "jusqu'à": ("préposition", "Jusqu'au bout de", "Jusqu'à demain."),
    "parmi": ("préposition", "Au milieu de plusieurs", "Parmi les fleurs."),
    "selon": ("préposition", "D'après, suivant", "Selon la météo."),
    "malgré": ("préposition", "En dépit de", "Malgré la pluie."),
    "sauf": ("préposition", "À l'exception de", "Tous sauf un."),
    "dès": ("préposition", "À partir de", "Dès demain."),
    "hors": ("préposition", "En dehors de", "Hors de la maison."),
    "envers": ("préposition", "À l'égard de", "Gentil envers tous."),

    # Conjunctions
    "et": ("conjonction", "Mot pour ajouter quelque chose", "Toi et moi."),
    "ou": ("conjonction", "Choix entre deux choses", "Rouge ou bleu ?"),
    "mais": ("conjonction", "Mot qui oppose deux idées", "Petit mais fort."),
    "car": ("conjonction", "Parce que", "Je reste car il pleut."),
    "si": ("conjonction", "Mot pour une condition", "Si tu veux."),
    "quand": ("conjonction", "Au moment où", "Quand il pleut."),
    "comme": ("conjonction", "De la même façon que", "Grand comme un arbre."),
    "ni": ("conjonction", "Pas l'un et pas l'autre", "Ni toi ni moi."),
    "donc": ("adverbe", "Par conséquent, alors", "Je pense, donc je suis."),
    "puis": ("adverbe", "Ensuite, après", "D'abord manger, puis jouer."),
    "aussi": ("adverbe", "Également, de même", "Moi aussi !"),
    "encore": ("adverbe", "Une fois de plus", "Encore un peu."),
    "déjà": ("adverbe", "Avant maintenant", "C'est déjà fini."),
    "très": ("adverbe", "Beaucoup, fortement", "Très content."),
    "bien": ("adverbe", "De bonne manière", "C'est bien fait."),
    "mal": ("adverbe", "De mauvaise manière", "J'ai mal au ventre."),
    "peu": ("adverbe", "Pas beaucoup", "Un peu de lait."),
    "beaucoup": ("adverbe", "En grande quantité", "Beaucoup de bonbons."),
    "trop": ("adverbe", "Plus que nécessaire", "C'est trop lourd."),
    "assez": ("adverbe", "Suffisamment", "Assez de gâteau."),
    "jamais": ("adverbe", "À aucun moment", "Je ne mens jamais."),
    "toujours": ("adverbe", "À chaque fois, sans arrêt", "Il rit toujours."),
    "souvent": ("adverbe", "Fréquemment", "Je lis souvent."),
    "parfois": ("adverbe", "De temps en temps", "Parfois il neige."),
    "ici": ("adverbe", "À cet endroit", "Viens ici !"),
    "là": ("adverbe", "À cet endroit-là", "Il est là."),
    "où": ("adverbe", "À quel endroit", "Où es-tu ?"),
    "comment": ("adverbe", "De quelle manière", "Comment vas-tu ?"),
    "pourquoi": ("adverbe", "Pour quelle raison", "Pourquoi tu ris ?"),
    "combien": ("adverbe", "Quelle quantité", "Combien ça coûte ?"),
    "ne": ("adverbe", "Mot de négation", "Je ne sais pas."),
    "pas": ("adverbe", "Mot de négation", "Ce n'est pas vrai."),
    "plus": ("adverbe", "Davantage / ne... plus", "Il n'y en a plus."),
    "moins": ("adverbe", "Pas autant", "Moins de bruit."),
    "oui": ("adverbe", "Réponse affirmative", "Oui, je veux bien."),
    "non": ("adverbe", "Réponse négative", "Non merci."),
    "peut-être": ("adverbe", "C'est possible", "Peut-être demain."),
    "maintenant": ("adverbe", "En ce moment", "Viens maintenant !"),
    "aujourd'hui": ("adverbe", "Ce jour", "Aujourd'hui c'est lundi."),
    "demain": ("adverbe", "Le jour d'après", "À demain !"),
    "hier": ("adverbe", "Le jour d'avant", "Hier il a plu."),
    "vite": ("adverbe", "Rapidement", "Cours vite !"),
    "loin": ("adverbe", "À grande distance", "C'est trop loin."),
    "près": ("adverbe", "À petite distance", "Tout près d'ici."),
    "ensemble": ("adverbe", "L'un avec l'autre", "Jouons ensemble !"),
    "surtout": ("adverbe", "Par-dessus tout", "Surtout, sois prudent."),
    "enfin": ("adverbe", "Pour finir", "Enfin les vacances !"),
    "vraiment": ("adverbe", "En vérité", "C'est vraiment beau."),
    "seulement": ("adverbe", "Rien de plus", "Seulement deux."),
    "presque": ("adverbe", "Pas tout à fait", "Presque fini !"),
    "autant": ("adverbe", "La même quantité", "J'en veux autant."),
    "tant": ("adverbe", "Tellement", "Tant mieux !"),

    # Common verbs (infinitive form)
    "être": ("verbe", "Exister, se trouver quelque part", "Je suis ici."),
    "avoir": ("verbe", "Posséder quelque chose", "J'ai un chat."),
    "faire": ("verbe", "Réaliser, fabriquer", "Faire un dessin."),
    "dire": ("verbe", "Parler, exprimer avec des mots", "Dire bonjour."),
    "aller": ("verbe", "Se déplacer d'un endroit à un autre", "Aller à l'école."),
    "voir": ("verbe", "Regarder avec les yeux", "Voir un oiseau."),
    "savoir": ("verbe", "Connaître, avoir appris", "Savoir lire."),
    "pouvoir": ("verbe", "Être capable de", "Je peux courir."),
    "vouloir": ("verbe", "Avoir envie de", "Je veux jouer."),
    "venir": ("verbe", "Arriver, se déplacer vers ici", "Venir à la maison."),
    "devoir": ("verbe", "Être obligé de", "Je dois dormir."),
    "prendre": ("verbe", "Saisir avec la main", "Prendre un livre."),
    "trouver": ("verbe", "Découvrir quelque chose", "Trouver un trésor."),
    "donner": ("verbe", "Offrir quelque chose à quelqu'un", "Donner un cadeau."),
    "parler": ("verbe", "Utiliser des mots pour communiquer", "Parler français."),
    "aimer": ("verbe", "Avoir beaucoup d'affection pour", "Aimer sa famille."),
    "passer": ("verbe", "Traverser, aller au-delà", "Passer devant la maison."),
    "mettre": ("verbe", "Placer quelque chose quelque part", "Mettre ses chaussures."),
    "demander": ("verbe", "Poser une question", "Demander le chemin."),
    "tenir": ("verbe", "Garder dans ses mains", "Tenir un ballon."),
    "sembler": ("verbe", "Avoir l'air de", "Il semble content."),
    "laisser": ("verbe", "Ne pas prendre, abandonner", "Laisser la porte ouverte."),
    "rester": ("verbe", "Ne pas partir, demeurer", "Rester à la maison."),
    "penser": ("verbe", "Réfléchir dans sa tête", "Penser à ses amis."),
    "croire": ("verbe", "Penser que c'est vrai", "Croire au père Noël."),
    "comprendre": ("verbe", "Saisir le sens de quelque chose", "Comprendre une histoire."),
    "connaître": ("verbe", "Savoir qui est quelqu'un", "Connaître son voisin."),
    "sentir": ("verbe", "Percevoir une odeur ou une sensation", "Sentir les fleurs."),
    "attendre": ("verbe", "Rester jusqu'à ce que quelque chose arrive", "Attendre le bus."),
    "entendre": ("verbe", "Percevoir des sons avec les oreilles", "Entendre de la musique."),
    "tomber": ("verbe", "Chuter vers le bas", "Tomber par terre."),
    "perdre": ("verbe", "Ne plus avoir quelque chose", "Perdre ses clés."),
    "commencer": ("verbe", "Démarrer, débuter", "Commencer un jeu."),
    "finir": ("verbe", "Terminer, arriver à la fin", "Finir ses devoirs."),
    "sortir": ("verbe", "Aller dehors", "Sortir de la maison."),
    "entrer": ("verbe", "Aller à l'intérieur", "Entrer dans la classe."),
    "ouvrir": ("verbe", "Faire qu'on peut passer ou voir à travers", "Ouvrir la fenêtre."),
    "fermer": ("verbe", "Bloquer l'accès ou la vue", "Fermer la porte."),
    "lire": ("verbe", "Regarder des mots écrits et les comprendre", "Lire un livre."),
    "écrire": ("verbe", "Tracer des lettres ou des mots", "Écrire une lettre."),
    "courir": ("verbe", "Se déplacer très vite sur ses pieds", "Courir dans le jardin."),
    "manger": ("verbe", "Mettre de la nourriture dans sa bouche", "Manger une pomme."),
    "boire": ("verbe", "Avaler un liquide", "Boire de l'eau."),
    "dormir": ("verbe", "Se reposer les yeux fermés", "Dormir la nuit."),
    "jouer": ("verbe", "S'amuser", "Jouer au ballon."),
    "chanter": ("verbe", "Faire de la musique avec sa voix", "Chanter une chanson."),
    "danser": ("verbe", "Bouger son corps en rythme", "Danser la valse."),
    "dessiner": ("verbe", "Faire une image avec un crayon", "Dessiner un soleil."),
    "marcher": ("verbe", "Se déplacer à pied", "Marcher dans la forêt."),
    "monter": ("verbe", "Aller vers le haut", "Monter les escaliers."),
    "descendre": ("verbe", "Aller vers le bas", "Descendre la colline."),
    "porter": ("verbe", "Transporter ou avoir sur soi", "Porter un chapeau."),
    "montrer": ("verbe", "Faire voir quelque chose", "Montrer un dessin."),
    "suivre": ("verbe", "Aller derrière quelqu'un", "Suivre le chemin."),
    "vivre": ("verbe", "Être en vie", "Vivre heureux."),
    "mourir": ("verbe", "Cesser de vivre", "La fleur va mourir."),
    "apprendre": ("verbe", "Acquérir de nouvelles connaissances", "Apprendre à nager."),
    "servir": ("verbe", "Être utile, aider", "Servir le repas."),
    "recevoir": ("verbe", "Obtenir quelque chose", "Recevoir un cadeau."),
    "répondre": ("verbe", "Donner une réponse", "Répondre à la question."),
    "rendre": ("verbe", "Redonner ce qu'on a pris", "Rendre un livre."),
    "rappeler": ("verbe", "Faire penser à quelque chose", "Rappeler un souvenir."),
    "appeler": ("verbe", "Dire le nom de quelqu'un fort", "Appeler son ami."),
    "compter": ("verbe", "Dire les nombres dans l'ordre", "Compter jusqu'à dix."),
    "raconter": ("verbe", "Dire une histoire", "Raconter un conte."),
    "choisir": ("verbe", "Prendre ce qu'on préfère", "Choisir un gâteau."),
    "rire": ("verbe", "Exprimer la joie avec des sons", "Rire aux éclats."),
    "pleurer": ("verbe", "Avoir des larmes qui coulent", "Pleurer de tristesse."),
    "crier": ("verbe", "Parler très fort", "Crier de joie."),
    "jeter": ("verbe", "Lancer loin de soi", "Jeter la balle."),
    "toucher": ("verbe", "Mettre la main sur quelque chose", "Toucher le mur."),
    "regarder": ("verbe", "Diriger ses yeux vers", "Regarder un film."),
    "écouter": ("verbe", "Prêter attention aux sons", "Écouter la musique."),
    "chercher": ("verbe", "Essayer de trouver", "Chercher ses clés."),
    "essayer": ("verbe", "Tenter de faire quelque chose", "Essayer de nager."),

    # Common nouns
    "homme": ("nom", "Personne adulte masculine", "Un homme grand.", "m"),
    "femme": ("nom", "Personne adulte féminine", "Une femme gentille.", "f"),
    "enfant": ("nom", "Jeune personne, garçon ou fille", "Un enfant joue.", "m"),
    "jour": ("nom", "Période de 24 heures", "Un beau jour.", "m"),
    "temps": ("nom", "Durée qui passe", "Le temps passe vite.", "m"),
    "fois": ("nom", "Occasion, moment où quelque chose se passe", "Une fois par semaine.", "f"),
    "chose": ("nom", "Objet ou idée", "Une belle chose.", "f"),
    "vie": ("nom", "Le fait d'être vivant", "La vie est belle.", "f"),
    "main": ("nom", "Partie du corps au bout du bras", "Lever la main.", "f"),
    "œil": ("nom", "Organe pour voir", "Un bel œil.", "m"),
    "yeux": ("nom", "Pluriel d'œil, organes pour voir", "De beaux yeux.", "m"),
    "tête": ("nom", "Partie du corps au-dessus du cou", "Lever la tête.", "f"),
    "monde": ("nom", "La Terre et tout ce qui s'y trouve", "Tout le monde.", "m"),
    "an": ("nom", "Période de 12 mois", "Un an de plus.", "m"),
    "année": ("nom", "Période de 12 mois", "Une bonne année.", "f"),
    "mot": ("nom", "Groupe de lettres qui veut dire quelque chose", "Un mot gentil.", "m"),
    "père": ("nom", "Papa, parent masculin", "Mon père est grand.", "m"),
    "mère": ("nom", "Maman, parent féminin", "Ma mère est douce.", "f"),
    "fils": ("nom", "Enfant garçon de quelqu'un", "Le fils du roi.", "m"),
    "fille": ("nom", "Enfant féminin de quelqu'un", "La fille du roi.", "f"),
    "frère": ("nom", "Garçon qui a les mêmes parents", "Mon frère aîné.", "m"),
    "sœur": ("nom", "Fille qui a les mêmes parents", "Ma petite sœur.", "f"),
    "ami": ("nom", "Personne qu'on aime bien", "Mon meilleur ami.", "m"),
    "amie": ("nom", "Personne qu'on aime bien (féminin)", "Ma meilleure amie.", "f"),
    "heure": ("nom", "Unité de temps de 60 minutes", "Quelle heure est-il ?", "f"),
    "maison": ("nom", "Bâtiment où on habite", "Une jolie maison.", "f"),
    "porte": ("nom", "Ouverture pour entrer et sortir", "Ferme la porte.", "f"),
    "place": ("nom", "Endroit, espace libre", "Prendre sa place.", "f"),
    "rue": ("nom", "Chemin en ville bordé de maisons", "Traverser la rue.", "f"),
    "pays": ("nom", "Territoire avec ses habitants", "Un grand pays.", "m"),
    "terre": ("nom", "Le sol, ou notre planète", "La Terre tourne.", "f"),
    "eau": ("nom", "Liquide transparent qu'on boit", "Un verre d'eau.", "f"),
    "air": ("nom", "Ce qu'on respire", "L'air pur.", "m"),
    "nuit": ("nom", "Quand il fait noir dehors", "La nuit étoilée.", "f"),
    "coeur": ("nom", "Organe qui bat dans la poitrine", "Mon cœur bat.", "m"),
    "cœur": ("nom", "Organe qui bat dans la poitrine", "Mon cœur bat.", "m"),
    "voix": ("nom", "Sons qu'on fait en parlant", "Une belle voix.", "f"),
    "nom": ("nom", "Mot qui désigne une personne ou chose", "Quel est ton nom ?", "m"),

    # Common adjectives
    "bon": ("adjectif", "Agréable, de qualité", "Un bon gâteau."),
    "bonne": ("adjectif", "Féminin de 'bon'", "Une bonne idée."),
    "grand": ("adjectif", "De grande taille", "Un grand arbre."),
    "grande": ("adjectif", "Féminin de 'grand'", "Une grande maison."),
    "petit": ("adjectif", "De petite taille", "Un petit chat."),
    "petite": ("adjectif", "Féminin de 'petit'", "Une petite fleur."),
    "beau": ("adjectif", "Agréable à regarder", "Un beau jour."),
    "belle": ("adjectif", "Féminin de 'beau'", "Une belle étoile."),
    "nouveau": ("adjectif", "Qui vient d'apparaître", "Un nouveau livre."),
    "nouvelle": ("adjectif", "Féminin de 'nouveau'", "Une nouvelle amie."),
    "vieux": ("adjectif", "Qui existe depuis longtemps", "Un vieux château."),
    "vieille": ("adjectif", "Féminin de 'vieux'", "Une vieille maison."),
    "jeune": ("adjectif", "Qui n'est pas vieux", "Un jeune garçon."),
    "long": ("adjectif", "De grande longueur", "Un long chemin."),
    "longue": ("adjectif", "Féminin de 'long'", "Une longue route."),
    "gros": ("adjectif", "Qui prend beaucoup de place", "Un gros ballon."),
    "grosse": ("adjectif", "Féminin de 'gros'", "Une grosse pomme."),
    "blanc": ("adjectif", "De la couleur de la neige", "Un chat blanc."),
    "blanche": ("adjectif", "Féminin de 'blanc'", "Une robe blanche."),
    "noir": ("adjectif", "De la couleur de la nuit", "Un chien noir."),
    "noire": ("adjectif", "Féminin de 'noir'", "Une nuit noire."),
    "rouge": ("adjectif", "De la couleur du sang", "Un ballon rouge."),
    "bleu": ("adjectif", "De la couleur du ciel", "Le ciel bleu."),
    "bleue": ("adjectif", "Féminin de 'bleu'", "La mer bleue."),
    "vert": ("adjectif", "De la couleur de l'herbe", "Un arbre vert."),
    "verte": ("adjectif", "Féminin de 'vert'", "Une pomme verte."),
    "jaune": ("adjectif", "De la couleur du soleil", "Un poussin jaune."),
    "joli": ("adjectif", "Agréable à voir, mignon", "Un joli dessin."),
    "jolie": ("adjectif", "Féminin de 'joli'", "Une jolie fleur."),
    "haut": ("adjectif", "Élevé, vers le ciel", "Un mur haut."),
    "haute": ("adjectif", "Féminin de 'haut'", "Une tour haute."),
    "fort": ("adjectif", "Qui a beaucoup de force", "Un homme fort."),
    "forte": ("adjectif", "Féminin de 'fort'", "Une femme forte."),
    "premier": ("adjectif", "Qui vient avant tous les autres", "Le premier jour."),
    "première": ("adjectif", "Féminin de 'premier'", "La première fois."),
    "dernier": ("adjectif", "Qui vient après tous les autres", "Le dernier jour."),
    "dernière": ("adjectif", "Féminin de 'dernier'", "La dernière page."),
    "seul": ("adjectif", "Sans personne d'autre", "Tout seul."),
    "seule": ("adjectif", "Féminin de 'seul'", "Toute seule."),
    "plein": ("adjectif", "Qui est rempli", "Un verre plein."),
    "vrai": ("adjectif", "Qui est réel, pas faux", "Une vraie histoire."),
    "faux": ("adjectif", "Qui n'est pas vrai", "Un faux billet."),
    "possible": ("adjectif", "Qui peut arriver", "C'est possible."),
    "sûr": ("adjectif", "Certain, sans danger", "C'est sûr."),
    "simple": ("adjectif", "Facile, pas compliqué", "Un jeu simple."),
    "pauvre": ("adjectif", "Qui n'a pas beaucoup d'argent", "Un homme pauvre."),
    "riche": ("adjectif", "Qui a beaucoup d'argent", "Un homme riche."),
    "content": ("adjectif", "Heureux, satisfait", "Je suis content."),
    "contente": ("adjectif", "Féminin de 'content'", "Elle est contente."),
    "heureux": ("adjectif", "Qui ressent de la joie", "Un enfant heureux."),
    "heureuse": ("adjectif", "Féminin de 'heureux'", "Une fille heureuse."),
    "triste": ("adjectif", "Qui a du chagrin", "Un visage triste."),
    "gentil": ("adjectif", "Aimable et doux", "Un garçon gentil."),
    "gentille": ("adjectif", "Féminin de 'gentil'", "Une fille gentille."),
    "méchant": ("adjectif", "Qui fait du mal", "Le méchant loup."),
    "méchante": ("adjectif", "Féminin de 'méchant'", "La méchante sorcière."),
    "chaud": ("adjectif", "Qui a une température élevée", "Un chocolat chaud."),
    "chaude": ("adjectif", "Féminin de 'chaud'", "Une soupe chaude."),
    "froid": ("adjectif", "Qui a une basse température", "Un vent froid."),
    "froide": ("adjectif", "Féminin de 'froid'", "De l'eau froide."),
    "dur": ("adjectif", "Difficile ou solide", "Un sol dur."),
    "dure": ("adjectif", "Féminin de 'dur'", "Une vie dure."),
    "doux": ("adjectif", "Agréable au toucher, tendre", "Un tissu doux."),
    "douce": ("adjectif", "Féminin de 'doux'", "Une voix douce."),
    "propre": ("adjectif", "Qui est net, pas sale", "Des mains propres."),
    "sale": ("adjectif", "Qui n'est pas propre", "Des pieds sales."),
    "sec": ("adjectif", "Qui n'est pas mouillé", "Un chemin sec."),
    "mouillé": ("adjectif", "Couvert d'eau", "Un chien mouillé."),

    # More common words without clear morphological pattern
    "est-ce que": ("adverbe", "Mot pour poser une question", "Est-ce que tu viens ?"),
    "dieu": ("nom", "Être supérieur et créateur", "Mon Dieu !", "m"),
    "besoin": ("nom", "Ce qu'il nous faut", "J'ai besoin d'aide.", "m"),
    "accord": ("nom", "Entente entre personnes", "D'accord !", "m"),
    "juste": ("adjectif", "Correct et équitable", "C'est juste."),
    "gens": ("nom", "Des personnes", "Les gens sont gentils.", "m"),
    "parce que": ("conjonction", "Mot qui donne la raison", "Je ris parce que c'est drôle."),
    "hein": ("interjection", "Mot familier pour demander", "C'est bien, hein ?"),
    "oeil": ("nom", "Organe pour voir", "Ferme un œil.", "m"),
    "fait": ("nom", "Chose qui est vraie, réalité", "C'est un fait.", "m"),
    "eh": ("interjection", "Exclamation pour interpeller", "Eh bien !"),
    "truc": ("nom", "Chose, objet (familier)", "C'est quoi ce truc ?", "m"),
    "tard": ("adverbe", "À un moment avancé", "Il est tard."),
    "quelques": ("déterminant", "Un petit nombre de", "Quelques amis."),
    "type": ("nom", "Sorte, ou un homme (familier)", "Un drôle de type.", "m"),
    "mec": ("nom", "Homme, garçon (familier)", "Un mec sympa.", "m"),
    "fou": ("adjectif", "Qui n'est pas raisonnable", "C'est fou !"),
    "folle": ("adjectif", "Féminin de 'fou'", "Elle est folle de joie."),
    "prêt": ("adjectif", "Qui est préparé", "Je suis prêt !"),
    "prête": ("adjectif", "Féminin de 'prêt'", "Elle est prête."),
    "part": ("nom", "Morceau, portion", "Une part de gâteau.", "f"),
    "longtemps": ("adverbe", "Pendant une longue durée", "Il y a longtemps."),
    "gars": ("nom", "Garçon, homme (familier)", "Un bon gars.", "m"),
    "cas": ("nom", "Situation particulière", "En tout cas.", "m"),
    "salut": ("interjection", "Bonjour ou au revoir (familier)", "Salut les amis !"),
    "désolé": ("adjectif", "Qui regrette", "Je suis désolé."),
    "désolée": ("adjectif", "Féminin de 'désolé'", "Je suis désolée."),
    "suite": ("nom", "Ce qui vient après", "La suite de l'histoire.", "f"),
    "mari": ("nom", "L'époux d'une femme", "Son mari est grand.", "m"),
    "là-bas": ("adverbe", "À cet endroit éloigné", "Regarde là-bas !"),
    "corps": ("nom", "L'ensemble du physique d'une personne", "Le corps humain.", "m"),
    "autres": ("adjectif", "Les différents, les restants", "Les autres enfants."),
    "ok": ("interjection", "D'accord", "Ok, je viens !"),
    "façon": ("nom", "Manière de faire", "De toute façon.", "f"),
    "dont": ("pronom", "Pronom relatif (de qui, de quoi)", "Le livre dont je parle."),
    "arme": ("nom", "Objet pour se défendre ou attaquer", "Une arme de chevalier.", "f"),
    "cause": ("nom", "Raison, motif", "À cause de la pluie.", "f"),
    "reste": ("nom", "Ce qui est encore là", "Le reste du gâteau.", "m"),
    "tiens": ("interjection", "Pour donner ou exprimer la surprise", "Tiens, prends ça !"),
    "plutôt": ("adverbe", "De préférence, assez", "Plutôt content."),
    "droit": ("nom", "Ce qu'on peut faire selon la loi", "Le droit de jouer.", "m"),
    "chef": ("nom", "Personne qui dirige", "Le chef de cuisine.", "m"),
    "tour": ("nom", "Mouvement circulaire ou bâtiment élevé", "La tour Eiffel.", "m"),
    "instant": ("nom", "Très court moment", "Un instant s'il te plaît.", "m"),
    "parent": ("nom", "Père ou mère", "Un parent aimant.", "m"),
    "lieu": ("nom", "Endroit, place", "Un beau lieu.", "m"),
    "aide": ("nom", "Action d'aider quelqu'un", "Besoin d'aide.", "f"),
    "numéro": ("nom", "Chiffre qui identifie", "Le numéro 1.", "m"),
    "chéri": ("nom", "Personne qu'on aime tendrement", "Mon chéri.", "m"),
    "chérie": ("nom", "Féminin de 'chéri'", "Ma chérie.", "f"),
    "faute": ("nom", "Erreur, ce qui est mal fait", "Une faute d'orthographe.", "f"),
    "sinon": ("conjonction", "Autrement, dans le cas contraire", "Dépêche-toi sinon on sera en retard."),
    "café": ("nom", "Boisson chaude brune ou lieu où on la boit", "Un café au lait.", "m"),
    "compte": ("nom", "Calcul, ou compte en banque", "Rendre des comptes.", "m"),
    "facile": ("adjectif", "Pas difficile, simple", "Un exercice facile."),
    "esprit": ("nom", "L'intelligence, la pensée", "Un bon esprit.", "m"),
    "flic": ("nom", "Policier (familier)", "Un flic sympa.", "m"),
    "âge": ("nom", "Nombre d'années qu'on a vécu", "Quel âge as-tu ?", "m"),
    "force": ("nom", "Capacité physique ou puissance", "La force des bras.", "f"),
    "difficile": ("adjectif", "Pas facile, compliqué", "Un problème difficile."),
    "paix": ("nom", "Absence de guerre, calme", "La paix dans le monde.", "f"),
    "président": ("nom", "Chef d'un pays ou d'un groupe", "Le président parle.", "m"),
    "cours": ("nom", "Leçon à l'école", "Un cours de français.", "m"),
    "grave": ("adjectif", "Sérieux, important", "Ce n'est pas grave."),
    "partout": ("adverbe", "Dans tous les endroits", "Il y a des fleurs partout."),
    "âme": ("nom", "La partie invisible de nous", "Une belle âme.", "f"),
    "patron": ("nom", "Chef d'une entreprise", "Le patron du restaurant.", "m"),
    "médecin": ("nom", "Docteur qui soigne les gens", "Aller chez le médecin.", "m"),
    "rapport": ("nom", "Lien entre deux choses", "Quel rapport ?", "m"),
    "avis": ("nom", "Ce qu'on pense de quelque chose", "À mon avis.", "m"),
    "retour": ("nom", "Action de revenir", "Le retour à la maison.", "m"),
    "génial": ("adjectif", "Super, formidable", "C'est génial !"),
    "dollar": ("nom", "Monnaie américaine", "Un dollar.", "m"),
    "pareil": ("adjectif", "Identique, le même", "C'est pareil."),
    "pareille": ("adjectif", "Féminin de 'pareil'", "Elle est pareille."),
    "tôt": ("adverbe", "De bonne heure", "Se lever tôt."),
    "ailleurs": ("adverbe", "Dans un autre endroit", "Va jouer ailleurs."),
    "bout": ("nom", "Extrémité, fin", "Au bout du chemin.", "m"),
    "faim": ("nom", "Envie de manger", "J'ai faim !", "f"),
    "soif": ("nom", "Envie de boire", "J'ai soif !", "f"),
    "bras": ("nom", "Partie du corps entre l'épaule et la main", "Ouvre les bras.", "m"),
    "pied": ("nom", "Partie du corps au bout de la jambe", "Un coup de pied.", "m"),
    "dos": ("nom", "Partie arrière du corps", "Mal au dos.", "m"),
    "doigt": ("nom", "Les cinq parties au bout de la main", "Montrer du doigt.", "m"),
    "sang": ("nom", "Liquide rouge dans le corps", "Du sang rouge.", "m"),
    "bruit": ("nom", "Son fort ou désagréable", "Un grand bruit.", "m"),
    "mur": ("nom", "Paroi verticale d'une construction", "Le mur est blanc.", "m"),
    "sol": ("nom", "Surface sur laquelle on marche", "Le sol est propre.", "m"),
    "ciel": ("nom", "L'étendue bleue au-dessus de nous", "Le ciel est bleu.", "m"),
    "bois": ("nom", "Matière des arbres, ou petite forêt", "Un bout de bois.", "m"),
    "lit": ("nom", "Meuble pour dormir", "Aller au lit.", "m"),
    "clé": ("nom", "Objet pour ouvrir une serrure", "La clé de la maison.", "f"),
    "loi": ("nom", "Règle que tout le monde doit suivre", "La loi est la loi.", "f"),
    "roi": ("nom", "Chef d'un royaume", "Le roi est juste.", "m"),
    "reine": ("nom", "Femme du roi ou chef d'un royaume", "La reine est sage.", "f"),
    "feu": ("nom", "Flammes qui brûlent", "Le feu réchauffe.", "m"),
    "jeu": ("nom", "Activité pour s'amuser", "Un jeu de cartes.", "m"),
    "droit": ("adjectif", "Qui ne penche pas, correct", "Une ligne droite."),
    "plat": ("nom", "Récipient pour servir la nourriture, ou mets", "Un bon plat.", "m"),
    "plan": ("nom", "Projet ou dessin d'ensemble", "Un bon plan.", "m"),
    "prix": ("nom", "Ce que coûte quelque chose", "Le prix est bas.", "m"),
    "voiture": ("nom", "Véhicule à quatre roues", "Une belle voiture.", "f"),
    "classe": ("nom", "Salle d'école ou groupe d'élèves", "La classe de CE1.", "f"),
    "lettre": ("nom", "Signe de l'alphabet ou message écrit", "Écrire une lettre.", "f"),
    "terre": ("nom", "Sol, ou notre planète", "La Terre tourne.", "f"),

    # Interjections
    "oh": ("interjection", "Exclamation de surprise", "Oh, c'est beau !"),
    "ah": ("interjection", "Exclamation de compréhension", "Ah, je comprends !"),
    "hé": ("interjection", "Pour appeler quelqu'un", "Hé, viens ici !"),
    "bon": ("interjection", "Pour marquer l'accord", "Bon, d'accord."),
    "voilà": ("adverbe", "Pour montrer quelque chose", "Voilà ton sac !"),

    # Other common words
    "merci": ("nom", "Mot pour remercier", "Merci beaucoup !", "m"),
    "monsieur": ("nom", "Titre pour un homme adulte", "Bonjour monsieur.", "m"),
    "madame": ("nom", "Titre pour une femme adulte", "Bonjour madame.", "f"),
    "peur": ("nom", "Sentiment quand on a peur", "Avoir peur du noir.", "f"),
    "point": ("nom", "Petit rond, ou sujet", "Un point final.", "m"),
    "côté": ("nom", "Face, direction", "De l'autre côté.", "m"),
    "moment": ("nom", "Court instant", "Un bon moment.", "m"),
    "parti": ("nom", "Groupe politique / décision", "Prendre parti.", "m"),
    "partie": ("nom", "Morceau d'un tout", "Une partie du gâteau.", "f"),
    "sorte": ("nom", "Type, genre de chose", "Une sorte de gâteau.", "f"),
    "coup": ("nom", "Choc, action rapide", "Un coup de vent.", "m"),
    "raison": ("nom", "Cause, motif", "La raison du retard.", "f"),
    "état": ("nom", "Situation, condition", "En bon état.", "m"),
    "effet": ("nom", "Résultat, conséquence", "Un bel effet.", "m"),
    "genre": ("nom", "Type, sorte", "Un genre de musique.", "m"),
}

# --- Morphological categorization rules ---
def categorize_by_ending(word):
    """Guess category and generate a definition based on French morphology."""
    w = word.lower()

    # Verb infinitives
    if w.endswith("er") and len(w) > 3:
        return "verbe", f"Verbe : {w}"
    if w.endswith("ir") and len(w) > 3:
        return "verbe", f"Verbe : {w}"
    if w.endswith("re") and len(w) > 3:
        return "verbe", f"Verbe : {w}"
    if w.endswith("oir") and len(w) > 4:
        return "verbe", f"Verbe : {w}"

    # Adverbs (-ment)
    if w.endswith("ment") and len(w) > 5:
        base = w[:-4]
        # Try to recover the adjective root
        if base.endswith("m"):
            adj = base + "nt"  # e.g., lentement → lent
        elif base.endswith("é") or base.endswith("i") or base.endswith("u"):
            adj = base
        else:
            adj = base
        return "adverbe", f"De manière {adj}e" if not adj.endswith("e") else f"De manière {adj}"

    # Nouns by suffix (with meaningful descriptions)
    noun_suffixes = {
        "ation": ("nom", "f", "Action ou résultat"),
        "ition": ("nom", "f", "Action ou résultat"),
        "tion": ("nom", "f", "Action ou résultat"),
        "sion": ("nom", "f", "Action ou résultat"),
        "ment": ("nom", "m", "Action ou résultat"),
        "age": ("nom", "m", "Action ou résultat"),
        "isme": ("nom", "m", "Idée ou mouvement"),
        "iste": ("nom", "m", "Personne qui pratique"),
        "teur": ("nom", "m", "Personne qui fait l'action"),
        "eur": ("nom", "m", "Personne ou chose qui agit"),
        "trice": ("nom", "f", "Personne qui fait l'action"),
        "euse": ("nom", "f", "Personne ou chose qui agit"),
        "ière": ("nom", "f", "Personne ou lieu lié à"),
        "ier": ("nom", "m", "Personne ou arbre lié à"),
        "ence": ("nom", "f", "Qualité ou état"),
        "ance": ("nom", "f", "Qualité ou état"),
        "ité": ("nom", "f", "Qualité ou caractéristique"),
        "té": ("nom", "f", "Qualité ou état"),
        "été": ("nom", "f", "Qualité ou caractéristique"),
        "esse": ("nom", "f", "Qualité ou état"),
        "ise": ("nom", "f", "Qualité ou manière"),
        "ée": ("nom", "f", "Résultat ou contenu"),
        "ie": ("nom", "f", "Domaine ou qualité"),
        "ure": ("nom", "f", "Résultat d'une action"),
        "ette": ("nom", "f", "Petite chose"),
        "aille": ("nom", "f", "Ensemble ou collection"),
        "ille": ("nom", "f", "Nom féminin"),
        "ine": ("nom", "f", "Substance ou lieu"),
        "oir": ("nom", "m", "Objet ou lieu"),
        "eau": ("nom", "m", "Nom masculin"),
        "al": ("nom", "m", "Nom masculin"),
        "ail": ("nom", "m", "Nom masculin"),
        "eil": ("nom", "m", "Nom masculin"),
        "euil": ("nom", "m", "Nom masculin"),
        "ot": ("nom", "m", "Petite chose"),
        "et": ("nom", "m", "Petite chose"),
        "on": ("nom", "m", "Nom masculin"),
    }
    for suffix, (cat, gender, hint) in sorted(noun_suffixes.items(), key=lambda x: -len(x[0])):
        if w.endswith(suffix) and len(w) > len(suffix) + 1:
            return cat, f"({gender}.) {hint}"

    # Adjective suffixes
    adj_suffixes_map = {
        "ique": "Qui se rapporte à",
        "able": "Qui peut être",
        "ible": "Qui peut être",
        "eux": "Qui a la qualité de",
        "euse": "Qui a la qualité de",
        "if": "Qui a tendance à",
        "ive": "Qui a tendance à",
        "al": "Qui se rapporte à",
        "ale": "Qui se rapporte à",
        "el": "Qui se rapporte à",
        "elle": "Qui se rapporte à",
        "ien": "Qui vient de ou se rapporte à",
        "ienne": "Qui vient de ou se rapporte à",
        "ain": "Qui vient de",
        "aine": "Qui vient de",
        "ois": "Qui vient de",
        "oise": "Qui vient de",
        "ais": "Qui vient de",
        "aise": "Qui vient de",
    }
    for suffix, hint in sorted(adj_suffixes_map.items(), key=lambda x: -len(x[0])):
        if w.endswith(suffix) and len(w) > len(suffix) + 1:
            return "adjectif", hint

    return "nom", "Mot français"


def generate_definition(word):
    """Generate a basic definition for a French word."""
    w = word.lower()

    # Check hardcoded first
    if w in HARDCODED:
        entry = HARDCODED[w]
        if len(entry) == 4:
            return entry[0], entry[1], entry[2], entry[3]
        return entry[0], entry[1], entry[2], None

    cat, defn = categorize_by_ending(w)
    return cat, defn, "", None


def main():
    import os

    with open("src/data/dictionary.json", "r", encoding="utf-8-sig") as f:
        dictionary = json.load(f)

    # Load kid_defs.json if it exists (handcrafted definitions)
    kid_defs = {}
    if os.path.exists("kid_defs.json"):
        with open("kid_defs.json", "r", encoding="utf-8") as f:
            kid_defs = json.load(f)
        print(f"Loaded {len(kid_defs)} handcrafted definitions from kid_defs.json")

    # Normalize English category labels to French
    cat_map = {
        "noun": "nom", "verb": "verbe", "adjective": "adjectif",
        "adverb": "adverbe", "preposition": "préposition",
        "conjunction": "conjonction", "pronoun": "pronom",
        "interjection": "interjection", "determiner": "déterminant",
    }
    for entry in dictionary:
        c = entry.get("category", "").lower()
        if c in cat_map:
            entry["category"] = cat_map[c]

    # Detect auto-generated definitions that should be re-generated
    auto_patterns = ["Mot français", "Action de ", "(m.)", "(f.)", "Qui est ",
                     "Verbe :", "Qui se rapporte", "Qui peut être",
                     "Qui a la qualité", "Qui a tendance", "Qui vient de",
                     "De manière"]

    updated = 0
    from_kid_defs = 0
    for entry in dictionary:
        defn = entry.get("definition", "")
        is_auto = not defn or any(p in defn for p in auto_patterns)
        if not is_auto:
            continue

        word = entry["word"]

        # Priority 1: kid_defs.json handcrafted definitions
        if word in kid_defs:
            kd = kid_defs[word]
            entry["category"] = kd["cat"]
            entry["definition"] = kd["def"]
            entry["example"] = kd.get("ex", "")
            if kd.get("g"):
                entry["gender"] = kd["g"]
            from_kid_defs += 1
            updated += 1
            continue

        # Priority 2: Hardcoded + morphology
        cat, defn, example, gender = generate_definition(word)
        entry["category"] = cat
        entry["definition"] = defn
        entry["example"] = example
        if gender:
            entry["gender"] = gender

        updated += 1

    with open("src/data/dictionary.json", "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)

    print(f"Updated {updated} entries out of {len(dictionary)} total.")
    print(f"  From kid_defs.json: {from_kid_defs}")
    print(f"  From hardcoded/morphology: {updated - from_kid_defs}")

    # Stats
    good = len([e for e in dictionary if not any(p in e.get("definition","") for p in ["Mot français"])])
    print(f"  Words with meaningful definitions: {good}/{len(dictionary)}")

    samples = [e for e in dictionary if e["word"] in ["chenille", "papillon", "manger", "rapidement", "courage", "liberté", "ange", "requin"]]
    for s in samples:
        print(f"  {s['word']}: [{s['category']}] {s['definition']}")


if __name__ == "__main__":
    main()
