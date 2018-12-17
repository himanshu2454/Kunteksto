
# Create models
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    path = db.Column(db.Unicode(128))

    def __unicode__(self):
        return self.name


class Datamodel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'))
    title = db.Column('Title', db.String(250), unique=True, nullable=False)
    description = db.Column('Description', db.Text, unique=False, nullable=False)
    copyright = db.Column('Copyright', db.String(250), unique=False, nullable=True)
    author = db.Column('Author', db.String(250), unique=False, nullable=False)
    definition_url = db.Column('Defining URL', db.String(500), unique=False, nullable=False)
    dmid = db.Column('Data Model ID', db.String(40), unique=True, nullable=False)
    dataid = db.Column('Data Cluster ID', db.String(40), unique=True, nullable=False)
    components = db.relationship('Component', backref='datamodel', lazy=True)
    
    def __repr__(self):
        return '<Data Model: %r>' % self.title
    

class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('datamodel.id'))
    model = db.relationship("Datamodel", back_populates="components")
    header = db.Column('CSV Column Header', db.String(100), unique=False, nullable=False)
    label = db.Column('Label Value', db.String(250), unique=False, nullable=False)
    datatype = db.Column('Datatype', db.String(10), unique=False, nullable=False)
    min_len = db.Column('Minimum Length', db.Integer, nullable=True)
    max_len = db.Column('Maximum Length', db.Integer, nullable=True)
    choices = db.Column('String Enumerations', db.Text, unique=False, nullable=True)
    regex = db.Column('Regular Expression', db.String(100), unique=False, nullable=True)
    min_incl = db.Column('Minimum Value (Inclusive)', db.String(100), unique=False, nullable=True)
    max_incl = db.Column('Maximum Value (Inclusive)', db.String(100), unique=False, nullable=True)
    min_excl = db.Column('Minimum Value (Exclusive)', db.String(100), unique=False, nullable=True)
    max_excl = db.Column('Maximum Value (Exclusive)', db.String(100), unique=False, nullable=True)
    description = db.Column('Description', db.Text, unique=False, nullable=False)
    definition_url = db.Column('Defining URL', db.String(500), unique=False, nullable=False)
    pred_obj = db.Column('List of predicate/object pairs', db.Text, unique=False, nullable=True)
    def_text = db.Column('Default Text', db.Text, unique=False, nullable=True)
    def_num = db.Column('Default Number', db.String(100), unique=False, nullable=True)
    units = db.Column('Units', db.String(50), unique=False, nullable=True)
    mcid = db.Column('Component ID', db.String(40), unique=True, nullable=False)
    adid = db.Column('Adapter ID', db.String(40), unique=True, nullable=False)

    def __repr__(self):
        return '<Component: %r>' % self.label
