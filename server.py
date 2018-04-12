import persistence
import logic
import time

from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__, static_url_path='/static')


# -------------- INDEX --------------
@app.route('/', methods=['GET', 'POST'])
def index():
    lastes_questions = persistence.few_questions(5)

    return render_template('index.html', lastes_questions=lastes_questions,)


@app.route('/signined', methods=['POST'])
def signined():
    user_name = request.form.get('user_name')
    user_password = request.form.get('user_password')


    return redirect(url_for('index'))


# -------------- QUESTIONS ----------
@app.route('/data_handler', methods=['POST'])
def data_handler():
    if 'id' in request.form:  # edit mode
        check = logic.check_login_password(request.form.get('login'),
                                      request.form.get('password'),
                                      request.form.get('id'))
        if type(check)  == int:
            persistence.edit_question(request.form)
            # here must clear session!!!
            return redirect(url_for('questions'))
        else:
            return redirect(url_for('edit_question', question_id=request.form.get('id')))

    else:  # new post
        check = logic.check_login_password(request.form.get('login'),
                                      request.form.get('password'))
        if type(check)  == int:
            question = logic.make_question(request.form['title'],
                                       request.form['message'],
                                       check,
                                       request.form['image'])
            persistence.add_new_question(question)
            # here must clear session!!!!
            return redirect(url_for('questions'))
        else:
            print(request.form.get('title') + ' ' + check + ' OOOOOOOOOO')
            session['login'] = request.form['login']
            session['title'] = request.form['title']
            session['message'] = request.form['message']
            session['image'] = request.form['image']
            return redirect(url_for('new_question', info_for_user=check))


@app.route('/questions', methods=['GET', 'POST'])
def questions():
    list_of_questions = persistence.get_list_of_questions()
    return render_template('list.html', list_of_questions=list_of_questions)


@app.route('/questions/<int:question_id>', methods=['GET'])
def delete_question(question_id):
    persistence.delete_table('question', 'id = {question_id}'.format(question_id=question_id))
    logic.update_view_number(question_id, -1)

    return redirect('/questions')


@app.route('/new_question/<info_for_user>', methods=['POST', 'GET'])
def new_question(info_for_user='log in'):
    if 'title' in session:
        print('session!!!')
        print(session)
        login = session.get('login')
        title = session.get('title')
        message_text = session.get('message')
        image = session.get('image')
        print(message_text)
        print(info_for_user)
        return render_template('newQuestion.html', login=login,
                                                   title=title,
                                                   message_text=message_text,
                                                   image=image,
                                                   info=info_for_user)
    else:
        print('no session!!!!')
        return render_template('newQuestion.html')


@app.route('/question/edit/<question_id>', methods=['POST', 'GET'])
def edit_question(question_id):
    question = persistence.get_question(question_id)

    return render_template('newQuestion.html', question=question)


@app.route('/question/<question_id>', methods=['POST', 'GET'])
def show_question(question_id, answer_id=None, comment_id=None):
    #answer_id = request.args.get("answer_id")
    #comment_id = request.args.get("comment_id")
    questions = persistence.get_question_by_id(question_id)
    answers = persistence.get_answers_to_question(question_id)
    comments = persistence.get_comment_to_question(question_id)
    tags = persistence.get_tag_to_question(question_id)
    users = persistence.get_all_users()
    logic.update_view_number(question_id)
    
    return render_template('question.html',
                           questions=questions,
                           answers=answers,
                           comments=comments,
                           tags=tags,
                           users=users,
                           question_id=question_id)


@app.route('/question/<question_id>/<answer_id>/<vote>', methods=["POST"])
@app.route('/question/<question_id>/<vote>', methods=["POST"])
def vote(question_id, vote, answer_id=None):
    logic.voting(question_id, vote, answer_id, )
    logic.update_view_number(int(question_id), -1)
    return redirect('/question/{}'.format(question_id))


# -------------- ANSWERS ----------
@app.route('/question/<int:question_id>/new_answer', methods=['POST', 'GET'])
def post_answer(question_id):
    new_answer = logic.make_answer(request.form['message'],
                                   request.form['image'],
                                   question_id)
    persistence.add_new_answer(new_answer)
    return redirect(url_for('show_question', question_id=question_id))


