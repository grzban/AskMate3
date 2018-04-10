import csv
import base64
import os
import psycopg2
import psycopg2.extras
import database_common
import util


@database_common.connection_handler
def login_password(cursor, login):
    cursor.execute("""
                    SELECT user_password FROM users
                    WHERE user_name = '{login}';
                   """.format(login=login))
    return cursor.fetchall()


@database_common.connection_handler
def get_question(cursor, question_id):
    cursor.execute("""
                    SELECT q.submission_time, q.view_number, q.vote_number, q.title, q.message, u.user_name, q.image FROM question q
                    LEFT JOIN users u ON (q.user_id=u.user_id)
                    WHERE q.id = '{question_id}';
                   """.format(question_id=question_id))
    return cursor.fetchall()[0]


@database_common.connection_handler
def get_answer(cursor, answer_id):
    cursor.execute("""
                    SELECT a.*, u.user_name FROM answer a
                    LEFT JOIN users u ON (a.user_id=u.user_id)
                    WHERE id = '{answer_id}';
                   """.format(answer_id=answer_id))
    return cursor.fetchall()[0]


@database_common.connection_handler
def get_answers_to_question(cursor, question_id):
    cursor.execute("""
                    SELECT a.*, u.user_name FROM answer a
                    LEFT JOIN users u ON (a.user_id=u.user_id)
                    WHERE question_id = %s;
                   """, [question_id])
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_to_question(cursor, question_id):
    cursor.execute("""
                    SELECT c.*, u.user_name FROM comment c
                    LEFT JOIN users u ON (c.user_id=u.user_id)
                    WHERE question_id = %s;
                   """, [question_id])
    return cursor.fetchall()


@database_common.connection_handler
def few_questions(cursor, limit):
    cursor.execute("""
                    SELECT id, title, message FROM question
                    ORDER BY submission_time DESC
                    LIMIT {limit};
                   """.format(limit=limit))
    return cursor.fetchall()


@database_common.connection_handler
def delete_table(cursor, table_name, condition):
    cursor.execute("""
                    DELETE FROM {table_name}
                    WHERE {condition};
                   """.format(table_name=table_name,
                              condition=condition))


@database_common.connection_handler
def search_table(cursor, search_word):  # in SEARCH feature
    cursor.execute("""
                    SELECT id, title FROM question
                    WHERE title LIKE '%{search_word}%';
                   """.format(search_word=search_word))
    return cursor.fetchall()


@database_common.connection_handler
def get_ids(cursor, table):
    query = """SELECT id FROM {};""".format(table)
    cursor.execute(query)
    table = cursor.fetchall()
    return table


@database_common.connection_handler
def get_list_of_questions(cursor):
    cursor.execute("SELECT * FROM question;")
    return cursor.fetchall()


@database_common.connection_handler
def update(cursor, table, id_row, column, new_value):
    query = """UPDATE {}
              SET {}='{}'
              WHERE id = '{}';""".format(table, column, new_value, id_row)
    cursor.execute(query)


@database_common.connection_handler
def add_new_question(cursor, new_question):
    value = (new_question['id'],
             new_question['submission_time'],
             new_question['view_number'],
             new_question['vote_number'],
             new_question['title'],
             new_question['message'],
             new_question['image'])
    cursor.execute("""
                    INSERT INTO question
                    VALUES({value});
                   """.format(value=value))


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


@database_common.connection_handler
def add_new_answer(cursor, new_answer):
    value = (new_answer['id'],
             new_answer['submission_time'],
             new_answer['vote_number'],
             new_answer['question_id'],
             new_answer['message'],
             new_answer['image'])
    cursor.execute("""
                    INSERT INTO answer
                    VALUES {value};
                   """.format(value=value))


@database_common.connection_handler
def add_new_comment(cursor, new_comment):
    value = (new_comment['id'],
             new_comment['message'],
             new_comment['submission_time'],
             new_comment['edited_count'],
             new_comment['question_id'],)

    cursor.execute("""
                    INSERT INTO comment (id, message, submission_time, edited_count, question_id)
                    VALUES {value};
                   """.format(value=value))


@database_common.connection_handler
def edit_answer(cursor, dictionary):
    cursor.execute("""
                    UPDATE answer
                    SET submission_time = '{submission_time}',
                        vote_number = {vote_number},
                        message = '{message}',
                        image = '{image}'
                    WHERE question_id = {question_id} AND id = {id};
                   """.format(submission_time=dictionary['submission_time'],
                              vote_number=dictionary['vote_number'],
                              message=dictionary['message'],
                              image=dictionary['image'],
                              question_id=dictionary['question_id'],
                              id=dictionary['id']
                              ))


@database_common.connection_handler
def edit_coment(cursor, dictionary):
    cursor.execute("""
                    UPDATE comment
                    SET submission_time = '{submission_time}',
                        vote_number = {vote_number},
                        message = '{message}',
                        image = '{image}'
                    WHERE question_id = {question_id} AND id = {id};
                   """.format(submission_time=dictionary['submission_time'],
                              vote_number=dictionary['vote_number'],
                              message=dictionary['message'],
                              question_id=dictionary['question_id'],
                              id=dictionary['id']
                              ))


# user
def get_user_query(user_id):
    return "SELECT * FROM users WHERE user_id = " + str(user_id)


@database_common.connection_handler
def get_user(cursor, user_id):
    cursor.execute(get_user_query(user_id))


def add_user_query(user):
    user_column = []
    user_data = []
    for key, value in user.items():
        user_column.append(str(key))
        user_data.append('\'' + str(value) + '\'')
    print((user_column, user_data))
    return 'INSERT INTO users (' + ', '.join(user_column) + ') values (' + ', '.join(user_data) + ');'


@database_common.connection_handler
def add_user(cursor, user):
    cursor.execute(add_user_query(user))


# user = {
#     'user_name': 'GB',
#     'user_password': 'password',
#     'user_reputation': 10
#     }

