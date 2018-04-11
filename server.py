import persistence
import logic
import time

from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__, static_url_path='/static')


# -------------- INDEX --------------
@app.route('/')
def index():
    lastes_questions = persistence.last_five_questions()

    return render_template('index.html', lastes_questions=lastes_questions,)


# -------------- QUESTIONS ----------
@app.route('/questions', methods=['GET', 'POST'])
def questions():
    list_of_questions = persistence.get_list_of_questions()
    return render_template('list.html', list_of_questions=list_of_questions)


@app.route('/questions/<int:question_id>', methods=['GET'])
def delete_question(question_id):
    persistence.delete_table('question', 'id = {question_id}'.format(question_id=question_id))
    logic.update_view_number(question_id, -1)

    return redirect('/questions')


@app.route('/new_question', methods=['POST', 'GET'])
def new_question():

    return render_template('newQuestion.html')


@app.route('/question/edit/<question_id>', methods=['POST', 'GET'])
def edit_question(question_id):
    question = persistence.get_question(question_id)

    return render_template('newQuestion.html', question=question)


@app.route('/question/<question_id>', methods=['POST', 'GET'])
def show_question(question_id, answer_id=None, comment_id=None):
    answer_id = request.args.get("answer_id")
    comment_id = request.args.get("comment_id")
    question = persistence.get_question(question_id)
    answers = persistence.get_answers_to_question(question_id)
    comment = persistence.get_comment_to_question(question_id)
    tags = persistence.get_tag_to_question(question_id)
    logic.update_view_number(question_id)

    return render_template('question.html',
                           question=question,
                           answers=answers,
                           comment=comment,
                           tags=tags,
                           question_id=question_id,
                           answer_id=answer_id,
                           comment_id=comment_id)


@app.route('/data_handler', methods=['POST', 'GET'])
def data_handler():
    if 'id' in request.form:
        persistence.edit_question(request.form)
    else:
        question = logic.make_question(request.form['title'],
                                       request.form['message'],
                                       request.form['image'])
        persistence.add_new_question(question)

    return redirect(url_for('questions'))


@app.route('/question/<question_id>/<answer_id>/<vote>', methods=["POST"])
def vote(question_id, answer_id, vote):
    logic.voting(question_id, answer_id, vote)
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
    print(list_of_titles)
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
@app.route('/users')
def users():
    list_of_users = persistence.get_list_of_users()
    return render_template('users.html', list_of_users=list_of_users)



if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
