import threading
import json

from flask import render_template, request, redirect, url_for, session, current_app

from app.main.utilities import hash_password, ssh_hashcat_from_hashes, ssh_send_command
from app.main import bp

SCORES_TEXT = [
    "Risqué",
    "Faible",
    "Moyen",
    "Fort",
    "Excellent"
]


@bp.route("/test", methods=("GET", "POST"))
def test():
    # Parameters
    current_page = "test.html"
    next_fun = "main.test"
    chara_pic = "draft_neutral"
    speech_text = [
        "Bonjour ! Mon nom est Égide, et nous allons découvrir ensemble comment les mots de passes fonctionnent.",
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
    chara_pic = "draft_wink"
    speech_text = [
        "Durant cette expérience, nous allons tenter de deviner les mots de passe que vous allez fournir.",
        "Nous allons vous expliquer comment les <i>hackers</i> et autres pirates s'y prennent pour trouver vos mots de passe.",
        "Bien entendu, ne donnez pas vos vrais mots de passe...",
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
        # "Un mot de passe faible correspond à un mot de passe qui va facilement être découvert par de méchants pirates.",
        # "Un mot de passe fort ne devrait pas pouvoir facilement être deviné par des personnes malicieuses.",
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
                "plain": plain,
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
                "plain": plain,
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
                "plain": plain,
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
                f"Tous vos de mots de passe ont le même score, '{SCORES_TEXT[pass_scores[0]]}'. Pourquoi pas !"
            )
        case (_, _):
            speech_text.insert(
                1,
                f"Les {total_pass} mots de passe ont un score différent, " + \
                ", ".join([f"'{SCORES_TEXT[i]}'" for i in pass_scores]) + "."
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
                    "score_message": SCORES_TEXT[session["weak"]["score"]],
                },
            } if "weak" in session else {"plain": "",
                                         "score": {"score_percentage": 0, "score_message": SCORES_TEXT[0]}},
            medium={
                "plain": session["medium"]["plain"],
                "score": {
                    "score_percentage": int(100 * (1 + session["medium"]["score"]) / 5),
                    "score_message": SCORES_TEXT[session["medium"]["score"]],
                },
            } if "medium" in session else {"plain": "",
                                           "score": {"score_percentage": 0, "score_message": SCORES_TEXT[0]}},
            strong={
                "plain": session["strong"]["plain"],
                "score": {
                    "score_percentage": int(100 * (1 + session["strong"]["score"]) / 5),
                    "score_message": SCORES_TEXT[session["strong"]["score"]],
                },
            } if "strong" in session else {"plain": "",
                                           "score": {"score_percentage": 0, "score_message": SCORES_TEXT[0]}},
        )
    # Next page
    if request.method == "POST":
        if next_fun != "main.enter_password":  # Check that passwords
            # We deletin' just for the beauty of it...
            hashes = list()
            if "weak" in session:
                del session["weak"]["plain"]
                hashes.append(session["weak"]["md5_hash"])
            if "medium" in session:
                del session["medium"]["plain"]
                hashes.append(session["medium"]["md5_hash"])
            if "strong" in session:
                del session["strong"]["plain"]
                hashes.append(session["strong"]["md5_hash"])
            hashes = '\n'.join(hashes)

            # Send password for cracking
            command = fr"printf '{hashes}' > /users/username/hashcat_test/hashcat-6.2.6/current_hash"
            print(command)
            test = ssh_send_command(command, "curnagl.dcsr.unil.ch", "username")
            try:
                stdout = test["stdout"]
                print(stdout)
                stderr = test["stderr"]
                print(stderr)
            except TimeoutError:
                pass

            def fun_fun_2():
                command = 'srun -c 8 --mem 32G --partition gpu-l40 --reservation=password_day --gres gpu:8 bash -c "module load cuda hashcat;hashcat --force -O -w 4 --opencl-device-types 1,2 -m 0 -a 0 /users/username/hashcat_test/hashcat-6.2.6/current_hash /reference/weakpass/weakpass_4.txt -r /users/username/hashcat_test/hashcat-6.2.6/rules/OneRuleToRuleThemAll.rule"'
                print(command)
                test = ssh_send_command(command, "curnagl.dcsr.unil.ch", "username")
                try:
                    stdout = test["stdout"]
                    print(stdout)
                    stderr = test["stderr"]
                    print(stderr)
                except TimeoutError:
                    pass

            fun_thread = threading.Thread(target=fun_fun_2, name="do stuff")
            fun_thread.start()

        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))


