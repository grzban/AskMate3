import csv
import base64
import os
import psycopg2
import psycopg2.extras
import database_common
import util


@database_common.connection_handler
def get_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = '{question_id}';
                   """.format(question_id=question_id))
    return cursor.fetchall()[0]


@database_common.connection_handler
def get_answer(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = '{answer_id}';
                   """.format(answer_id=answer_id))
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
def get_tag_to_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question_tag
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
                    VALUES {value};
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
def edit_comment(cursor, dictionary):
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

@database_common.connection_handler
def get_list_of_users(cursor):
    cursor.execute("SELECT user_name, user_reputation, registration_time FROM users;")
    return cursor.fetchall()

@database_common.connection_handler
def add_new_tag(cursor, new_tag):
    value = (new_tag['id'],
             new_tag['name'],)

    cursor.execute("""
                    INSERT INTO tag (id, name)
                    VALUES {value};
                   """.format(value=value))
