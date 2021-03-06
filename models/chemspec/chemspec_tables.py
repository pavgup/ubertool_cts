"""
.. module:: chemspec_tables
   :synopsis: A useful module indeed.
"""

# import numpy
from django.template import Context, Template, defaultfilters
# from django.utils.safestring import mark_safe
# import logging
import time
import datetime
from django.template.loader import render_to_string
import logging
import json
from StringIO import StringIO
from django.utils.safestring import mark_safe
from models.gentrans import data_walks


# image sizes:
lgWidth = 250
mdWidth = 125 
smWidth = 75
scale = 100 # default is 28 


def getdjtemplate():
    dj_template ="""
    <dl class="shiftRight">
    {% for label, value in data.items %}
        <dd>
        {{label}}: {{value|default:"none"}}
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


def getMolTblData(chemspec_obj):
    data = {
        'SMILES': chemspec_obj.smiles, 
        'IUPAC': chemspec_obj.name, 
        'Formula': chemspec_obj.formula, 
        'Mass': chemspec_obj.mass
    }
    return data


def getIsoPtData(chemspec_obj):
    data = {
        'Isoelectric Point': chemspec_obj.isoPtDict['isoPt']
    }
    return data


# Ionization Constants (pKa) Parameters Data
def getPkaInputs(chemspec_obj):
    data = {
        'Number of Decimals': chemspec_obj.pKa_decimals, 
        'pH Lower Limit': chemspec_obj.pKa_pH_lower, 
        'pH Upper Limit': chemspec_obj.pKa_pH_upper,  
        'pH Step Size': chemspec_obj.pKa_pH_increment,
        'Generate Major Microspecies at pH': chemspec_obj.pH_microspecies,
        'Isoelectric Point (pl) pH Step Size of Charge Distribution': chemspec_obj.isoelectricPoint_pH_increment
    }
    return data


# Dominate Tautomer Distribution Data
def getTautData(chemspec_obj):
    data = {
        'Maximum Number of Structures': chemspec_obj.tautomer_maxNoOfStructures, 
        'at pH': chemspec_obj.tautomer_pH
    }
    return data


# Stereoisomers Data
def getStereoData(chemspec_obj):
    data = {
        'Maximum Number of Structures': chemspec_obj.stereoisomers_maxNoOfStructures
    }
    return data


# Parent/Micro species data dictionary for templating
def getPkaValues(chemspec_obj):
    # jsonData = json.dumps(chemspec_obj.result)
    
    data = { 
        'Basic pKa Value(s)': chemspec_obj.pkaDict['mostBasicPka'], 
        'Acidic pKa Value(s)': chemspec_obj.pkaDict['mostAcidicPka']
    }
    return data


# djtemplate = getdjtemplate()
tmpl = Template(getdjtemplate())
inTmpl = Template(getInputTemplate())


def table_all(chemspec_obj):
    # html_all = '<script type="text/javascript" src="/static/stylesheets/structure_wrapper.js"></script>'
    html_all = '<script type="text/javascript" src="/static/stylesheets/qtip/jquery.qtip.js"></script>'
    html_all += '<link type="text/css" rel="stylesheet" href="/static/stylesheets/qtip/jquery.qtip.css"></link>'
    # inputs:
    html_all += table_inputs(chemspec_obj)
    # outputs:
    html_all += table_outputs(chemspec_obj)
    # raw data button and textbox:
    # html_all += render_to_string('cts_display_raw_data.html', {'rawData': chemspec_obj.rawData}) # temporary
    # qtip popup script for images with class "wrapped_molecule"
    html_all += """
    <script>
    function tipit() {
        // Using qtip2 for tooltip
        $('.chemspec_molecule').each(function() {
            $(this).qtip({
                content: {
                    text: $(this).next('.tooltiptext')
                },
                style: {
                    classes: 'qtip-light'
                },
                position: {
                    my: 'bottom center',
                    at: 'center right',
                    target: 'mouse'
                }
            });
        });
    }
    </script>
    <script>
    tipit();
    </script>
    """
    return html_all


def timestamp(chemspec_obj="", batch_jid=""):
    if chemspec_obj:
        st = datetime.datetime.strptime(chemspec_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    else:
        st = datetime.datetime.strptime(batch_jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div id="timestamp" class="out_">
        <b>Chemical Speciation - Version 1.0 (Alpha)<br>
    """
    html += st
    html += " (EST)</b>"
    html += """
    </div>"""
    return html


