from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import numpy as np
import joblib
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load model
model_path = os.path.join('model', 'loan.pickle')
model = joblib.load(model_path)

# Root redirects to login if not authenticated
@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname == 'admin' and pwd == 'admin123':
            session['user'] = 'admin'
            return redirect(url_for('admin'))
        elif uname == 'user' and pwd == 'user123':
            session['user'] = 'user'
            return redirect(url_for('home'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

# Logout route to clear session
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Admin page (now showing logout.html)
@app.route('/admin')
def admin():
    if session.get('user') == 'admin':
        return render_template('logout.html')
    return redirect(url_for('login'))

# Prediction form page
@app.route('/predict')
def predict_page():
    if session.get('user') in ['user', 'admin']:
        return render_template('predict.html')
    return redirect(url_for('login'))

# Result page
@app.route('/result')
def result():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('result.html')

# API endpoint for prediction
@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        data = request.get_json()
        features = [int(data[key]) for key in [
            'dependents', 'education', 'self_employed', 'income',
            'loan_amount', 'loan_term', 'cibil_score', 'residential',
            'commercial', 'luxury', 'bank'
        ]]
        prediction = model.predict([np.array(features)])[0]
        return jsonify({'result': "Approved" if prediction == 0 else "Rejected"})
    except Exception as e:
        return jsonify({'error': str(e)})

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

