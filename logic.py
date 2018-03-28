import persistence
import database_common
import util


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


def search_question(question_id):
    list_of_questions = persistence.get_dicts_from_file('sample_data/question.csv', 'que')
    for question in list_of_questions:
        if question['id'] == question_id:
            break
    return question


def search_list_of_answers_for_ques(question_id):
    list_of_all_answers = persistence.get_dicts_from_file('sample_data/answer.csv', 'ans')
    answers_for_ques = [answer for answer in list_of_all_answers
                        if answer['question_id'] == question_id]
    return answers_for_ques


def search_answer(answer_id):
    list_of_answers = persistence.get_dicts_from_file('sample_data/answer.csv', 'ans')
    for answer in list_of_answers:
        if answer['id'] == answer_id:
            break
    return answer


def update_view_number(question_id):
    question = search_question(question_id)
    view_number = int(question['view_number'])
    view_number += 1
    persistence.update('sample_data/question.csv', question_id, 'view_number',
                       str(view_number), persistence.QUES_HEADER, 'que')


def voting(question_id, answer_id, vote):
    if answer_id == 'None':
        ques = search_question(question_id)
        votes = int(ques.get('vote_number'))
        if vote == 'plus':
            votes += 1
        else:
            votes -= 1
        persistence.update('sample_data/question.csv', question_id, 'vote_number',
                           str(votes), persistence.QUES_HEADER, 'que')

    else:
        ans = search_answer(answer_id)
        votes = int(ans.get('vote_number'))
        if vote == 'plus':
            votes += 1
        else:
            votes -= 1
        persistence.update('sample_data/answer.csv', answer_id, 'vote_number',
                           str(votes), persistence.ANS_HEADER, 'ans')


# ----------------- ACTION ON TABLE -------------------
@database_common.connection_handler
def update_table(cursor, table_name, column_name, update_value, condition):
    cursor.execute("""
                    UPDATE {table_name}
                    SET {column_name} = '{update_value}'
                    WHERE {condition};
                   """.format(table_name=table_name,
                              column_name=column_name,
                              update_value=update_value,
                              condition=condition))


@database_common.connection_handler
def delete_table(cursor, table_name, condition):
    print(table_name)
    print(condition)
    cursor.execute("""
                    DELETE FROM {table_name}
                    WHERE id = {condition};
                   """.format(table_name=table_name,
                              condition=condition))


@database_common.connection_handler
def insert_table(cursor, table_name, columns, value):
    cursor.execute("""
                    INSERT INTO {table_name} ({columns})
                    VALUES ({value});
                   """.format(table_name=table_name,
                              columns=columns,
                              value=value))


# -------------------- SQL FUNCTIONS -----------------
@database_common.connection_handler
def get_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %s;
                   """, [question_id])
    return cursor.fetchall()


@database_common.connection_handler
def get_answers_to_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id = %s;
                   """, [question_id])
    return cursor.fetchall()


@database_common.connection_handler
def max_from(cursor, table_name, value):
    cursor.execute("""
                    SELECT * FROM {table_name}
                    WHERE {value} = (SELECT MAX({value}) FROM {table_name});
                   """.format(table_name=table_name, value=value))
    return cursor.fetchall()


@database_common.connection_handler
def edit_question(cursor, dictionary):
    cursor.execute("""
                    UPDATE question
                    SET submission_time = '{submission_time}',
                        view_number = {view_number},
                        vote_number = {vote_number},
                        title = '{title}',
                        message = '{message}',
                        image = '{image}'
                    WHERE id = {id};
                   """.format(submission_time=util.decode_time_for_human(util.get_current_timestamp()),
                              view_number=dictionary['view_number'],
                              vote_number=dictionary['vote_number'],
                              title=dictionary['title'],
                              message=dictionary['message'],
                              image=dictionary['image'],
                              id=dictionary['id']
                              ))


def delete_question():
    pass
