
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    # Validate the answer
    if answer is None or answer == "":
        return False, "Answer cannot be empty."

    # Store the answer in the Django session
    session["answers"][current_question_id] = answer
    return True, ""


def get_next_question(current_question_id):
    try:
        index = PYTHON_QUESTION_LIST.index(current_question_id)
        next_index = index + 1
        if next_index < len(PYTHON_QUESTION_LIST):
            return PYTHON_QUESTION_LIST[next_index], next_index
        else:
            return None, -1
    except ValueError:
        return None, -1


def generate_final_response(session):
    correct_answers = 0
    total_questions = len(PYTHON_QUESTION_LIST)

    for question_data in PYTHON_QUESTION_LIST:
        question_id = question_data["question"]
        correct_answer = question_data["answer"]
        user_answer = session.get("answers", {}).get(question_id, "")

        if user_answer.lower() == correct_answer.lower():
            correct_answers += 1

    score = correct_answers / total_questions * 100
    result_message = f"You answered {correct_answers} out of {total_questions} questions correctly. Your score is {score:.2f}%."
    return result_message
