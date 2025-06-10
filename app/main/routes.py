import json

from flask import render_template, request, redirect, url_for, session, current_app

from app.main.utilities import hash_password
from app.main import bp


@bp.route("/test", methods=("GET", "POST"))
def test():
    # Parameters
    current_page = "test.html"
    next_fun = "main.test"
    chara_pic = "draft_neutral"
    speech_text = [
        "dd ! Mon nom est Égide, et nous allons découvrir ensemble comment les mots de passes fonctionnent.",
        "Autre texte",
        "asdfdsaf texte",
        "af dsf",
        "Autre tdfdfexte",
    ]

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
        )
    # Next page

    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))


@bp.route("/", methods=("GET", "POST"))
@bp.route("/entry", methods=("GET", "POST"))
def entry():
    # Parameters
    current_page = "part/entry.html"
    next_fun = "main.disclaimer"
    chara_pic = "draft_neutral"
    speech_text = [
        "Salut ! Mon nom est Égide, et nous allons découvrir ensemble comment les mots de passe fonctionnent.",
        "Envie de tester votre mot de passe ?..",
    ]

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
        )
    # Next page
    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))


@bp.route("/disclaimer", methods=("GET", "POST"))
def disclaimer():
    # Parameters
    current_page = "part/disclaimer.html"
    next_fun = "main.enter_password"
    chara_pic = "draft_neutral"
    speech_text = [
        "Durant cette expérience, nous allons tenter de deviner les mots de passe que vous allez fournir.",
        "Nous allons vous expliquer comment les <i>hackers</i> et autres pirates s'y prennent pour trouver vos mots de passe.",
        "Bien entendu, ne donnez pas vos vrais mots de passe... 😉",
    ]

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
        )
    # Next page
    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))


@bp.route("/enter_password", methods=("GET", "POST"))
def enter_password():
    # Parameters
    current_page = "part/enter_password.html"
    next_fun = "main.ack_password"
    chara_pic = "draft_pointing"
    speech_text = [
        "Bien ! Commençons !",
        "Je vous propose ici de me donner trois mots de passe, un faible, un moyen, un fort.",
        "Un mot de passe faible correspond à un mot de passe qui va facilement être découvert par de méchants pirates.",
        "Un mot de passe fort ne devrait pas pouvoir facilement être deviné par des personnes malicieuses.",
        "A vous de proposer des mots de passe qui semblent coller !"
    ]

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
        )
    # Next page
    if request.method == "POST":
        session.clear()
        print(request.form)
        # weak
        plain = request.form.get("weak")
        if plain and plain != "":
            md5_hash, bcrypt_hash = hash_password(plain)
            session["weak"] = {
                "plain": plain if current_app.config["DEBUG"] else "*" * len(plain),
                "score": int(request.form.get("score_weak")),
                "md5_hash": md5_hash,
                "bcrypt_hash": bcrypt_hash,
                "time": json.loads(request.form.get("time_weak")),
            }
        # medium
        plain = request.form.get("medium")
        if plain and plain != "":
            md5_hash, bcrypt_hash = hash_password(plain)
            session["medium"] = {
                "plain": plain if current_app.config["DEBUG"] else "*" * len(plain),
                "score": int(request.form.get("score_medium")),
                "md5_hash": md5_hash,
                "bcrypt_hash": bcrypt_hash,
                "time": json.loads(request.form.get("time_medium")),
            }
        # strong
        plain = request.form.get("strong")
        if plain and plain != "":
            md5_hash, bcrypt_hash = hash_password(plain)
            session["strong"] = {
                "plain": plain if current_app.config["DEBUG"] else "*" * len(plain),
                "score": int(request.form.get("score_strong")),
                "md5_hash": md5_hash,
                "bcrypt_hash": bcrypt_hash,
                "time": json.loads(request.form.get("time_strong")),
            }

        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))


@bp.route("/ack_password", methods=("GET", "POST"))
def ack_password():
    current_page = "part/ack_password.html"
    next_fun = "main.explanation_1"
    chara_pic = "draft_neutral"
    speech_text = [
        "Merci pour les mots de passe !",
        "Nous allons pouvoir commencer l'expérience. Mais, nous n'allons pas stocker les mots de passe...",
    ]

    scores = [
        "Risqué",
        "Faible",
        "Moyen",
        "Fort",
        "Excellent"
    ]

    pass_scores = [
        session["weak"]["score"] if "weak" in session else -1,
        session["medium"]["score"] if "medium" in session else -1,
        session["strong"]["score"] if "strong" in session else -1,
    ]
    pass_scores = [s for s in pass_scores if s != -1]
    total_pass = len(pass_scores)
    pass_scores = sorted(set(pass_scores))
    diff_pass = len(pass_scores)

    match (total_pass, diff_pass):
        case (0, _):
            next_fun = "main.enter_password"
            chara_pic = "draft_meh"
            speech_text = [
                "Aucun mot de passe n'a été entré...",
                "Je vous laisse appuyer sur \"Continuer\" et réessayer."
            ]
        case (_, 1):
            speech_text.insert(
                1,
                f"Tous vos de mots de passe ont le même score, '{scores[pass_scores[0]]}'. Pourquoi pas!"
            )
        case (_, _):
            speech_text.insert(
                1,
                f"Les {total_pass} mots de passe ont un score différent, " + \
                ", ".join([f"'{scores[i]}'" for i in pass_scores]) + "."
            )

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
            weak={
                "plain": session["weak"]["plain"],
                "score": {
                    "score_percentage": int(100 * (1 + session["weak"]["score"]) / 5),
                    "score_message": scores[session["weak"]["score"]],
                },
            } if "weak" in session else {"plain": "", "score": {"score_percentage": 0, "score_message": scores[0]}},
            medium={
                "plain": session["medium"]["plain"],
                "score": {
                    "score_percentage": int(100 * (1 + session["medium"]["score"]) / 5),
                    "score_message": scores[session["medium"]["score"]],
                },
            } if "medium" in session else {"plain": "", "score": {"score_percentage": 0, "score_message": scores[0]}},
            strong={
                "plain": session["strong"]["plain"],
                "score": {
                    "score_percentage": int(100 * (1 + session["strong"]["score"]) / 5),
                    "score_message": scores[session["strong"]["score"]],
                },
            } if "strong" in session else {"plain": "", "score": {"score_percentage": 0, "score_message": scores[0]}},
        )
    # Next page
    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))


