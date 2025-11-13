from flask import Flask,render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta
import requests 

app = Flask(__name__)
app.secret_key = '1q2w3e4r5t6y7u8i9o0pp0o9i8u7y6t5r4e3w2q1'
app.permanent_session_lifetime = timedelta(minutes=30)

API='https://www.themealdb.com/api/json/v1/1/search.php?s='
api_detalles='https://www.themealdb.com/api/json/v1/1/lookup.php?i='




@app.route('/' , methods=['GET', 'POST'])
def index():
        
    return render_template('base.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    comida = request.form.get('name', '').strip().lower()
    
    if not comida:
        flash('Por favor ingresa un nombre de comida válido.', 'error')
        return redirect(url_for('index'))
    
    API = "https://www.themealdb.com/api/json/v1/1/search.php?s="

    try:
        response = requests.get(f"{API}{comida}")
        if response.status_code == 200:
            comida_data = response.json()
            if comida_data['meals']:

                lista_comidas = []  # <--- lista de comidas

                for platillo in comida_data['meals']:  # <--- recorre TODAS
                    comida_info = {
                        'name': platillo['strMeal'].title(),
                        'categoria': platillo['strCategory'],
                        'area': platillo['strArea'],
                        'instrucciones': platillo['strInstructions'],
                        'imagen': platillo['strMealThumb'],
                        'ingredientes': []
                    }

                    for i in range(1, 21):
                        ingrediente = platillo.get(f'strIngredient{i}')
                        medida = platillo.get(f'strMeasure{i}')
                        if ingrediente and ingrediente.strip():
                            comida_info['ingredientes'].append(f"{ingrediente} - {medida}")

                    lista_comidas.append(comida_info)

                return render_template('targeta.html', comidas=lista_comidas)

            else:
                flash(f'Comida "{comida}" no encontrada.', 'error')
                return redirect(url_for('index'))

        else:
            flash('Error al obtener datos de la API.', 'error')
            return redirect(url_for('index'))

    except requests.exceptions.RequestException as e:
        print(e)
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