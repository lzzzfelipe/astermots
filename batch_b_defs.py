#!/usr/bin/env python3
"""Batch B: 100 handcrafted kid-friendly definitions."""
import json

new_defs = {
    "viser": {
        "definition": "Essayer de toucher quelque chose en regardant bien où on lance ou tire.",
        "example": "Il vise la cible avec son arc."
    },
    "génie": {
        "definition": "Une personne très très intelligente, ou un être magique dans les contes.",
        "example": "Le génie de la lampe a exaucé trois vœux."
    },
    "tribunal": {
        "definition": "L'endroit où un juge décide si quelqu'un a fait quelque chose de mal.",
        "example": "Le voleur est allé au tribunal."
    },
    "malheureux": {
        "definition": "Qui est très triste et qui n'a pas de chance.",
        "example": "Le petit chien abandonné avait l'air malheureux."
    },
    "millier": {
        "definition": "Un groupe d'environ mille choses.",
        "example": "Il y avait des milliers d'étoiles dans le ciel."
    },
    "lèvre": {
        "definition": "La partie rose et douce autour de ta bouche.",
        "example": "Elle s'est mordu la lèvre en mangeant."
    },
    "promener": {
        "definition": "Marcher dehors pour le plaisir, souvent avec quelqu'un ou un animal.",
        "example": "On va promener le chien au parc."
    },
    "venger": {
        "definition": "Faire quelque chose de mal à quelqu'un parce qu'il t'a fait du mal avant.",
        "example": "Il ne faut pas chercher à se venger."
    },
    "changement": {
        "definition": "Quand quelque chose devient différent de ce qu'il était avant.",
        "example": "Le changement de saison apporte de nouvelles couleurs."
    },
    "responsabilité": {
        "definition": "Quand c'est à toi de t'occuper de quelque chose ou de quelqu'un.",
        "example": "Nourrir le poisson rouge, c'est ta responsabilité."
    },
    "informer": {
        "definition": "Dire quelque chose d'important à quelqu'un pour qu'il le sache.",
        "example": "La maîtresse nous a informés de la sortie scolaire."
    },
    "pression": {
        "definition": "Une force qui pousse sur quelque chose, ou quand on se sent stressé.",
        "example": "L'eau sort du tuyau à cause de la pression."
    },
    "propriétaire": {
        "definition": "La personne à qui appartient quelque chose, comme une maison ou un animal.",
        "example": "Le propriétaire du chat est venu le chercher."
    },
    "lier": {
        "definition": "Attacher des choses ensemble ou devenir ami avec quelqu'un.",
        "example": "On peut lier les deux cordes ensemble."
    },
    "chair": {
        "definition": "La partie molle du corps sous la peau, ou la viande qu'on mange.",
        "example": "La chair de la pêche est très juteuse."
    },
    "effrayer": {
        "definition": "Faire très peur à quelqu'un.",
        "example": "Le tonnerre a effrayé le petit chat."
    },
    "fêter": {
        "definition": "Célébrer un événement joyeux avec de la musique, des gâteaux ou des amis.",
        "example": "On va fêter ton anniversaire samedi !"
    },
    "saisir": {
        "definition": "Attraper quelque chose rapidement avec la main, ou comprendre une idée.",
        "example": "Il a saisi la balle au vol."
    },
    "impliquer": {
        "definition": "Faire participer quelqu'un à quelque chose.",
        "example": "Ce jeu implique toute la classe."
    },
    "ordonner": {
        "definition": "Dire à quelqu'un ce qu'il doit faire, comme un chef.",
        "example": "Le capitaine a ordonné à l'équipage de lever l'ancre."
    },
    "principal": {
        "definition": "Ce qui est le plus important parmi plusieurs choses.",
        "example": "Le personnage principal de l'histoire est une petite fille."
    },
    "faveur": {
        "definition": "Un service gentil qu'on fait pour quelqu'un.",
        "example": "Peux-tu me faire une faveur et m'aider ?"
    },
    "menteur": {
        "definition": "Une personne qui ne dit pas la vérité.",
        "example": "Le menteur a dit qu'il n'avait pas mangé le gâteau."
    },
    "carrière": {
        "definition": "Le métier qu'on fait pendant longtemps dans sa vie.",
        "example": "Elle rêve d'une carrière de vétérinaire."
    },
    "série": {
        "definition": "Plusieurs choses qui se suivent, ou une histoire à la télé avec beaucoup d'épisodes.",
        "example": "J'ai regardé trois épisodes de ma série préférée."
    },
    "indiquer": {
        "definition": "Montrer ou dire où se trouve quelque chose.",
        "example": "Le panneau indique la direction de l'école."
    },
    "examiner": {
        "definition": "Regarder quelque chose de très près pour bien le comprendre.",
        "example": "Le docteur a examiné mon genou."
    },
    "puer": {
        "definition": "Sentir très très mauvais.",
        "example": "Les chaussettes sales puent !"
    },
    "avaler": {
        "definition": "Faire descendre la nourriture dans le ventre après avoir mâché.",
        "example": "Mâche bien avant d'avaler !"
    },
    "portable": {
        "definition": "Quelque chose qu'on peut transporter facilement, comme un téléphone.",
        "example": "Maman a oublié son téléphone portable à la maison."
    },
    "rencontre": {
        "definition": "Quand on voit quelqu'un pour la première fois ou par hasard.",
        "example": "J'ai fait une belle rencontre au parc."
    },
    "démarrer": {
        "definition": "Faire commencer quelque chose, surtout une machine ou un moteur.",
        "example": "Papa a démarré la voiture."
    },
    "prétendre": {
        "definition": "Dire quelque chose qui n'est peut-être pas vrai, ou faire semblant.",
        "example": "Il prétend qu'il sait voler comme un oiseau."
    },
    "criminel": {
        "definition": "Une personne qui a fait quelque chose d'interdit par la loi.",
        "example": "La police a attrapé le criminel."
    },
    "soutenir": {
        "definition": "Aider quelqu'un ou tenir quelque chose pour que ça ne tombe pas.",
        "example": "Mes amis me soutiennent quand je suis triste."
    },
    "vision": {
        "definition": "La capacité de voir avec les yeux, ou une image qu'on imagine dans sa tête.",
        "example": "L'aigle a une vision très puissante."
    },
    "malheureusement": {
        "definition": "Un mot qu'on dit quand quelque chose de triste arrive.",
        "example": "Malheureusement, il pleut et on ne peut pas sortir."
    },
    "journaliste": {
        "definition": "Une personne qui raconte les nouvelles à la télé, à la radio ou dans un journal.",
        "example": "La journaliste a posé des questions au maire."
    },
    "gloire": {
        "definition": "Être très célèbre et admiré par beaucoup de gens.",
        "example": "Le chevalier a connu la gloire après sa victoire."
    },
    "créature": {
        "definition": "Un être vivant, souvent imaginaire ou étrange.",
        "example": "Le livre raconte l'histoire d'une créature magique."
    },
    "franchement": {
        "definition": "Dire les choses honnêtement, sans mentir.",
        "example": "Franchement, je préfère le chocolat à la vanille."
    },
    "champion": {
        "definition": "La personne qui a gagné une compétition.",
        "example": "Elle est devenue championne de natation !"
    },
    "affreux": {
        "definition": "Quelque chose de très moche ou de très désagréable.",
        "example": "Il y avait un bruit affreux dehors."
    },
    "exiger": {
        "definition": "Demander quelque chose avec force, comme si c'était obligatoire.",
        "example": "Le professeur exige le silence en classe."
    },
    "inquiet": {
        "definition": "Quand tu as peur que quelque chose de mauvais arrive.",
        "example": "Maman est inquiète quand je rentre en retard."
    },
    "victoire": {
        "definition": "Quand tu gagnes un jeu, un match ou une bataille.",
        "example": "L'équipe a crié de joie après sa victoire."
    },
    "chasseur": {
        "definition": "Une personne qui cherche des animaux dans la nature pour les attraper.",
        "example": "Le chasseur marche dans la forêt."
    },
    "pistolet": {
        "definition": "Une petite arme qui tire des balles. C'est très dangereux.",
        "example": "Le policier porte un pistolet à sa ceinture."
    },
    "saigner": {
        "definition": "Quand du sang sort de ton corps parce que tu t'es blessé.",
        "example": "Mon genou saigne parce que je suis tombé."
    },
    "identité": {
        "definition": "Ce qui fait que tu es toi : ton nom, ta date de naissance, à quoi tu ressembles.",
        "example": "La carte d'identité montre qui tu es."
    },
    "vieil": {
        "definition": "Un autre mot pour dire vieux, quand on parle d'un homme.",
        "example": "Le vieil homme raconte des histoires du passé."
    },
    "national": {
        "definition": "Qui concerne tout un pays.",
        "example": "Le 14 juillet est la fête nationale en France."
    },
    "apercevoir": {
        "definition": "Voir quelque chose rapidement ou de loin.",
        "example": "J'ai aperçu un écureuil dans l'arbre."
    },
    "offre": {
        "definition": "Ce qu'on propose de donner ou de faire pour quelqu'un.",
        "example": "Le magasin a une offre spéciale sur les jouets."
    },
    "frontière": {
        "definition": "La ligne imaginaire qui sépare deux pays.",
        "example": "On a passé la frontière pour aller en Espagne."
    },
    "social": {
        "definition": "Qui a rapport avec les gens qui vivent ensemble en société.",
        "example": "Les abeilles sont des insectes très sociaux."
    },
    "réserver": {
        "definition": "Garder une place ou quelque chose pour plus tard.",
        "example": "On a réservé une table au restaurant."
    },
    "provoquer": {
        "definition": "Faire exprès d'embêter quelqu'un ou causer quelque chose.",
        "example": "Ne provoque pas ton frère, s'il te plaît."
    },
    "policier": {
        "definition": "Une personne qui protège les gens et fait respecter les lois.",
        "example": "Le policier aide les enfants à traverser la rue."
    },
    "trembler": {
        "definition": "Bouger très vite sans le vouloir parce qu'on a froid ou peur.",
        "example": "Le chiot tremblait de froid sous la pluie."
    },
    "embêter": {
        "definition": "Faire quelque chose qui dérange ou ennuie quelqu'un.",
        "example": "Arrête d'embêter ta sœur !"
    },
    "opinion": {
        "definition": "Ce que tu penses de quelque chose. Tout le monde a des opinions différentes.",
        "example": "Mon opinion, c'est que les chats sont adorables."
    },
    "confirmer": {
        "definition": "Dire que oui, c'est bien vrai.",
        "example": "La maîtresse a confirmé qu'il n'y a pas école demain."
    },
    "passion": {
        "definition": "Quelque chose qu'on aime énormément, très très fort.",
        "example": "Le dessin est sa grande passion."
    },
    "puissance": {
        "definition": "Une très grande force ou un très grand pouvoir.",
        "example": "Le lion est un animal d'une grande puissance."
    },
    "lunette": {
        "definition": "Des verres qu'on met sur le nez pour mieux voir.",
        "example": "Papi a besoin de ses lunettes pour lire."
    },
    "rare": {
        "definition": "Quelque chose qu'on ne trouve pas souvent, qui est spécial.",
        "example": "Ce papillon bleu est très rare."
    },
    "décevoir": {
        "definition": "Rendre quelqu'un triste parce que ce n'était pas aussi bien qu'il espérait.",
        "example": "Je ne veux pas décevoir mes parents."
    },
    "réagir": {
        "definition": "Faire ou dire quelque chose après qu'il s'est passé quelque chose.",
        "example": "Comment as-tu réagi quand tu as vu la surprise ?"
    },
    "haine": {
        "definition": "Un sentiment très fort quand on n'aime pas du tout quelqu'un ou quelque chose.",
        "example": "La haine, c'est un sentiment qui rend malheureux."
    },
    "enregistrer": {
        "definition": "Garder un son, une image ou une information pour pouvoir la revoir ou la réécouter.",
        "example": "On a enregistré la chanson avec un micro."
    },
    "vôtre": {
        "definition": "Un mot pour dire que quelque chose appartient à vous.",
        "example": "Ce livre est le vôtre, pas le mien."
    },
    "enfance": {
        "definition": "La période de la vie quand on est un enfant.",
        "example": "Mamie raconte des souvenirs de son enfance."
    },
    "autorité": {
        "definition": "Le pouvoir de dire aux autres ce qu'ils doivent faire.",
        "example": "Les parents ont de l'autorité sur leurs enfants."
    },
    "épée": {
        "definition": "Une grande lame en métal que les chevaliers utilisaient pour se battre.",
        "example": "Le chevalier a sorti son épée brillante."
    },
    "fixer": {
        "definition": "Attacher solidement quelque chose, ou regarder sans bouger les yeux.",
        "example": "Il fixe le tableau sans dire un mot."
    },
    "prière": {
        "definition": "Des mots qu'on dit à Dieu ou à quelqu'un de très important pour demander quelque chose.",
        "example": "Avant de dormir, elle fait sa prière."
    },
    "révéler": {
        "definition": "Dire un secret ou montrer quelque chose de caché.",
        "example": "Il a révélé la surprise avant l'heure !"
    },
    "cassette": {
        "definition": "Un petit boîtier qui contient une bande pour écouter de la musique ou regarder un film.",
        "example": "Mamie a retrouvé de vieilles cassettes au grenier."
    },
    "déménager": {
        "definition": "Quitter sa maison pour aller vivre dans une autre.",
        "example": "Mon meilleur ami va déménager dans une autre ville."
    },
    "admirer": {
        "definition": "Regarder quelque chose ou quelqu'un en trouvant ça très beau ou impressionnant.",
        "example": "On admire les étoiles dans le ciel."
    },
    "théorie": {
        "definition": "Une idée qui essaie d'expliquer comment quelque chose fonctionne.",
        "example": "Le scientifique a une théorie sur les dinosaures."
    },
    "émission": {
        "definition": "Un programme qu'on regarde à la télé ou qu'on écoute à la radio.",
        "example": "Mon émission préférée passe à 18 heures."
    },
    "promesse": {
        "definition": "Quand tu dis que tu vas faire quelque chose et que tu t'engages à le faire.",
        "example": "J'ai fait la promesse de ranger ma chambre."
    },
    "également": {
        "definition": "Un autre mot pour dire « aussi » ou « de la même façon ».",
        "example": "J'aime le chocolat et également la vanille."
    },
    "mesure": {
        "definition": "Trouver la taille ou la quantité de quelque chose avec un outil.",
        "example": "On prend la mesure du tissu avec un mètre."
    },
    "conseiller": {
        "definition": "Dire à quelqu'un ce qu'on pense qu'il devrait faire pour l'aider.",
        "example": "Je te conseille de mettre un manteau, il fait froid."
    },
    "bataille": {
        "definition": "Un grand combat entre deux groupes, comme dans les histoires de chevaliers.",
        "example": "Les soldats ont gagné la bataille."
    },
    "accueillir": {
        "definition": "Recevoir quelqu'un chez toi en étant gentil et content de le voir.",
        "example": "On a accueilli nos cousins avec un gros câlin."
    },
    "enseigner": {
        "definition": "Apprendre des choses à quelqu'un, comme le fait un professeur.",
        "example": "La maîtresse enseigne les mathématiques."
    },
    "plonger": {
        "definition": "Sauter dans l'eau la tête la première ou aller sous l'eau.",
        "example": "Elle a plongé dans la piscine."
    },
    "gardien": {
        "definition": "La personne qui surveille et protège un endroit ou quelque chose.",
        "example": "Le gardien du zoo nourrit les animaux."
    },
    "habituer": {
        "definition": "Faire quelque chose si souvent que ça devient normal et facile.",
        "example": "Le chat s'est habitué à sa nouvelle maison."
    },
    "buter": {
        "definition": "Taper son pied contre quelque chose sans le faire exprès.",
        "example": "J'ai buté contre une pierre et je suis tombé."
    },
    "explication": {
        "definition": "Ce qu'on dit pour aider quelqu'un à comprendre quelque chose.",
        "example": "La maîtresse a donné une explication très claire."
    },
    "célèbre": {
        "definition": "Quelqu'un ou quelque chose que beaucoup de gens connaissent.",
        "example": "La tour Eiffel est un monument célèbre."
    },
    "péter": {
        "definition": "Quand de l'air sort de tes fesses et ça fait du bruit.",
        "example": "Il a pété et tout le monde a rigolé."
    },
    "médical": {
        "definition": "Qui a rapport avec les docteurs et la santé.",
        "example": "L'examen médical montre que tu es en bonne santé."
    },
    "cimetière": {
        "definition": "L'endroit où on enterre les personnes qui sont mortes.",
        "example": "On va au cimetière mettre des fleurs pour papi."
    },
    "humeur": {
        "definition": "Comment tu te sens à un moment : content, triste, en colère...",
        "example": "Ce matin, je suis de bonne humeur !"
    },
}

with open("kid_defs.json", "r", encoding="utf-8") as f:
    existing = json.load(f)

existing.update(new_defs)

with open("kid_defs.json", "w", encoding="utf-8") as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print(f"Added {len(new_defs)} definitions. Total: {len(existing)}")
