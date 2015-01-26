"""
.. module:: gentrans_tables
   :synopsis: A useful module indeed.
"""

from django.template import Context, Template
import datetime
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
import logging
import json

from models.pchemprop import pchemprop_tables
# import importlib
import gentrans_output


def getheaderpvu():
    headings = ["Parameter", "Value"]
    return headings

def getheaderpvr():
	headings = ["Parameter", "Acute", "Chronic","Units"]
	return headings


def gethtmlrowsfromcols(data, headings):
    columns = [data[heading] for heading in headings]

    # get the length of the longest column
    max_len = len(max(columns, key=len))

    for col in columns:
        # padding the short columns with None
        col += [None,] * (max_len - len(col))

    # Then rotate the structure...
    rows = [[col[i] for col in columns] for i in range(max_len)]
    return rows


def getdjtemplate():
    dj_template ="""
    <dl class="shiftRight">
    {% for label, value in data.items %}
        <dd>
        <b>{{label}}:</b> {{value|default:"none"}}
        </dd>
    {% endfor %}    
    </dl>
    """
    return dj_template


def getInputTemplate():
    input_template = """
    <th colspan="2" class="alignLeft">{{heading}}</th>
    {% for label, value in data.items %}
        <tr>
        <td>{{label}}</td> <td>{{value|default:"none"}}</td>
        </tr>
    {% endfor %}
    """
    return input_template


def getStructInfo(gentrans_obj):
    data = {
        'SMILES': gentrans_obj.smiles, 
        'IUPAC': gentrans_obj.name, 
        'Formula': gentrans_obj.formula, 
        'Mass': gentrans_obj.mass
    }
    return data


def getReactPathSimData(gentrans_obj):

    # Formats list of libraries used for display:
    libs = ""
    for item in gentrans_obj.trans_libs:
        libs += item + ", "
    libs = libs[:-2]

    data = { 
        'Libraries': libs, 
        'Generation Limit': gentrans_obj.gen_limit, 
        'Population Limit': gentrans_obj.pop_limit, 
        'Likely Limit': gentrans_obj.likely_limit
    }
    return data


tmpl = Template(getdjtemplate())
inTmpl = Template(getInputTemplate())


def table_all(gentrans_obj):
    html_all = table_inputs(gentrans_obj)
    html_all += table_metabolites(gentrans_obj)
    # html_all += pchemprop_input_fields(gentrans_obj)
    html_all += table_metabolite_info(gentrans_obj)
    # html_all += render_to_string('cts_display_raw_data.html', {'rawData': gentrans_obj.rawData})
    return html_all


def pchemprop_input_fields(gentrans_obj):
    """
    Fills hidden input element with 
    pchemprop table inputs dictionary to 
    be accessed on the front end for obtaining
    pchem props for selected metabolites 
    """
    if hasattr(gentrans_obj, 'pchemprop_obj'):
        pchemprops = json.dumps(gentrans_obj.pchemprop_obj.__dict__)
        pchemprops_safe = ''
        for char in pchemprops:
            if char == '"':
                char = '&quot;'
            pchemprops_safe = pchemprops_safe + char
        html = '<input type="hidden" id="pchemprops" value="' + pchemprops_safe + '">'
        return html
    else: 
        return ""


def table_inputs(gentrans_obj):
    """
    An attempt at making one large table
    for all user inputs
    """

    html = """
    <br>
    <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
    <div class="out_">
    <table class="inputTableForOutput">
    """
    html += inTmpl.render(Context(dict(data=getStructInfo(gentrans_obj), heading="Molecular Information")))
    html += inTmpl.render(Context(dict(data=getReactPathSimData(gentrans_obj), heading="Reaction Pathway Simulator")))
    html += """
    </table>
    </div>
    """
    return html


def timestamp(gentrans_obj="", batch_jid=""):
    if gentrans_obj:
        st = datetime.datetime.strptime(gentrans_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    else:
        st = datetime.datetime.strptime(batch_jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>Generate Transformation Pathways Version 1.0</a> (Alpha)<br>
    """
    html = html + st
    html = html + " (EST)</b>"
    html = html + """
    </div>"""
    return html


def table_metabolites(gentrans_obj):
    """
    Populate input with hidden value
    of metabolites as a json string
    """

    new_result = ''
    for char in gentrans_obj.results:
        if char == '"':
            char = '&quot;'
        new_result = new_result + char

    gentrans_obj.results = new_result

    html = """
    <H3 class="out_1 collapsible" id="section1"><span></span>Reaction Pathways</H3>
    <div class="out_">
    """
    html += '<input id="hiddenJson" type="hidden" value="' + gentrans_obj.results + '">'
    html += render_to_string('cts_gentrans_tree.html')
    html += """
    </div>
    """

    return html


def table_metabolite_info(gentrans_obj):
    """
    For floating window that displays metabolite's 
    p-chem and structure data. 
    """
    from models.pchemprop import pchemprop_parameters

    html = """
    <link rel="stylesheet" href="//code.jquery.com/ui/1.11.2/themes/smoothness/jquery-ui.css">
    <script>
    $(document).ready(function() { 
        $("#metaboliteInfo").draggable();
        $("#tabs").tabs();

        $("#pchemprop_table").css('display', 'table');

    });
    </script>
    """

    pchemHTML = render_to_string('cts_pchem.html', {})
    pchemHTML += str(pchemprop_parameters.form(None))

    html += floatTmpl().render(Context(dict(html=pchemHTML)))

    return html


def floatTmpl():
    floatTmpl = """
    <div id="metaboliteInfo">
        <div id="tabs">
            <ul>
                <li><a href="#tabs-1">View data</a></li>
                <li><a href="#tabs-2">Get data</a></li>
            </ul>
            <div id="tabs-1"><p>Right click a metabolite to view its data</p></div>
            <div id="tabs-2">
                Select properties to gather data...
                {% autoescape off %}{{html}}{% endautoescape %}
                <br>
                <input type="button" value="Get data" class="input_button" id="nodepchem">
            </div>
        </div>
    </div>
    """
    return Template(floatTmpl)