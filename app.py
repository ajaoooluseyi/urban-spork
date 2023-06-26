from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:march196@localhost/testdatabase'
db = SQLAlchemy(app)

#create Word table in database
class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False, default="Test")

#get function to get word "Test"
@app.route('/get-word')
def get_word():
    word = Word.query.first()
    if word:
        response = {'word': word.word}
        return jsonify(response), 200  # Return status code 200 (OK)
    else:
        return jsonify({'message': 'Word not found'}), 404  # Return status code 404 (Not Found)


#function to change word in DB
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        new_word = request.form['word']
        word = Word.query.first()
        if word is None:
            word = Word(word=new_word)
            db.session.add(word)
            return jsonify({'message': 'Word added successfully.'}), 200
        else:
            word.word = new_word        
        db.session.commit()
        return jsonify({'message': 'Word updated successfully.'}), 200
    return render_template('admin.html', word=Word.query.first())


if __name__ == '__main__':
    app.run(debug=True)
