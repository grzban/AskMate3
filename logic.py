import persistence
import database_common
import util


def check_login_password(login, password):
    password_from_database = persistence.login_password(login)
    if password_from_database:  # not empty list:
        if password_from_database[0].get('user_password') == password:
            return 'valid'
        else:
            return 'invalid password'
    else:
        return 'registration'


def make_answer(message, image, question_id, answer_id=None):
    if answer_id is None:
        id_ = generate_id(persistence.get_ids("answer"))
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
        id_ = generate_id(persistence.get_ids("comment"))
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
        'id': generate_id(persistence.get_ids('question')),
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
    question = persistence.get_question(question_id)
    views_number = int(question['view_number'])
    views_number += amount
    persistence.update('question', question_id, 'view_number', views_number)


def voting(question_id, answer_id, vote):
    if answer_id == 'None':  # if voting on question:
        questions = persistence.get_question(question_id)
        votes = int(questions.get('vote_number'))
        votes += 1 if vote == 'plus' else -1
        persistence.update('question', question_id, 'vote_number', votes)

    else:  # if voting on answer:
        answer = persistence.get_answer(answer_id)
        votes = int(answer.get('vote_number'))
        votes += 1 if vote == 'plus' else -1
        persistence.update('answer', int(answer_id), 'vote_number', votes)