def table_inputs(chemspec_obj):
    """
    An attempt at making one large table
    for all user inputs. This will/would replace
    table_struct, table_pka_input, table_taut_input,
    and table_stereo_input
    """
    html = """
    <br>
    <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
    <div class="out_">
    <table class="inputTableForOutput">
    """
    html += inTmpl.render(Context(dict(data=getMolTblData(chemspec_obj), heading="Molecular Information")))
    html += inTmpl.render(Context(dict(data=getPkaInputs(chemspec_obj), heading="Ionization Parameters")))
    html += inTmpl.render(Context(dict(data=getTautData(chemspec_obj), heading="Tautomer Parameters")))
    html += inTmpl.render(Context(dict(data=getStereoData(chemspec_obj), heading="Stereoisomer Parameters")))
    html += """
    </table>
    </div>
    <br>
    """
    return html


def table_outputs(chemspec_obj):

    html = """
    <H3 class="out_1 collapsible" id="section1"><span></span>Results</H3>
    <div class="out_">
    """
    # build output with below defs
    # html += inTmpl.render(Context(dict(data=getPkaResults(chemspec_obj), heading="pKa")))

    html += getPkaResults(chemspec_obj)
    html += getIsoPtResults(chemspec_obj)
    html += getMajorMsImages(chemspec_obj)
    html += getStereoisomersResults(chemspec_obj)
    html += getTautomerResults(chemspec_obj)
    html += """
    </div>
    """
    return html


def getIsoPtResults(chemspec_obj):
    """
    IsoelectricPoint calculations
    """
    try:
        isoPtObj = chemspec_obj.jchemPropObjects['isoelectricPoint']
        isoPt = isoPtObj.getIsoelectricPoint()
        isoPtChartData = isoPtObj.getIsoPtChartData()
    except AttributeError:
        logging.info("isoelectricPoint not checked..moving on..")
        return ""
    else:
        html = """
        <H4 class="out_1 collapsible" id="section6"><span></span>Isoelectric Point</H4>
        <div class="out_">
        """
        if isoPt:
            html += '<div id="isoPtData" class="hideData">'
            html += mark_safe(json.dumps(isoPtChartData))
            html += '</div>'
            html += render_to_string('cts_plot_isoelectricPoint.html', {"ip": isoPt})
        else:
            html += '<p>No isoelectric point</p>'
        html += '</div>'
        return html


def getMajorMsImages(chemspec_obj):
    """
    MajorMicrospecies image
    """
    try:
        majorMsDict = chemspec_obj.jchemPropObjects['majorMicrospecies'].getMajorMicrospecies()
    except AttributeError:
        logging.info("major microspecies not checked..moving on..")
        return ""
    else:
        html = """
        <H4 class="out_1 collapsible" id="section6"><span></span>Major Microspecies at pH: {}</H4>
        <div class="out_ shiftRight">""".format(chemspec_obj.pH_microspecies)
        html += wrap_molecule(majorMsDict, None, mdWidth, scale)
        html += """
        </div>
        """
        return html


def getPkaResults(chemspec_obj):
    html = """
    <H4 class="out_1 collapsible" id="section6"><span></span>pKa</H4>
    <div class="out_">
    """
    # acidic/basic pKa values:
    try:
        pkaValues = {
            'Acidic pKa Value(s)': chemspec_obj.jchemPropObjects['pKa'].getMostAcidicPka(),
            'Basic pKa Value(s)': chemspec_obj.jchemPropObjects['pKa'].getMostBasicPka()
        }
    except AttributeError:
        logging.info("pKa not selected..moving..")
        return "" # get out of here!
    else:
        html += tmpl.render(Context(dict(data=pkaValues)))

    # pKa parent species:
    html += '<table id="msMain"><tr><td>'
    html += wrap_molecule(chemspec_obj.jchemPropObjects['pKa'].getParent(), None, lgWidth, scale)
    html += '<br></td><td>'

    # pKa microspecies:
    microspeciesList = chemspec_obj.jchemPropObjects['pKa'].getMicrospecies()
    try:
        for item in microspeciesList:
            html += wrap_molecule(item, None, smWidth, scale)
    except TypeError as te:
        logging.info("no microspecies to plot..moving on")
        html += 'No microspecies to plot'

    html += '</td><td><br>'

    # Microspecies Distribution Plot:
    html += '<div id="microDistData1" class="hideData">'
    html += mark_safe(json.dumps(chemspec_obj.jchemPropObjects['pKa'].getChartData()))
    html += '</div>'
    html += render_to_string('cts_plot_microspecies_dist.html')
    html += '</td></table></div>'

    return html


