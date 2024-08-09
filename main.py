from flask import Flask, render_template, request, flash
from googletrans import Translator
import requests
import datetime

app = Flask(__name__)
app.secret_key = 'hjhjsdahhds'  

@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        ville = request.form['ville']

        url = f'https://api.openweathermap.org/data/2.5/weather?q={ville}&appid=6a1858373170036b7d59fd4bbe98cae2'
        params = {'units': 'metric'}

        translator = Translator()

        jour = datetime.date.today()
        info = requests.get(url, params=params).json()
        description_english = info['weather'][0]['description']
        icon = info['weather'][0]['icon']
        temp = info['main']['temp']
        description_french = translator.translate(description_english, src='en', dest='fr').text
        background_image = f"images/{description_english}.png"

        return render_template('index.html',
                               description_english=description_english,
                               description_french=description_french,
                               icon=icon,
                               temp=temp,
                               jour=jour,
                               ville=ville,
                               background_image=background_image,
                               exception_occurred=False)

    except KeyError:
        exception_occurred = True
        flash('Entered data is not available to API')
        jour = datetime.date.today()
        return render_template('index.html',
                               description_english='clear sky',
                               description_french='ciel clair',
                               icon='01d',
                               temp=25,
                               jour=jour,
                               ville='Paris',
                               background_image="images/default.png",
                               exception_occurred=exception_occurred)

if __name__ == '__main__':
    app.run(debug=False)
