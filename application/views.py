import os, json
from flask import render_template, request, flash, redirect, url_for, send_from_directory, jsonify
from werkzeug import secure_filename
from application import application
from application import db, models
from forms import SearchForm, UploadForm, ContactForm
from models import Genes, Datasets, Species, AnatomyOntology, IpMethod
from flask.ext.mail import Message, Mail
from flask.ext.sqlalchemy import SQLAlchemy

ALLOWED_EXTENSIONS = set(['bed', 'txt', 'rtf'])

mail = Mail()
mail.init_app(application)
app = application
@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')

@app.route('/_peaks/<int:entrez_id>')  ## returns a json object for datatables for a single gene
def broad_peak_data(entrez_id):         ## called by search page  ##  ## need to filter by tissue and method if they are passed
    #entrez_id = request.args.get('geneId')
    
    gene = models.Genes.query.filter(Genes.entrez_gene_id == entrez_id).one()
         ## make array of dictionaries
    peak_data = []
    
  #  if request.args.get('methods') != 'None':
  #      methods = request.args.get('methods')
        
   # if request.args.get('tissues') != 'None':
   #     tissues = request.args.get('tissues')
        
            ## get broad peak info as a json object to populate datatables##
    for each_peak in gene.broad_peaks:
        
       # if (methods or tissues):
     #  if (each_peak.dataset.method.method_id in methods or (each_peak.dataset.tissue.uberon_id in tissues)):
        peak_data.append([
                          str(each_peak.breadth_signal),
                          each_peak.dataset.method.display_name,
                          each_peak.dataset.tissue.uberon_description, # link to uberon
                          each_peak.dataset.bio_sample
                          ])
    
    return jsonify(aaData = peak_data)

@app.route('/_multi_peaks', methods=['GET']) ## returns a json object for datatables             
def multi_broad_peaks():                    ### for a list of entrez_ids, species_ids, tissue_ids, or methods; called by search page
## search with a list of multiple gene ids ###  
    method_list = []
    tissue_list = []
    
  #  query = request.query_string
 #   return request.args.get('method_ids')

    if request.args.get('gene_ids'):
        ids = request.args.get('gene_ids')
    
        # return ids   
        id_list = ids.split(' ')
          # return id_list
 
        genes = models.Genes.query.filter(Genes.entrez_gene_id.in_(id_list)).all()
 
    if request.args.get('method_ids'):  # get methods if there are any
        methods = request.args.get('method_ids')
        
        #return method ids
        method_list = methods.split(' ')
        
    if request.args.get('tissue_ids'):  # get tissue ids if there are any
        tissues = request.args.get('tissue_ids')
        #return tissues
        #return tissue ids
        tissue_list = tissues.split(' ')
         
    peak_data = []
        
    for one_gene in genes:
            
        for each_peak in one_gene.broad_peaks:
          
            if (len(method_list) == 0 and len(tissue_list) == 0):  ## NO FILTER FOR TISSUE OR METHOD
                peak_data.append([one_gene.gene_url,
                                      one_gene.species.name,
                                      str(each_peak.breadth_signal),
                                      each_peak.dataset.method.display_name,
                                      each_peak.dataset.tissue.uberon_description,  ## link to uberon?
                                      each_peak.dataset.bio_sample
                                  ])
                continue
            
            if (len(method_list) > 0):  ## there is a method filter
                     
                if (str(each_peak.dataset.method_id) in method_list):  # method filter agrees
                                     
                    if (len(tissue_list) > 0): # tissue filter, too
                        if (str(each_peak.dataset.uberon_id) in tissue_list): # tissue filter agrees and method filter pass
                            peak_data.append([one_gene.gene_url,
                                      one_gene.species.name,
                                      str(each_peak.breadth_signal),
                                      each_peak.dataset.method.display_name,
                                      each_peak.dataset.tissue.uberon_description,  ## link to uberon?
                                      each_peak.dataset.bio_sample
                                  ])
                        else:     # right method, wrong tissue
                            continue
                    else:  # right method, no tissue filter
                        peak_data.append([one_gene.gene_url,
                                      one_gene.species.name,
                                      str(each_peak.breadth_signal),
                                      each_peak.dataset.method.display_name,
                                      each_peak.dataset.tissue.uberon_description,  ## link to uberon?
                                      each_peak.dataset.bio_sample
                                  ])
                else:  # method filter is wrong; doesn't matter if there is a tissue filter or not
                    continue
                
            else:  # no method filter
               # return ("no method filter")
                if(len(tissue_list) > 0):  # tissue filter
                    
                    if(str(each_peak.dataset.uberon_id) in tissue_list):  #tissue filter right, no method filter
                         peak_data.append([one_gene.gene_url,
                                      one_gene.species.name,
                                      str(each_peak.breadth_signal),
                                      each_peak.dataset.method.display_name,
                                      each_peak.dataset.tissue.uberon_description,  ## link to uberon?
                                      each_peak.dataset.bio_sample
                                  ])
                         
                        # return each_peak.dataset.tissue.uberon_description
                    else:  # no method filter, wrong tissue
                        #return ('no method filter, wrong tissue filter')
                        continue
                else: # no tissue or method filter
                    peak_data.append([one_gene.gene_url,
                                      one_gene.species.name,
                                      str(each_peak.breadth_signal),
                                      each_peak.dataset.method.display_name,
                                      each_peak.dataset.tissue.uberon_description,  ## link to uberon?
                                      each_peak.dataset.bio_sample
                                  ])
            
    return jsonify(aaData = peak_data)
    
        
