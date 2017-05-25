__author__ = 'christiaan'

from bs4 import BeautifulSoup as Soup
import codecs
from lxml import html
import lxml
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def template_test():
    return render_template('template.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5])





#if __name__ == '__main__':
    #app.run(debug=True)

