import persistence
import logic
import time

from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__, static_url_path='/static')


# -------------- INDEX ---------------
@app.route('/')
def index():
    lastes_questions = logic.last_five_questions()

    return render_template('index.html', lastes_questions=lastes_questions,)


# -------------- QUESTIONS -----------
@app.route('/questions', methods=['GET', 'POST'])
def questions():
    list_of_questions = persistence.get_dicts_from_file("question")

    return render_template('list.html', list_of_questions=list_of_questions)


@app.route('/questions/<int:question_id>', methods=['GET'])
def delete_question(question_id):
    logic.delete_table('question', 'id = {question_id}'.format(question_id=question_id))

    return redirect('/questions')


@app.route('/new_question', methods=['POST', 'GET'])
def new_question():

    return render_template('newQuestion.html')


@app.route('/question/edit/<question_id>', methods=['POST', 'GET'])
def edit_question(question_id):
    question = logic.get_question(question_id)

    return render_template('newQuestion.html', question=question)


@app.route('/question/<question_id>', methods=['POST', 'GET'])
def show_question(question_id, answer_id=None):
    answer_id = request.args.get("answer_id")
    question = logic.get_question(question_id)
    answers = logic.get_answers_to_question(question_id)

    return render_template('question.html',
                           question=question,
                           answers=answers,
                           question_id=question_id,
                           answer_id=answer_id)


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


# -------------- ANSWERS -----------
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
    logic.delete_table('answer', 'id = {answer_id}'.format(answer_id=request.args.get("answer_id")))

    return redirect(url_for('show_question', question_id=request.args.get("question_id")))


@app.route('/tags')
def tags():
    return render_template('tags.html')


# -------------- SEARCH -----------
@app.route('/search', methods=['GET', 'POST'])
def search():
    list_of_titles = logic.search_table(request.form['word'])

    return render_template('search.html', list_of_titles=list_of_titles)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
