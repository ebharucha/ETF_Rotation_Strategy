import etf_rotation_strategy as etf
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def home():
    top_n_etfs = etf.df_etf.head(etf.n).Symbols.values
    return render_template("etfs.html", today=etf.today, n=etf.n, top_n_etfs=top_n_etfs,
    df_etf=etf.df_etf)
    
# app.run(host='0.0.0.0', port=8080, debug=True) 