@app.route('/search', methods = ['GET', 'POST'])
def search():
    form = SearchForm()

    ## searching by gene name ##
    if request.method == 'POST': # and form.validate():
        geneid = form.geneid.data or 'None'    
        speciesid = form.speciesid.data or 'None'
        tissueid = form.tissueid.data or 'None'
        methodid = form.methodid.data or 'None'
       
        input = ""
        result = models.Genes.query
        
        if (geneid != 'None'):  ## Try symbol first
            input = geneid
            
            geneList = geneid.split(", ")  ## see if there is > 1 gene id, separated by commas
            
            if (len(geneList) == 1):
                geneList = geneList[0].split(",") ## make sure it isn't just a space issue
                      
            result = result.filter(Genes.symbol.in_(geneList))
            
        ## then filter by species;
          
        if (speciesid != 'None'):
            input = input + (", ").join(speciesid)
            
            result = result.filter(Genes.species_id.in_(speciesid))
            
        temp_result = result.all()
        
        ## no results -- straight tissue or method search 
        if len(temp_result) == 0:
            
            if (tissueid != 'None'):
                result = result.filter(Datasets.tissue.uberon_id.in_(tissueid))
            else:
                return render_template('no_results.html', query=input)
            
        elif (len(temp_result) == 1): ## return a gene page if there is one result
            
            return render_template('gene_page.html', 
                                 gene=result[0],
                                 tissues = tissueid,
                                 methods = methodid)
         
        elif (len(temp_result) > 1): ## returns a page with multiple results if there is more than one result
            geneList = []
            for each in result:
                geneList.append(str(each.entrez_gene_id))
            
            return render_template('search_result.html', 
                                   genes=result,
                                   geneList = geneList,
                                   tissues = tissueid,
                                   methods = methodid)
        
        else:
            
            return render_template('no_results.html', 
                                   query = input)
            
    elif request.method == 'GET':
        # see if it is an entrez id; specifically for a single gene page
        geneid = request.args.get('entrezId')  ## search by entrez gene id
        
        if (geneid):
            result = models.Genes.query.filter(Genes.entrez_gene_id == geneid).all()
            
            if (len(result) == 1): ## return a gene page if there is one result
                return render_template('gene_page.html', 
                                       gene=result[0]
                                       )
                
            elif (len(result) > 1): ## return multiple results page if there is more than one result (shouldn't happen)
                geneList = []
                for each in result:
                    geneList.append(str(each.entrez_gene_id))
                    
                return render_template('search_result.html', 
                                   genes=result,
                                   geneList = geneList)
            else:
                return render_template('no_results.html',
                                       query = geneid)
        else: # no entrezId
            return render_template('search.html', form=form)
  
    
@app.route('/dataset/<int:datasetId>')
def dataset_page(datasetId):
    return render_template('dataset.html',
                           dataset = models.Datasets.query.filter(Datasets.dataset_id == datasetId).one()
    )
    
#@app.route('/method/<int:methodid>')
#def dataset_page(datasetId):
#    return render_template('dataset.html',
#                           dataset = models.Datasets.query.filter(Datasets.dataset_id == datasetId).one()
#)
                   
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return render_template('success.html')
                     
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
  form = UploadForm()
  
  if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('upload.html', form=form)
        else:
            file = request.files['filename']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                msg = Message(form.subject.data, sender='yeastmine@gmail.com', recipients=['yeastmine@gmail.com'])
                msg.body = """
                From: %s <%s>
                Subject: %s
                PeakCaller: %s
                SupplementalInfo: %s
                File Name: %s
                """ % (form.name.data, form.email.data, form.subject.data, form.peakcaller.data, form.supplementalinfo.data, filename)
                mail.send(msg)
                return redirect(url_for('uploaded_file',
                                        filename=filename))
  elif request.method == 'GET':
    return render_template('upload.html', form=form)
 

                 
@app.route('/download')
def download():
    return render_template('download.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
 
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
        msg = Message(form.subject.data, sender='yeastmine@gmail.com', recipients=['yeastmine@gmail.com'])
        msg.body = """
        From: %s <%s>
        Affiliation: %s
        Field(s) of Interest: %s
        Message: %s
        """ % (form.name.data, form.email.data, form.affiliation.data, form.fieldofinterest.data, form.message.data)
        mail.send(msg)
        return render_template('contact_success.html')
 
  elif request.method == 'GET':
    return render_template('contact.html', form=form)
  

  