@app.route('/question/<int:question_id>/edit_answer/<int:answer_id>', methods=['POST', 'GET'])
def edit_answer(question_id, answer_id):
    new_answer = logic.make_answer(request.form['message'],
                                   request.form['image'],
                                   question_id,
                                   answer_id)
    persistence.edit_answer(new_answer)
    return redirect(url_for('show_question', question_id=question_id))


@app.route('/delete_answer', methods=['GET'])
def delete_answer():
    persistence.delete_table('answer', 'id = {answer_id}'.format(answer_id=request.args.get("answer_id")))

    return redirect(url_for('show_question', question_id=request.args.get("question_id")))


# -------------- TAGS -------------
@app.route('/tags')
def tags():
    tags = persistence.get_all_tag()
    return render_template('tags.html', tags=tags)

@app.route('/question/<int:question_id>/new_tag', methods=['POST', 'GET'])
def post_tag(question_id):
    new_tag = logic.make_tag(request.form['name'])
    id_new_tag=new_tag['id']
    new_tag_id = logic.make_tag_id(question_id, id_new_tag)


    persistence.add_new_tag(new_tag)
    persistence.add_new_tags(new_tag_id)

    return redirect(url_for('show_question', question_id=question_id))

@app.route('/selected_tag/<name>', methods=['GET', 'POST'])
def select(name):
    list_of_titles = persistence.search_table_by_tag(name)
    print(list_of_titles)

    return render_template('selected_tag.html', list_of_titles=list_of_titles)


# -------------- SEARCH -----------
@app.route('/search', methods=['GET', 'POST'])
def search():
    list_of_titles = persistence.search_table(request.form['word'])

    return render_template('search.html', list_of_titles=list_of_titles)


# -------------- COMMENTS ---------
@app.route('/question/<int:question_id>/new_comment', methods=['POST', 'GET'])
def post_comment(question_id):
    new_comment = logic.make_comment(request.form['message'],
                                     question_id)
    persistence.add_new_comment(new_comment)
    return redirect(url_for('show_question', question_id=question_id))


@app.route('/question/<int:question_id>/edit-comment/<int:comment_id>', methods=['POST', 'GET'])
def edit_coment(question_id, coment_id):
    new_comment = logic.make_comment(request.form['message'],
                                     question_id)
    persistence.edit_coment(new_comment)
    return redirect(url_for('show_question', question_id=question_id))


# -------------- USERS -------------
@app.route('/signin/')
@app.route('/signin/<alert_for_user>')
def signin(alert_for_user=None):
    return render_template('signin.html', alert_for_user=alert_for_user)


@app.route('/signin/check', methods=['POST'])
def check_user():
    login = request.form.get('user_name')
    password = request.form.get('user_password')
    validate = logic.check_sign_in(login, password)
    if type(validate) == str:
        return redirect(url_for('signin', alert_for_user=validate))
    else:
        session['user_id'] = validate['user_id']
        session['user_name'] = validate['user_name']
        print('USER ID from session : ' + str(session['user_id']))

    return redirect(url_for('index'))


@app.route('/logout/')
def logout():
    if 'user_id' in session:
        del session['user_id']
    if 'user_name' in session:
        del session['user_name']
    return redirect(url_for('index'))


@app.route('/users')
def users():
    list_of_users = persistence.get_list_of_users()
    return render_template('users.html', list_of_users=list_of_users)


@app.route('/registration')
def registration():
    return render_template('registration.html')


@app.route('/registration/add', methods=['POST'])
def add_user():
    new_user = {
        'user_name': request.form.get('user_name'),
        'user_password': request.form.get('user_password'),
        'user_reputation': 0
    }
    persistence.add_user(new_user)
    return redirect(url_for('index'))


@app.route('/user/<user_id>', methods=['POST', 'GET'])
def show_user(user_id):
    user = persistence.get_user(user_id)
    return render_template('user.html', user=user)


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
