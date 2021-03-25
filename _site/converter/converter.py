
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
            if column == "Venue":
                table += "    <th>Venue (<a class='page-link' href='/assets/files/venues.html'>Abbreviation List</a>)</th>\n"
            else:
                table += "    <th>{0}</th>\n".format(column.strip())

    table += "  </thead>\n"

    table += "<tbody>"
    # Create the table's row data
    for r in range(len(df)):
        row = list(df.iloc[r])
        table += "  <tr>\n"
        table += "    <td>{0}</td>\n".format(r+1)
        table += "    <td><a href='{}'>{}</a></td>\n".format(row[3], row[0])
        table += "    <td>{0}</td>\n".format(row[1])
        table += "    <td>{0}</td>\n".format(row[2])
        for col in range(4, len(row)):
            if row[col] != 0:
                write_html(row[col], os.path.join(dirout, f"{r+1}-{col}.html"))
                table += "    <td>{}<a class='page-link' href='/assets/files/form_quotes/{}-{}.html'>Quote</a></td>\n".format('{% include _icons/users.html %}', r+1, col)
            else:
                table += "    <td>-</td>"
        table += "  </tr>\n"
        
    table += "</tbody>"
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
        "  <link rel='stylesheet' href='/assets/css/sortable-theme-bootstrap.css' />\n"
        "  <script src='/assets/js/sortable.min.js'></script>\n"
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


    
    intro = "This is a placeholder for adding contents, to add more"

    intro = (
            "<div class='homemain'>\n" 
            "    <div>\n"
            "        <p>\n"
            "            This is an collection of 218 NLP Explanation studies. Each paper includes: Paper Tile, Paper Link, Published Year, Published Year, Form Annotations. \n"
            "            <br>You can sort the Table heads w.r.t. forms you need to view.\n"
            "        </p>\n"
            "    </div>\n"
            "    <span class='subtitle'>Citations</span>\n"
            "    <div class='citequote'>\n"
            "        @article{exnlp:2021:hxcai,\n"
            "            <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; title = {Explaining the Road Not Taken},\n"
            "            <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; author = {Shen, Hua  and  Huang, Ting-Hao (Kenneth)},\n"
            "            <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; journal = {ACM CHI Workshop on Operationalizing Human-Centered Perspectives in Explainable AI},\n"
            "            <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; year = {2021 }\n"
            "        <br>}\n"
            "    </div>\n"
            "</div>\n")

    table = heads + intro + "<table class='sortable-theme-bootstrap' data-sortable>\n"

    csv2html_converter(table, df, fileout, dirout)

            # "            This is an collection of 218 NLP Explanation studies. Each paper includes:\n"
            # "            <li class='formlist'>Paper Tile</li>\n"
            # "            <li class='formlist'>Paper Link</li>\n"
            # "            <li class='formlist'>Published Year</li>\n"
            # "            <li class='formlist'>Published Venue</li>\n"
            # "            <li class='formlist'>Form Annotations</li>\n"