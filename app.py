import etf_rotation_strategy as etf
import flask

app = flask.Flask(__name__)

@app.route('/')
def home():
    output = ''
    output = output + f'<h3>Top {etf.n} ETFs : {etf.df_etf.head(etf.n).Symbols.values}</h3><p>'
    output = output + f'{etf.df_etf.to_html()}'
    return (output)
    
app.run(host='0.0.0.0', port=8080, debug=True)