@bp.route("/explanation_1", methods=("GET", "POST"))
def explanation_1():
    # Parameters
    current_page = "part/explanation_1.html"
    next_fun = "main.explanation_2"
    chara_pic = "draft_neutral"
    speech_text = [
        "D'ailleurs, lorsque vous créez un mot de passe pour un site Internet, il n'est jamais stocké tel quel !",
        "Les sites Internet utilisent des techniques pour \"cacher\" le mot de passe, afin de ne pas le garder.",
        "L'une des méthodes les plus courantes est le hachage, qui transforme votre mot de passe en une chaîne de caractères illisible.",
    ]

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
        )
    # Next page
    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))


@bp.route("/explanation_2", methods=("GET", "POST"))
def explanation_2():
    # Parameters
    current_page = "part/explanation_2.html"
    next_fun = "main.explanation_3"
    chara_pic = "draft_neutral"
    speech_text = [
        "Le hachage est une fonction mathématique qui convertit votre mot de passe en une série de caractères fixe, appelée \"valeur de hachage\".",
        "Par exemple, même un simple mot comme <code>chat</code> devient méconnaissable après hachage, comme <code>aa8af3ebe14831a7cd1b6d1383a03755</code> (en utilisant un algorithme de hachage comme MD5).",
        "Les valeurs de hachage sont conçues pour être irréversibles, ce qui signifie qu'il est très difficile de retrouver le mot de passe original à partir de la valeur de hachage.",
        "Cette valeur de hachage est ensuite stockée dans la base de données au lieu du mot de passe en clair.",
    ]

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
        )
    # Next page
    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))


@bp.route("/explanation_3", methods=("GET", "POST"))
def explanation_3():
    # Parameters
    current_page = "part/explanation_3.html"
    next_fun = "main.explanation_4"
    chara_pic = "draft_neutral"
    speech_text = [
        "Pour ajouter une couche de sécurité supplémentaire, les sites utilisent une technique appelée \"salage\".",
        "Le salage consiste à ajouter une chaîne aléatoire unique, appelée \"sel\", à votre mot de passe avant de le hacher.",
        "Chaque utilisateur·trice a un sel différent, ce qui rend encore plus difficile la tâche des pirates informatiques pour deviner les mots de passe.",
    ]

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
        )
    # Next page
    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))


@bp.route("/explanation_4", methods=("GET", "POST"))
def explanation_4():
    # Parameters
    current_page = "part/explanation_4.html"
    next_fun = "main.explanation_5"
    chara_pic = "draft_neutral"
    speech_text = [
        "Lorsque vous vous connectez, le site hache le mot de passe que vous entrez et compare la valeur de hachage avec celle stockée dans la base de données.",
        "Si les valeurs de hachage correspondent, vous êtes authentifié·e et pouvez accéder à votre compte.",
    ]

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
        )
    # Next page
    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))


@bp.route("/explanation_5", methods=("GET", "POST"))
def explanation_5():
    # Parameters
    current_page = "part/explanation_5.html"
    next_fun = "main.explanation_6"
    chara_pic = "draft_neutral"
    speech_text = [
        "Pour cette expérience, nous allons utiliser les algorithmes de hachage MD5 et bcrypt pour stocker les mots de passe.",
        "MD5 a été largement utilisé, mais il est maintenant considéré comme peu sûr.",
        "Une attaque par collision se produit lorsque deux entrées différentes produisent la même valeur de hachage, ce qui peut compromettre la sécurité.",
        "Bcrypt, en revanche, est un algorithme de hachage plus moderne et plus sûr, spécialement conçu pour le stockage des mots de passe.",
        "Bcrypt utilise un facteur de travail, ce qui signifie qu'il peut être configuré pour être plus lent et donc plus résistant aux attaques par force brute.",
    ]

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
        )
    # Next page
    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))


@bp.route("/explanation_6", methods=("GET", "POST"))
def explanation_6():
    # Parameters
    current_page = "part/explanation_6.html"
    next_fun = "main.explanation_7"
    chara_pic = "draft_neutral"
    speech_text = [
        "XXX",
    ]

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
        )
    # Next page
    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))


@bp.route("/explanation_7", methods=("GET", "POST"))
def explanation_7():
    # Parameters
    current_page = "part/explanation_7.html"
    next_fun = "main.explanation_8"
    chara_pic = "draft_neutral"
    speech_text = [
        "XXX",
    ]

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
        )
    # Next page
    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))


@bp.route("/explanation_8", methods=("GET", "POST"))
def explanation_8():
    # Parameters
    current_page = "part/explanation_8.html"
    next_fun = "main.cracking"
    chara_pic = "draft_neutral"
    speech_text = [
        "XXX",
    ]

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
        )
    # Next page
    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))
