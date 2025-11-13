from flask import Flask,render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta
import requests 

app = Flask(__name__)
app.secret_key = '1q2w3e4r5t6y7u8i9o0pp0o9i8u7y6t5r4e3w2q1'
API='https://www.themealdb.com/api/json/v1/1/search.php?s='
app.permanent_session_lifetime = timedelta(minutes=30)

@app.route('/' , methods=['GET', 'POST'])
def index():
        
    return render_template('base.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    comida = request.form.get('name', '').strip().lower()
    
    if not comida:
        flash('Por favor ingresa un nombre de comida válido.', 'error')
        return redirect(url_for('base'))
    
    try:
        response = requests.get(f"{API}{comida }")
        if response.status_code == 200:
            comida_data = response.json()

            comida_info = {
                'name': comida_data['strMeal'].title(),
                'categoria': comida_data['strCategory'],
                'height': comida_data['strArea'],
                'instrucciones': comida_data['strInstructions'],
                'imagen': comida_data['strMealThumb'],
            }
            
            return render_template('targeta.html', comidas=comida_info)
        else:
            flash(f'Comida "{comida}" no encontrada.', 'error')
            return redirect(url_for('index'))
        
    except requests.exceptions.RequestException:
        flash('Error al conectar con la API de comida. Inténtalo de nuevo más tarde.', 'error')
        return redirect(url_for('index'))

@app.route('/targeta', methods=['GET', 'POST'])
def targeta():
    return render_template('targeta.html')

@app.route('/targetaplia', methods=['GET', 'POST'])
def targetaplia():
    return render_template('targetaplia.html')

if __name__ == '__main__':
    app.run(debug=True)