def getStereoisomersResults(chemspec_obj):
    """
    Stereoisomers image 
    """
    try:
        stereoList = chemspec_obj.jchemPropObjects['stereoisomers'].getStereoisomers()
    except AttributeError:
        logging.info("stereoisomers not checked..moving on..")
        return ""

    html = """
    <H4 class="out_1 collapsible" id="section10"><span></span>Stereoisomers ({})</H4>
    <div class="out_ shiftRight">""".format(len(stereoList))

    html += '<dl style="display:inline-block">'
    for item in stereoList:
        html += '<dd style="float:left;">'
        html += wrap_molecule(item, None, mdWidth, scale)
        html += '</dd>'
    html += "</dl>"

    html += """
    </div>
    """
    return html


def getTautomerResults(chemspec_obj):
    """
    Tautomer image
    """
    try:
        tautStructs = chemspec_obj.jchemPropObjects['tautomerization'].getTautomers()
    except AttributeError:
        logging.info("tautomerization not selected..moving on..")
        return ""

    html = """
    <H4 class="out_1 collapsible" id="section11"><span></span>Tautomerization</H4>
    <div class="out_ shiftRight">
    """

    # try:
    html += '<dl style="display:inline-block">'
    for item in tautStructs:
        html += '<dd style="float:left;">'
        if item and 'dist' in item:
            html += "Percent Dist: {}%".format(item['dist'])
            html += wrap_molecule(item, None, mdWidth, scale)
        else:
            html += "No tautomers"
        html += '</dd>'
    html += "</dl>"
    # except TypeError:
        # logging.info("no tautomers..")
        # html += 'no tautomers'
    # finally:
    html += """
    </div>
    """
    return html


def wrap_molecule(propDict, height, width, scale):
    """
    Wraps molecule image result (source url) with a table
    and populates said table with molecular details.

    Inputs: property dict (e.g., pka, taut image urls)
    Outputs: name, iupac, forumula, mass data wrapped in table with image and name
    """

    key = None
    if 'key' in propDict:
        key = propDict['key']

    # image = propDict['image']
    # image = mark_safe(data_walks.nodeWrapper(propDict['smiles'], 114, 100, key)) # displayed image
    # image = mark_safe(data_walks.nodeWrapper(propDict['smiles'], height, width, key)) # displayed image
    image = mark_safe(data_walks.nodeWrapper(propDict['smiles'], None, width, scale, key)) # displayed image
    formula = propDict['formula']
    iupac = propDict['iupac']
    mass = "{} g/mol".format(propDict['mass'])
    smiles = propDict['smiles']

    infoDict = {
        "image": image,
        "formula": formula,
        "iupac": iupac,
        "mass": mass,
        "smiles": smiles
    }

    # html = '<table class="' + defaultfilters.slugify(infoDict['iupac']) +' wrapped_molecule">'
    # # html += '<tr><td align="center">' + infoDict['iupac'] + '</td></tr>'
    # html += '<tr><td align="center">' + infoDict['image'] + '</td></tr></table>'

    html = """
    <div class="chemspec_molecule">
    """
    html += infoDict['image']
    html += """
    </div>
    """
    wrappedDict = data_walks.popupBuilder(infoDict, ['formula', 'iupac', 'mass', 'smiles'], key, 'Molecular Information') # popup table image
    # html += '<div class="tooltiptext ' + iupac + '">' + wrappedDict['html'] + '</div>'
    html += '<div class="tooltiptext ' + iupac + '">'
    html += wrappedDict['html']
    html += '</div>'

    return html