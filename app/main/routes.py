from flask import render_template, request, redirect, url_for

from app.main import bp


@bp.route("/test", methods=("GET", "POST"))
def test():
    # Parameters
    current_page = "test.html"
    next_fun = "main.test"
    chara_pic = "draft_neutral"
    speech_text = "En train de faire des tests en fait"

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
def entry():
    # Parameters
    current_page = "entry.html"
    next_fun = "main.test"
    chara_pic = "draft_neutral"
    speech_text = ""

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
