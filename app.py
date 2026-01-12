from flask import Flask, render_template, request
from recommendations import get_recommendations

app = Flask(__name__, template_folder="templates")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_id = request.form['user_id']
        recommendations = get_recommendations(user_id)
        return render_template('recommendations.html', user_id=user_id, recommendations=recommendations)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
