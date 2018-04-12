import persistence
import database_common
import util


def check_login_password(login, password, qa_id=None):
    password_from_database = persistence.login_password(login)
    if password_from_database:  # not empty list - login is in database:
        print("is login")
        if password_from_database[0].get('user_password') == password:  # if password is correct
            print("ok pass")
            if qa_id:  # if it's edit mode :
                if persistence.permission_for_edit('question', qa_id, login):  # if user is editing his question\ans\com
                    print("permission ok")
                    return persistence.get_user_id(login)
                else:
                    return 'Its not your question'
            else:  # creating new post:
                print('new post')
            return persistence.get_user_id(login)
        else:
            print('password not')
            return 'Incorrect password'
    else:
        print('Go to registration')
        return 'There is no user by given login. Create your account or correctly type your login.'


def check_sign_in(login, password):
    password_from_database = persistence.get_user_by_name(login)
    if password_from_database:  # not empty list - login is in database:
        if password_from_database[0].get('user_password') == password:  # if password is correct
            return persistence.get_user_by_name(login)[0]
        else:
            return 'Incorrect password'
    else:
        return 'There is no user by given login. Create new account or correctly type your login.'


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


def make_question(title, message, user_id, image=""):
    result = {
        'id': generate_id(persistence.get_ids('question')),
        'submission_time': util.decode_time_for_human(util.get_current_timestamp()),
        'view_number': 0,
        'vote_number': 0,
        'title': title,
        'message': message,
        'image': image,
        'user_id': user_id,
    }
    return result

def make_tag(name, tag_id=None):
    if tag_id is None:
        id_ = generate_id(persistence.get_ids("tag"))
    else:
        id_ = tag_id
    result = {
        'id':id_,
        'name': name,
    }
    return result

def make_tag_id(question_id, id_new_tag):
    result = {
        'question_id':question_id,
        'tag_id': id_new_tag,
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
    views_number = int(question[0]['view_number'])
    views_number += int(amount)
    persistence.update('question', question_id, 'view_number', views_number)


def voting(question_id, vote, answer_id):
    if answer_id == None:  # if voting on question:
        questions = persistence.get_question_by_id(question_id)[0]
        user_id = questions.get('user_id')
        votes = int(questions.get('vote_number'))
        votes += 1 if vote == 'plus' else -1
        if user_id is None:
            print("user does not exist")
        else:
            user = persistence.get_user(user_id)[0]
            user_reputation = int(persistence.get_reputation(user_id).get('user_reputation'))
            user_reputation = change_user_reputation(user_reputation, 'question', vote)
            persistence.update_user_reputation('users', user_id, 'user_reputation', user_reputation)
        persistence.update('question', question_id, 'vote_number', votes)
    else:  # if voting on answer:
        answer = persistence.get_answer(answer_id)
        user_id = answer.get('user_id')
        votes = int(answer.get('vote_number'))
        votes += 1 if vote == 'plus' else -1
        if user_id is None:
            print("user does not exist")
        else:
            user = persistence.get_user(user_id)[0]
            user_reputation = int(persistence.get_reputation(user_id).get('user_reputation'))
            user_reputation = change_user_reputation(user_reputation, 'answer', vote)
            persistence.update_user_reputation('users', user_id, 'user_reputation', user_reputation)
        persistence.update('answer', int(answer_id), 'vote_number', votes)


def change_user_reputation(user_reputation, event, kind_of_vote):
    if kind_of_vote == 'plus':
        if event == 'question':
            user_reputation += 5
        else:
            user_reputation += 10
    else:
        user_reputation -= 2
    return user_reputation
