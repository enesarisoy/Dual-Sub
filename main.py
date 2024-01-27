from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
texts = []  # Bu liste, gönderilen metinleri depolamak için kullanılacak
client = MongoClient(
    'mongodb+srv://arisoyeness:arisoyeness@pot.wd76axd.mongodb.net/?retryWrites=true&w=majority')  # MongoDB bağlantı adresini ayarlayın
db = client['words']  # Veritabanınızın adını ayarlayın
collection = db['texts']  # Kullanacağınız koleksiyonun adını ayarlayın


@app.route('/post_text/<username>', methods=['POST', 'GET'])
def post_text(username):
    user_collection = db[username]
    if request.method == 'POST':
        data = request.get_json()
        new_text = data.get('text')

        if new_text:
            user_collection.insert_one({'text': new_text})
            return jsonify({'message': 'Text added successfully'})
        else:
            return jsonify({'error': 'Text not provided'}), 400

    elif request.method == 'GET':
        new_text = request.args.get('text').capitalize()

        if new_text:
            user_collection.insert_one({'text': new_text})
            return jsonify({'message': 'Text added successfully'})
        else:
            return jsonify({'error': 'Text not provided'}), 400


@app.route('/get_texts/<username>', methods=['GET'])
def get_texts(username):
    user_collection = db[username]
    texts_from_db = list(user_collection.find())  # Tüm verileri MongoDB'den al ve liste olarak tut

    # Create a list of unique texts based on the 'text' field
    unique_texts = []
    seen_texts = set()
    for text_dict in texts_from_db:
        current_text = text_dict.get('text')
        if current_text not in seen_texts:
            unique_texts.append(text_dict)
            seen_texts.add(current_text)

    # Combine the unique texts into the desired format
    all_texts = []
    i = 0
    while i < len(unique_texts) - 1:
        current_text = unique_texts[i].get('text')
        next_text = unique_texts[i + 1].get('text')
        all_texts.append({
            'text': current_text,
            'translation': next_text
        })
        i += 2  # Her seferinde iki metni bir araya getir

    return jsonify({'texts': all_texts})


@app.route('/delete_text/<username>', methods=['DELETE'])
def delete_text(username):
    user_collection = db[username]
    texts_from_db = list(user_collection.find())  # Tüm verileri MongoDB'den al ve liste olarak tut

    # Verileri istediğiniz şekilde eşleştirme
    all_texts = []
    i = 0
    word_to_delete = request.args.get('word')
    while i < len(texts_from_db) - 1:

        current_text = texts_from_db[i].get('text')
        next_text = texts_from_db[i + 1].get('text')
        all_texts.append({
            'text': current_text,
            'translation': next_text
        })
        i += 2  # Her seferinde iki metni bir araya getir
        if word_to_delete == current_text:
            user_collection.delete_one({'text': word_to_delete})
            user_collection.delete_one({'text': next_text})
    return jsonify({'message': 'Text deleted successfully'})




# @app.route('/delete_text/<username>', methods=['DELETE'])
# def delete_text(username):
#     user_collection = db[username]
#
#     word_to_delete = request.args.get('word')
#
#     # Kelimeyi sil
#     result = user_collection.delete_one({'text': word_to_delete})
#
#     if result.deleted_count > 0:
#         # Silinen kelimenin sonrasındaki kelimeyi de sil
#         next_word = user_collection.find_one({'text': word_to_delete})
#         if next_word:
#             user_collection.delete_one({'_id': next_word['_id']})
#             return jsonify({'message': f'Text "{word_to_delete}" and its translation deleted successfully'})
#         else:
#             return jsonify({'message': f'Text "{word_to_delete}" deleted successfully'})
#     else:
#         return jsonify({'error': f'Text "{word_to_delete}" not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
