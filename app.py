from flask import Flask, render_template, request
import os
import importlib

app = Flask(__name__)

@app.route('/')
def home():
    import etf_rotation_strategy
    importlib.reload(etf_rotation_strategy)
    import etf_rotation_strategy as etf
    top_n_etfs = etf.df_etf.head(etf.n).Symbols.values
    return render_template("etfs.html", today=etf.today, n=etf.n, top_n_etfs=top_n_etfs,
    df_etf=etf.df_etf)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        etfs = request.form['etfs']
    file = 'etfs.txt'
    try:
        with open(f'{file}', 'w') as f:
            f.write(etfs)
    except:
        print ('Could not write to "{file}"')
    import etf_rotation_strategy
    importlib.reload(etf_rotation_strategy)
    import etf_rotation_strategy as etf
    if (etf.error != ''):
        return render_template("etfs.html",  error=error)
    else:
        top_n_etfs = etf.df_etf.head(etf.n).Symbols.values
        return render_template("etfs.html",  today=etf.today, n=etf.n, top_n_etfs=top_n_etfs,
        df_etf=etf.df_etf)    
    
# app.run(host='0.0.0.0', port=8080, debug=True) 