@bp.route("/explanation_1", methods=("GET", "POST"))
def explanation_1():
    # Parameters
    current_page = "part/explanation.html"
    next_fun = "main.explanation_2"
    chara_pic = "draft_pointing"
    speech_text = [
        "D'ailleurs, lorsque vous créez un mot de passe pour un site Internet, il n'est jamais stocké tel quel !",
        "Les sites Internet utilisent des techniques pour \"cacher\" le mot de passe, afin de ne pas le garder.",
    ]

    illu_pic = "no_stock.png"
    illu_source = None

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
            illu_pic=illu_pic,
            illu_source=illu_source,
        )
    # Next page
    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))


@bp.route("/explanation_2", methods=("GET", "POST"))
def explanation_2():
    # Parameters
    current_page = "part/explanation.html"
    next_fun = "main.explanation_3"
    chara_pic = "draft_neutral"
    speech_text = [
        "L'une des méthodes les plus courantes est le hachage !",
        "Le hachage est une fonction mathématique qui convertit votre mot de passe en une série de caractères fixe, appelée \"<i>hash</i>\", ou \"valeur de hachage\" en français.",
    ]

    illu_pic = "maths.png"
    illu_source = None

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
            illu_pic=illu_pic,
            illu_source=illu_source,
        )
    # Next page
    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))


@bp.route("/explanation_3", methods=("GET", "POST"))
def explanation_3():
    # Parameters
    current_page = "part/explanation.html"
    next_fun = "main.explanation_4"
    chara_pic = "draft_neutral"
    speech_text = [
        "Cette suite de caractères ne permet pas de deviner le mot d'origine.",
        "Un mot comme <code>chat</code> se transforme en<br/><small><code>aa8af3ebe14831a7cd1b6d1383a03755</code></small><br/>par exemple !",
        "Les <i>hashes</i> sont conçus pour être irréversibles.",
    ]

    illu_pic = "1way.png"
    illu_source = None

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
            illu_pic=illu_pic,
            illu_source=illu_source,
        )
    # Next page
    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))


@bp.route("/explanation_4", methods=("GET", "POST"))
def explanation_4():
    # Parameters
    current_page = "part/explanation.html"
    next_fun = "main.explanation_5"
    chara_pic = "draft_pointing"
    speech_text = [
        "Ce <i>hash</i> est ensuite stockée dans la base de données au lieu du mot de passe.",
        "Lorsque vous vous connectez, le site hache le mot de passe que vous entrez et compare le <i>hash</i> avec celui stocké.",
        "Si les valeurs correspondent, <i>you're in!</i>",
    ]

    illu_pic = "compar.png"
    illu_source = None

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
            illu_pic=illu_pic,
            illu_source=illu_source,
        )
    # Next page
    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))


@bp.route("/explanation_5", methods=("GET", "POST"))
def explanation_5():
    # Parameters
    current_page = "part/explanation.html"
    next_fun = "main.explanation_6"
    chara_pic = "draft_neutral"
    speech_text = [
        # "Pour cette expérience, nous allons utiliser les algorithmes de hachage MD5 et bcrypt pour stocker les mots de passe.",
        "Pour cette expérience, nous allons utiliser l'algorithme de hachage MD5 - mais il en existe bien d'autres !",
    ]

    illu_pic = "list_hashes.png"
    illu_source = "List of hash functions <i>via</i> Wikipédia"

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
            illu_pic=illu_pic,
            illu_source=illu_source,
        )
    # Next page
    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))


@bp.route("/explanation_6", methods=("GET", "POST"))
def explanation_6():
    # Parameters
    current_page = "part/explanation.html"
    next_fun = "main.explanation_7"
    chara_pic = "draft_hack"
    speech_text = [
        "MD5 a été largement utilisé, mais il est maintenant considéré comme peu sûr, en raison des \"attaques par collision\".",
        "Une attaque par collision se produit lorsque deux entrées différentes produisent la même valeur de hachage, ce qui peut compromettre la sécurité.",
    ]

    illu_pic = "coll.png"
    illu_source = None

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
            illu_pic=illu_pic,
            illu_source=illu_source,
        )
    # Next page
    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))


