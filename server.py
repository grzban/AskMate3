import persistence
import logic
import time

from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__, static_url_path='/static')


# -------------- INDEX ---------------
@app.route('/')
def index():
    lastes_question = logic.max_from("question", "submission_time")
    most_viewed_question = logic.max_from("question", "view_number")
    most_voted_question = logic.max_from("question", "vote_number")

    return render_template('index.html',
                           lastes_question=lastes_question,
                           most_viewed_question=most_viewed_question,
                           most_voted_question=most_voted_question)


# -------------- QUESTIONS ----------------
@app.route('/questions', methods=['GET', 'POST'])
def questions():
    list_of_questions = persistence.get_dicts_from_file("question")

    return render_template('list.html', list_of_questions=list_of_questions)


@app.route('/questions/<int:question_id>', methods=['GET'])
def delete_question(question_id):
    logic.delete_table('question', question_id)

    return redirect('/questions')


@app.route('/new_question', methods=['POST', 'GET'])
def new_question():

    return render_template('newQuestion.html')


@app.route('/question/edit/<question_id>', methods=['POST', 'GET'])
def edit_question(question_id):
    question = logic.get_question(question_id)

    return render_template('newQuestion.html', question=question[0])


@app.route('/question/<question_id>')
def show_question(question_id):
    question = logic.get_question(question_id)
    anserws = logic.get_answers_to_question(question_id)

    return render_template('question.html',
                           question=question,
                           anserws=anserws)


@app.route('/data_handler', methods=['POST', 'GET'])
def data_handler():
    if 'id' in request.form:
        question = logic.edit_question(request.form)
    else:
        question = logic.make_question(request.form['title'],
                                       request.form['message'],
                                       request.form['image'])
        persistence.add_new_question(question)

    return redirect(url_for('questions'))


@app.route('/tags')
def tags():
    return render_template('tags.html')

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
