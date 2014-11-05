# -*- coding: utf-8 -*-
"""
@author: (np)
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms, template
from django.db import models	
from django.template import Context, Template
from django.utils.safestring import mark_safe
import logging
from django.template.defaultfilters import stringfilter
from django.core import validators
from models.forms import validation


# Define Custom Templates
def tmpl_ChemCalcsCTS():
	tmpl_ChemCalcsCTS = """
	{% load color_table %}
	{% for field in form %}
		{% if field.id_for_label == "id_kow_wph" %}
			<tr>
			<th class="chemprop">{{ field }} <span>{{ field.label }}</span>
		{% elif field.id_for_label == "id_kow_ph" %}
			<span>{{field.label}}</span> {{field}}</th>
			<td id="id_kow_ChemAxon" class="{{form.kow_wph|color_filter:"chemaxon"}} chemaxon"></td>
			<td id="id_kow_EPI" class="{{form.kow_wph|color_filter:"epi"}} epi"></td>
			<td id="id_kow_TEST" class="{{form.kow_wph|color_filter:"test"}} test"></td>
			<td id="id_kow_SPARC" class="{{form.kow_wph|color_filter:"sparc"}} sparc"></td>
                        <td id="id_kow_MEASURED" class="{{form.kow_wph|color_filter:"test"}} test"></td>
		{% else %}
			<tr>
			<th class="chemprop">{{ field }} <span>{{ field.label }}</span></th>
			<td id="{{ field.id_for_label }}_ChemAxon" class="{{ field | color_filter:"chemaxon" }} chemaxon"></td>
			<td id="{{ field.id_for_label }}_EPI" class="{{ field | color_filter:"epi" }} epi"></td>
			<td id="{{ field.id_for_label }}_TEST" class="{{ field | color_filter:"test" }} test"></td>
			<td id="{{ field.id_for_label }}_SPARC" class="{{ field | color_filter:"sparc" }} sparc"></td>
                        <td id="{{ field.id_for_label }}_MEASURED" class="{{ field | color_filter:"test" }} test"></td>
			</tr>
		{% endif %}
	{% endfor %}
		<tr>
			<th></th>
			<td class="ChemCalcs_available">Available</td>
			<td class="ChemCalcs_unavailable">Unavailable</td>
		</tr>
	</table>
	"""
	return tmpl_ChemCalcsCTS


tmpl_ChemCalcsCTS = Template(tmpl_ChemCalcsCTS())


# Method(s) called from *_inputs.py
def form(formData):
	form_cts_ChemCalcs_props = cts_chemCalcs_props(formData)
	html = tmpl_ChemCalcsCTS.render(Context(dict(form=form_cts_ChemCalcs_props)))
	# form_cts_Transform = cts_Transform()
	# html = html + tmpl_TransformCTS.render(Context(dict(form=form_cts_Transform)))
	return html

class cts_chemCalcs_props(forms.Form):
	melting_point = forms.BooleanField(required=False, label=mark_safe('Melting Point (&degC)'))
	boiling_point = forms.BooleanField(required=False, label=mark_safe('Boiling Point (&degC)'))
	water_sol = forms.BooleanField(required=False, label=mark_safe('Water Solubility (mg/L)'))
	vapor_press = forms.BooleanField(required=False, label=mark_safe('Vapor Pressure (mmHg)'))
	mol_diss = forms.BooleanField(required=False, label=mark_safe('Molecular Diffusivity (cm<sup>2</sup>/s)'))
	ion_con = forms.BooleanField(required=False, label=mark_safe('Ionization Constant'))
	henrys_law_con = forms.BooleanField(required=False, label=mark_safe("Henry's Law Constant (atm-m<sup>3</sup>/mol)"))
	kow_no_ph = forms.BooleanField(required=False, label=mark_safe("Octanol/Water Partition Coefficient"))
	kow_wph = forms.BooleanField(required=False, label=mark_safe('Octanol/Water Partition Coefficient'))
	kow_ph = forms.CharField (
				required=False, 
				label=mark_safe('at pH:'), 
				widget=forms.TextInput(attrs={'size':1}),
				initial=7.4
			)
	koc = forms.BooleanField(required=False, label=mark_safe('Organic Carbon Partition Coefficient'))
	# dist_coeff = forms.BooleanField(required=False, label=mark_safe('Distribution Coefficient (L/kg)'))

class PchempropInp(cts_chemCalcs_props):
	pass
