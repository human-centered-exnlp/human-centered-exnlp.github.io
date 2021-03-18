
#!/usr/bin/python3
import os
import sys
import pandas as pd



def write_html(content, dirname):
    fileout = open(dirname, "w")
    fileout.writelines(content)
    fileout.close()
    
    
def csv2html_converter(table, df, fileout, dirout):
    """
    Input: .csv file
    Output: 1) form.html; 2) quotes files.
    """

    # Create the table's column headers

    header = list(df.head(0))
    table += "  <thead>\n"
    table += "    <th init-sort>ID</th>\n"
    for column in header:
        if not column == "Paper URL":
            table += "    <th>{0}</th>\n".format(column.strip())
    table += "  </thead>\n"


    # Create the table's row data
    for r in range(len(df)):
        row = list(df.iloc[r])
        table += "<tbody>"
        table += "  <tr>\n"
        table += "    <td>{0}</td>\n".format(r+1)
        table += "    <td><a href='{}'>{}</a></td>\n".format(row[3], row[0])
        table += "    <td>{0}</td>\n".format(row[1])
        table += "    <td>{0}</td>\n".format(row[2])
        for col in range(4, len(row)):
            if row[col] != 0:
                write_html(row[col], os.path.join(dirout, f"{r+1}-{col}.html"))
                table += "    <td>{}<a class='page-link' href='/assets/files/form_quotes/{}-{}.html'>Quote</a>".format('{% include _icons/users.html %}', r+1, col)
        table += "</tbody>"
        table += "  </tr>\n"
        
    table += "</table>"
    fileout.writelines(table)
    fileout.close()
    


if __name__ == "__main__":

    df=pd.read_csv('xai_forms.csv', sep=',').fillna(0)
    fileout = open("../src/forms.html", "w")
    dirout = "../assets/files/form_quotes"

    heads = (
        "---\n"
        "layout: default\n"
        "---\n"
        "\n\n\n"
        "<head>\n"
        "  <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/sortable/0.8.0/css/sortable-theme-bootstrap.min.css' />\n"
        "  <script src='https://cdnjs.cloudflare.com/ajax/libs/sortable/0.8.0/js/sortable.min.js'></script>\n"
        "  <script type='text/javascript' src='https://cdn.rawgit.com/pcooksey/bibtex-js/ef59e62c/src/bibtex_js.js'></script>\n"
        "  <bibtex src='references.bib'></bibtex>\n"
        "  <link rel='stylesheet' href='/assets/css/main.css'>\n"
        "</head>"
        "\n\n\n"

        "<script type='text/javascript'>\n"
        "  var table = document.querySelectorAll('table[data-sortable]')[0]\n"
        "  Sortable.initTable(table)\n"

        "  var initSortCol = document.querySelectorAll('table[data-sortable] > thead > tr > th[init-sort]')\n"
        "  if (initSortCol.length > 0) {\n"
        "    initSortCol[0].click()\n"
        "  }\n"

        "  function myFunction(variable) {\n"
        "    var myWindow = window.open('Quotes', variable, 'width=600, height=600');\n"
        "    myWindow.document.write('<p>'+myWindow.name+'</p>');\n"
        "  }\n"
        "</script>\n\n\n")


    table = heads + "<table class='sortable-theme-bootstrap' data-sortable>\n"

    csv2html_converter(table, df, fileout, dirout)