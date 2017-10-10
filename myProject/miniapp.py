from flask import Flask, render_template, flash, request
import os
import requests
import json
import argparse
import urllib
import subprocess

from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# App config.
#DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    name = TextField('Search Term:', validators=[validators.required()])


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    print form.errors
    if request.method == 'POST':
        name=request.form['name']
        print name

        ACCESS_TOKEN = 'AIzaSyCHw1SncshAFT3ry2n0poQGR4EArdx6I5Q'


        def build_URL(search_text='',types_text=''):
            base_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'     # Can change json to xml to change outp$
            key_string = '?key='+ACCESS_TOKEN                                           # First think after the base_url starts$
            query_string = '&query='+urllib.quote(search_text)
            sensor_string = '&sensor=false'                                             # Presumably you are not getting locati$
            type_string = ''
            if types_text!='':
                type_string = '&types='+urllib.quote(types_text)                        # More on types: https://developers.goo$
            url = base_url+key_string+query_string+sensor_string+type_string
            return url
        # parser = argparse.ArgumentParser()
        # parser.add_argument('-st', '--searchterm', dest='searchterm', type=str)
        # input_values = parser.parse_args()

        # a = build_URL(search_text=input_values.searchterm)
        a = build_URL(search_text=name)
        # print(a)
        response = requests.get(a)
        data = requests.get(a).json()


        # search = "San Francisco, CA"
        # print(data)
        # print(search)
        # print('python sample.py --location="%s"' % search)
        # os.system('python sample.py --location="%s"' % search)
        i = 0
        while(i <= 2):
            lat = str (data["results"][i]["geometry"]["location"]["lat"])
            long = str (data["results"][i]["geometry"]["location"]["lng"])
            placeName = str (data["results"][i]["name"])
            print("THING TO DO:")
            # print("latitude = " + lat)
            # print("longitude = " + long)
            print("Attraction = " + placeName)
            #flash("Attraction = " + placeName)
            print("")
            print("RESTUARANTS:")

            print("")
        # print('python sample.py --latitude="%s"' % lat)
        # print('python sample.py --longitude="%s"' % long)
        # os.system('python sample.py --latitude="%s" --longitude="%s"' % (lat, long))
# well one way around this is to copy in the whole file....
            #os.system('python sample.py --latitude="%s" --longitude="%s"' % (lat, long))
            output = subprocess.check_output('python sample.py --latitude="%s" --longitude="%s"' % (lat, long), shell=True)
            print(output)
            flash("Attraction = " + placeName + "<br/>" + "<br />" + output)
            i = i + 1


        if form.validate():
            # Save the comment here.
            flash('Ran search query for: ' + name)
        else:
            flash('All the form fields are required. ')

    return render_template('hello1.html', form=form)

if __name__ == "__main__":
    app.run()
