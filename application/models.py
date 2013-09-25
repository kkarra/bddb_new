from application import db
from sqlalchemy import and_, or_, not_ 

ROLE_USER = 0
ROLE_ADMIN = 1

class Species(db.Model):
    __tablename__ = 'species'
    species_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True, unique = True)
    ucsc_genome = db.Column(db.String(64), unique = True)
    genes = db.relationship('Genes', backref='species', lazy = 'dynamic')
    
    def __repr__(self):
        return '<name>'  % (self.name)
    
class Genes(db.Model):
    __tablename__ = 'genes'
    entrez_gene_id = db.Column(db.Integer, primary_key = True)
    symbol = db.Column(db.String(20))
    description = db.Column(db.String(300))
    species_id = db.Column(db.Integer, db.ForeignKey('species.species_id'))
    broad_peaks = db.relationship('BroadPeaks', backref='genes', lazy = 'dynamic')
    
    @property
    def gene_url(self):
        return "<a href=\'/search?entrezId=" + str(self.entrez_gene_id) +"\'>" + self.symbol+"</a>"
    
    @property
    def homolog(self):
        if (self.species.name == 'Homo sapiens'):  ## if gene is a human gene, return the mouse homolog ##
            
            homology_rel = db.relationship('Homology', backref='genes',
                                           primaryjoin = 'genes.entrez_gene_id == homology.human_id')
                                           
            return homology_rel.mouse_url
        
        elif (self.species.name == 'Mus musculus'):
            homology_rel = db.relationship('Homology', backref='genes',
                                           primaryjoin = 'genes.entrez_gene_id == homology.mouse_id')
            return homology_rel.human_url
        
        else:
            return "None"
       
    def __repr__(self):
       return '<gene_id>' %(self.entrez_gene_id) 
    
class BroadPeaks(db.Model):
    __tablename__ = 'broad_peaks'
    peak_id = db.Column(db.Integer, primary_key = True)
    gene_id = db.Column(db.Integer, db.ForeignKey('genes.entrez_gene_id'))
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.dataset_id'))
    tss_dist = db.Column(db.Integer)
    bd_length = db.Column(db.Integer)
    peak_name =  db.Column(db.String(20))
    extra =  db.Column(db.String(20))
    start_wrt_TSS =  db.Column(db.Integer)
    end_wrt_TSS =  db.Column(db.Integer)
    breadth_signal =  db.Column(db.Integer)
    dataset = db.relationship('Datasets', backref='broad_peaks')
     
    def __repr__(self):
        return '<tss_dist>' % (self.tss_dist)
    
class Datasets(db.Model):  
    __tablename__ = 'datasets'
    dataset_id = db.Column(db.Integer, primary_key = True)
    bio_sample = db.Column(db.String(20))
    bio_origin = db.Column(db.String(20))
    state = db.Column(db.String(20))
    treatment = db.Column(db.String(20))
    broad_cutoff = db.Column(db.Integer)
    peak_num = db.Column(db.Integer)
    species_id = db.Column(db.Integer, db.ForeignKey('species.species_id'))
    method_id = db.Column(db.Integer, db.ForeignKey('ip_method.method_id'))
    uberon_id = db.Column(db.Integer, db.ForeignKey('anatomy_ontology.uberon_id'))
    cancer = db.Column(db.Integer)
    
    method = db.relationship('IpMethod', backref='datasets')
    tissue = db.relationship('AnatomyOntology', backref='datasets')
    species = db.relationship('Species', backref='datasets')
  
    accession = db.relationship('DatasetsAccession', backref='datasets')

    def __repr__(self):
        return '<broad_cutoff>' % (self.broad_cutoff)

class DatasetsAccession(db.Model):  ## faked foreign key from dataset
    __tablename__='datasets_accession'
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.dataset_id'))
    accession = db.Column(db.String(20), primary_key = True)
    ac_type =  db.Column(db.String(20), unique = True)
 
    def __repr__(self):
        return '<accession>' % (self.accession)
 
class Homology(db.Model):
    __tablename__ = 'homology'
    human_id = db.Column(db.Integer)
    mouse_id =  db.Column(db.Integer)
    homologene_group_id = db.Column(db.Integer, primary_key=True)

    @property
    def mouse_url(self):
        return "<a href=\'http://www.ncbi.nlm.nih.gov/gene/" + str(self.mouse_id) +"\'>" + self.mouse_id+"</a>"
    @property
    def human_url(self):
        return "<a href=\'http://www.ncbi.nlm.nih.gov/gene/" + str(self.human_id) +"\'>" + self.human_id+"</a>"

    def __repr__(self):
        return '<homologene>' % (self.homologene_group_id)  
                        
class IpMethod(db.Model):
    __tablename__ = 'ip_method'
    method_id = db.Column(db.Integer, primary_key = True)
    wet_name = db.Column(db.String(20), unique = True)
    dry_name = db.Column(db.String(20), unique = True)
    input = db.Column(db.String(20), unique = True)
    
    @property
    def display_name(self):
        return self.wet_name + "-" + self.dry_name
    
    def __repr__(self):
        return '<wetname>' % (self.wet_name)
    
class AnatomyOntology(db.Model):
    __tablename__ = 'anatomy_ontology'
    uberon_id = db.Column(db.Integer, primary_key = True)
    uberon_term = db.Column(db.String(20), unique = True)
    uberon_description = db.Column(db.String(50), unique = True)
    
    def __repr__(self):
        return '<description>' % (self.uberon_description)
        
 
