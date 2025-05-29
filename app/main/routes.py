from flask import render_template, request, redirect, url_for

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
    next_fun = "main.hash"
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
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))