@bp.route("/explanation_7", methods=("GET", "POST"))
def explanation_7():
    # Parameters
    current_page = "part/explanation.html"
    next_fun = "main.explanation_8"
    chara_pic = "draft_neutral"
    speech_text = [
        "Un autre exemple, Bcrypt, est un algorithme de hachage plus moderne et plus sûr, spécialement conçu pour le stockage des mots de passe.",
        "Bcrypt utilise un \"facteur de travail\", ce qui signifie qu'il peut être configuré pour être plus lent et donc plus résistant aux attaques par force brute.",
    ]

    illu_pic = "bcrypt.png"
    illu_source = None

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
            illu_pic=illu_pic,
            illu_source=illu_source,
        )
    # Next page
    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))


@bp.route("/explanation_8", methods=("GET", "POST"))
def explanation_8():
    # Parameters
    current_page = "part/explanation.html"
    next_fun = "main.crack_1"
    chara_pic = "draft_wink"
    speech_text = [
        "Assez discuté théorie, passons à la pratique !",
        "Nous allons maintenant tenter de casser les mots de passe..."
    ]

    illu_pic = "clap-excited.gif"
    illu_source = "Seven Bucks Productions <i>via</i> tenor.com"

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
            illu_pic=illu_pic,
            illu_source=illu_source,
        )
    # Next page
    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))


@bp.route("/crack", methods=("GET", "POST"))
@bp.route("/crack_1", methods=("GET", "POST"))
def crack_1():
    # Parameters
    current_page = "part/crack.html"
    next_fun = "main.crack_2"
    chara_pic = "draft_pointing"
    speech_text = [
        "Voici les <i>hashes</i> des mots de passe données au début ! Comme promis, nous n'avons pas gardé les originaux.",
        "Nous allons envoyer ces <i>hashes</i> sur des ordinateurs très puissants, pour tenter de les craquer...",
    ]

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
            weak_md5=session["weak"]["md5_hash"] if "weak" in session else "",
            medium_md5=session["medium"]["md5_hash"] if "medium" in session else "",
            strong_md5=session["strong"]["md5_hash"] if "strong" in session else "",
        )
    # Next page
    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))

@bp.route("/get_results")
def get_results():
    try:
        hashes = request.args.get("hashes").split(",")
    except:
        return {}

    return ssh_hashcat_from_hashes(hashes)

@bp.route("/crack_2", methods=("GET", "POST"))
def crack_2():
    # Parameters
    current_page = "part/oz.html"
    next_fun = "main.advices"
    chara_pic = "draft_hack"
    speech_text = [
        "Et c'est parti...",
        "On va essayer...",
        "... De craquer tout ça...",
        "...",
        "Maximum pendant soixante secondes...",
        "...",
    ]

    # Current page
    if request.method == "GET":
        return render_template(
            current_page,
            chara_pic=chara_pic,
            speech_text=speech_text,
            weak_md5=session["weak"]["md5_hash"] if "weak" in session else "",
            medium_md5=session["medium"]["md5_hash"] if "medium" in session else "",
            strong_md5=session["strong"]["md5_hash"] if "strong" in session else "",
        )
    # Next page
    if request.method == "POST":
        return redirect(url_for(next_fun))

    # Error
    return redirect(url_for("main.entry"))

@bp.route("/results", methods=("GET", "POST"))
def results():
    # Parameters
    current_page = "part/results.html"
    next_fun = "main.advices"
    chara_pic = "draft_neutral"
    speech_text = [
        "Blabla sur les résultats.",
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

@bp.route("/advices", methods=("GET", "POST"))
def advices():
    # Parameters
    current_page = "part/advices.html"
    next_fun = "main.entry"
    chara_pic = "draft_pointing"
    speech_text = [
        "Merci d'avoir participé à cette expérience avec moi !",
        "On se laisse sur quelques conseils pour de meilleurs mots de passe...",
        "Bonne suite, et <i>stay safe</i>!",
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
