import etf_rotation_strategy as etf
import flask

app = flask.Flask(__name__)

def styleDF(df):
    df.style.set_table_styles(
    [{'selector': 'th',
    'props': [('background', '#7CAE00'), 
                ('color', 'white'),
                ('font-family', 'verdana')]},
    
    {'selector': 'td',
    'props': [('font-family', 'verdana')]},

    {'selector': 'tr:nth-of-type(odd)',
    'props': [('background', '#DCDCDC')]}, 
    
    {'selector': 'tr:nth-of-type(even)',
    'props': [('background', 'white')]},
    
    ]
    ).hide_index()
    return (df.to_html(border=5, col_space=10, index=False))

@app.route('/')
def home():
    output = ''
    df = styleDF(etf.df_etf)
    output = output + f'<h3>Top {etf.n} ETFs : {etf.df_etf.head(etf.n).Symbols.values}</h3><p>'
    output = output + '<hr style="width:42%;height:3px; background-color:#333;text-align:left;margin-left:0">'
    output = output + f'{df}'
    # output = output + f'{etf.df_etf.to_html()}'
    return (output)
    
# app.run(host='0.0.0.0', port=8080, debug=True)