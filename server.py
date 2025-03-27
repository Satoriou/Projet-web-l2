from flask import Flask, session, Response, request, redirect, url_for, render_template
import data_model as model


app = Flask(__name__)


########################################
# Routes des pages principales du site #
########################################

# Retourne une page principale 
@app.get('/')
def home():
  return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)
