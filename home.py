from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__, static_folder='.', static_url_path='')


def pivot_table(rows, cols, vals, attribute, filter, comp, fvalue):
    df = pd.DataFrame(pd.read_csv('datasetn.csv'))
    if filter:
        if filter in ['Value', 'Change%', 'Year']:
            if comp == "=":
                df2 = df.loc[df[filter] == float(fvalue)]
            elif comp == ">":
                df2 = df.loc[df[filter] > float(fvalue)]
            elif comp == ">=":
                df2 = df.loc[(df[filter] > float(fvalue)) | (df[filter] == float(fvalue))]
            elif comp == "<":
                df2 = df.loc[df[filter] < float(fvalue)]
            elif comp == "<=":
                df2 = df.loc[(df[filter] < float(fvalue)) | (df[filter] == float(fvalue))]
            elif comp == "!=":
                df2 = df.loc[df[filter] != float(fvalue)]
        else:
            if comp == "!=":
                df2 = df.loc[df[filter] != fvalue]
            else:
                df2 = df.loc[df[filter] == fvalue]
        table = pd.pivot_table(df2, index=rows, columns=cols, values=vals, aggfunc=attribute)
    else:
        table = pd.pivot_table(df, index=rows, columns=cols, values=vals, aggfunc=attribute)
    table = table.fillna(0)
    table.columns.name = None
    table = table.rename_axis(None)
    if attribute == 'count':
        a = (table.style
             .format("{:.0f}"))
    else:
        a = (table.style
             .format("{:.2f}"))
    b = a.render()
    return "<div class='heat-map'>" + ''.join(b) + "</div>"


@app.route("/")
def index_init():
    return render_template("/index.html")


@app.route("/index")
def index():
    return render_template("/index.html")


@app.route("/exchange")
def exchange():
    return render_template("/exchange.html")


@app.route("/about")
def about():
    return render_template("/about.html")


@app.route("/pivot_form")
def pivot_form():
    return render_template("/form.html")


@app.route("/database")
def database():
    return render_template("/database.html")


@app.route("/observations")
def obs():
    return render_template("/observations.html")


@app.route("/bubble")
def bub():
    return render_template("/bubble.html")


@app.route('/pivotgen', methods=['POST'])
def pivot():
    rows = request.form['row_label'] or 'Year'
    cols = request.form['col_label'] or 'Region'
    vals = request.form['agg_val'] or 'Value'
    attribute = request.form['agg_type'] or 'sum'
    filter = request.form['filter_type']
    comp = request.form['comparison'] or '='
    fvalue = request.form['filter_string']
    if cols == vals or rows == cols or vals == rows:
        error1 = 'Labels of rows, columns and aggregated value cannot be identical'
        return render_template('/form.html', error1=error1)
    if filter in ['Value', 'Change%', 'Year']:
        try:
            float(fvalue)
        except ValueError:
            error2 = "Your filter value may not be in our dataset or it is misspelled!"
            return render_template('/form.html', error2=error2)
    try:
        pivot_table(rows, cols, vals, attribute, filter, comp, fvalue)
    except IndexError:
        error2 = "Your filter value may not be in our dataset or it is misspelled!"
        return render_template('/form.html', error2=error2)
    return render_template('/pivot_table.html', rows=rows, cols=cols, vals=vals, fvalue=fvalue,
                           attribute=attribute, filter=filter, comp=comp,
                           pivot=pivot_table(rows, cols, vals, attribute, filter, comp, fvalue))


if __name__ == "__main__":
    app.run(debug=True)
