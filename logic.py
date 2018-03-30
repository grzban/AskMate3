import persistence
import database_common
import util


def make_answer(message, image, question_id, answer_id=None):
    if answer_id is None:
        id_ = generate_id(persistence.get_dicts_from_file("answer"))
    else:
        id_ = answer_id
    result = {
        'id': id_,
        'submission_time': util.decode_time_for_human(util.get_current_timestamp()),
        'vote_number': 0,
        'message': message,
        'question_id': question_id,
        'image': image
    }
    return result


def make_comment(message, question_id, comment_id=None):
    if comment_id is None:
        id_ = generate_id(persistence.get_dicts_from_file("comment"))
    else:
        id_ = comment_id
    result = {
        'id': id_,
        'submission_time': util.decode_time_for_human(util.get_current_timestamp()),
        'edited_count': 0,
        'message': message,
        'question_id': question_id,
        'answer_id': 0,
    }
    return result


def make_question(title, message, image=""):
    result = {
        'id': generate_id(persistence.get_dicts_from_file("question")),
        'submission_time': util.decode_time_for_human(util.get_current_timestamp()),
        'view_number': 0,
        'vote_number': 0,
        'title': title,
        'message': message,
        'image': image,
    }
    return result


def generate_id(table):
    ids = [int(dic.get('id')) for dic in table]
    ids.append(0)
    max_id = max(ids)
    new_id = str(max_id + 1)
    return new_id


def update_view_number(question_id, amount=1):
    question = search_question(question_id)
    views_number = int(question['view_number'])
    views_number += amount
    persistence.update('question', question_id, 'view_number', views_number)


def voting(question_id, answer_id, vote):
    if answer_id == 'None':  # if voting on question:
        questions = search_question(int(question_id))
        votes = int(questions.get('vote_number'))
        if vote == 'plus':
            votes += 1
        else:
            votes -= 1
        persistence.update('question', question_id, 'vote_number', votes)

    else:  # if voting on answer:
        answers = search_answer(int(answer_id))
        votes = int(answers.get('vote_number'))
        if vote == 'plus':
            votes += 1
        else:
            votes -= 1
        persistence.update('answer', int(answer_id), 'vote_number', votes)


# ----------------- SQL ACTION ON TABLES -------------------
@database_common.connection_handler
def delete_table(cursor, table_name, condition):
    cursor.execute("""
                    DELETE FROM {table_name}
                    WHERE {condition};
                   """.format(table_name=table_name,
                              condition=condition))


@database_common.connection_handler
def search_table(cursor, search_word):
    cursor.execute("""
                    SELECT id, title FROM question
                    WHERE title LIKE '%{search_word}%';
                   """.format(search_word=search_word))
    return cursor.fetchall()


# -------------------- SQL FUNCTIONS -----------------
@database_common.connection_handler
def get_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %s;
                   """, [question_id])
    return cursor.fetchall()[0]


@database_common.connection_handler
def get_answers_to_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id = %s;
                   """, [question_id])
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_to_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE question_id = %s;
                   """, [question_id])
    return cursor.fetchall()


@database_common.connection_handler
def last_five_questions(cursor):
    cursor.execute("""
                    SELECT id, title, message FROM question
                    ORDER BY submission_time DESC
                    LIMIT 5;
                   """)
    return cursor.fetchall()
