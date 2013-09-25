from flask.ext.wtf import Form, TextField, FileField, BooleanField, widgets, SelectMultipleField, TextAreaField, SubmitField, RadioField
from flask.ext.wtf import Required, validators
from app import models
from models import Species, IpMethod, AnatomyOntology

def _makeSelectList(table):  # given a table name, return a list of fields to select
    selectList = []
     
    if (table == 'Species'):  # make species list
        selectObjs = models.Species.query.all()
        
        for each in selectObjs:
            selectList.append((each.species_id, each.name))
            
    if (table == 'IpMethod'): # make method list
        selectObjs = models.IpMethod.query.all()
        
        for each in selectObjs:
            selectList.append((each.method_id, each.display_name))
            
    if (table == 'AnatomyOntology'): # make tissue list
        selectObjs = models.AnatomyOntology.query.all()
        
        for each in selectObjs:
            selectList.append((each.uberon_id, each.uberon_description))
            
    return selectList

class SearchForm(Form):  # returns the form fields for searching
    geneid = TextField('Search for Gene ID:', validators = [Required()])       
    speciesid = SelectMultipleField('Select Species:', choices=_makeSelectList('Species'))  
    tissueid = SelectMultipleField('Select Tissue:', choices=_makeSelectList('AnatomyOntology'))    
    methodid = SelectMultipleField('Select Method:', choices=_makeSelectList('IpMethod'))
                     #              widget = widgets.ListWidget(prefix_label=False),
                     #              option_widget=widgets.CheckboxInput())
        
class UploadForm(Form): # returns the upload form fields
    filename = FileField("", [validators.Required()])
    name = TextField("*Name:", [validators.Required()])
    email = TextField("*Email:", [validators.Required(), validators.Email()])
    subject = TextField("*Subject:", [validators.Required()])
    peakcaller = TextField("*Peak Caller Used:", [validators.Required()])
    supplementalinfo = TextAreaField("*Supplemental Info:",  [validators.Required()])
    submit = SubmitField("Upload")
    
class ContactForm(Form):  # returns the contact form fields
    name = TextField("*Name:", [validators.Required()])
    email = TextField("*Email:", [validators.Required(), validators.Email()])
    subject = TextField("*Subject:", [validators.Required()])
    affiliation = TextAreaField("*Affiliation",  [validators.Required()])
    fieldofinterest = TextAreaField("*Field(s) of Interest:",  [validators.Required()])
    message = TextAreaField("*Comments:",  [validators.Required()])
    submit = SubmitField("Send")
    
    
