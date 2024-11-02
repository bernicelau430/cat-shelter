from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import string
from datetime import datetime

# Configuration
app = Flask(__name__, template_folder='interface')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@localhost/cat_shelter'
db = SQLAlchemy(app)

# Database Models
class Cat(db.Model):
    # Cat table with columns for ID, Name, Birthday, Gender, DateArrived, and Adopted status
    ID = db.Column(db.String(5), primary_key=True, unique=True)
    Name = db.Column(db.String(255))
    Birthday = db.Column(db.Date)
    Gender = db.Column(db.String(10))
    DateArrived = db.Column(db.Date)
    Adopted = db.Column(db.String(3), default='No')

class Age(db.Model):
    # Age table with columns for ID, Birthday, Age, and CatID (foreign key to Cat table)
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Birthday = db.Column(db.Date)
    Age = db.Column(db.Integer)
    CatID = db.Column(db.String(5), db.ForeignKey('cat.ID'))

class AgeRange(db.Model):
    # AgeRange table with columns for ID, Age, Age_Range, and AgeID (foreign key to Age table)
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Age = db.Column(db.Integer)
    Age_Range = db.Column(db.String(10))
    AgeID = db.Column(db.Integer, db.ForeignKey('age.ID'))

class Applicant(db.Model):
    # Applicant table with columns for ID, Name, and Email
    ID = db.Column(db.String(5), primary_key=True, unique=True)
    Name = db.Column(db.String(255))
    Email = db.Column(db.String(255))

class Adopter(db.Model):
    # Adopter table with columns for ID, ApplicantID (foreign key to Applicant table), and CatID (foreign key to Cat table)
    ID = db.Column(db.String(5), primary_key=True, unique=True)
    ApplicantID = db.Column(db.String(5), db.ForeignKey('applicant.ID'))
    CatID = db.Column(db.String(5), db.ForeignKey('cat.ID'))

# Function to generate a random ID
def generate_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

@app.route('/')
def index():
    # Route for the home page
    query = request.args.get('query')
    extended_view = request.args.get('extended_view', 'false').lower() == 'true'
    
    adopters = []
    cats = []
    
    if query:
        # Try to parse the query as a date
        try:
            query_date = datetime.strptime(query, '%Y-%m-%d').date()
        except ValueError:
            query_date = None
        
        # Query for adopters based on the search query
        adopters = db.session.query(Adopter, Applicant, Cat, Age, AgeRange).join(Applicant, Adopter.ApplicantID == Applicant.ID).join(Cat, Adopter.CatID == Cat.ID).outerjoin(Age, Cat.ID == Age.CatID).outerjoin(AgeRange, Age.ID == AgeRange.AgeID).filter(
            (Adopter.ID.like(f'%{query}%')) |
            (Applicant.ID.like(f'%{query}%')) |
            (Applicant.Name.like(f'%{query}%')) |
            (Cat.ID.like(f'%{query}%')) |
            (AgeRange.Age_Range.like(f'%{query}%'))
        ).all()
        
        # Query for cats based on the search query
        cats_query = db.session.query(Cat, Age, AgeRange).outerjoin(Age, Cat.ID == Age.CatID).outerjoin(AgeRange, Age.ID == AgeRange.AgeID)
        
        if query_date:
            cats_query = cats_query.filter(Cat.Birthday == query_date)
        else:
            cats_query = cats_query.filter(
                (Cat.ID.like(f'%{query}%')) |
                (Cat.Name.like(f'%{query}%')) |
                (Cat.Birthday.like(f'%{query}%')) |
                (Age.Age.like(f'%{query}%')) |
                (AgeRange.Age_Range.like(f'%{query}%'))
            )
        
        cats = cats_query.all()
        
        return render_template('index.html', adopters=adopters, cats=cats, extended_view=extended_view, is_adopter_query=bool(adopters), is_cat_query=bool(cats))
    else:
        # Query for all cats if no search query is provided
        cats = db.session.query(Cat, Age, AgeRange).outerjoin(Age, Cat.ID == Age.CatID).outerjoin(AgeRange, Age.ID == AgeRange.AgeID).all()
        return render_template('index.html', cats=cats, extended_view=extended_view, is_adopter_query=False, is_cat_query=bool(cats))

@app.route('/new_cat', methods=['GET', 'POST'])
def new_cat():
    # Route for adding a new cat
    if request.method == 'POST':
        cat_id = generate_id()
        name = request.form['name']
        birthday = datetime.strptime(request.form['birthday'], '%Y-%m-%d')
        gender = request.form['gender']
        date_arrived = datetime.strptime(request.form['date_arrived'], '%Y-%m-%d')
        age = (datetime.now() - birthday).days // 365
        age_range = 'Kitten' if age <= 1 else 'Young' if age <= 2 else 'Adult'
        
        new_cat = Cat(ID=cat_id, Name=name, Birthday=birthday, Gender=gender, DateArrived=date_arrived)
        
        # Commit the Cat record first
        db.session.add(new_cat)
        db.session.commit()
        
        new_age = Age(Birthday=birthday, Age=age, CatID=cat_id)
        db.session.add(new_age)
        db.session.commit()
        
        new_age_range = AgeRange(Age=age, Age_Range=age_range, AgeID=new_age.ID)
        
        # Commit the AgeRange record
        db.session.add(new_age_range)
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template('new_cat.html', cat_id=generate_id())

@app.route('/adoption', methods=['GET', 'POST'])
def adoption():
    # Route for processing an adoption
    adopter_id = generate_id()  # Generate adopter_id here to use it in both form and database insertion
    applicant_id = generate_id()  # Generate applicant_id here to use it in both form and database insertion
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cat_id = request.form['cat_id']
        
        new_applicant = Applicant(ID=applicant_id, Name=name, Email=email)
        
        # Commit the Applicant record first
        db.session.add(new_applicant)
        db.session.commit()
        
        new_adopter = Adopter(ID=adopter_id, ApplicantID=applicant_id, CatID=cat_id)
        
        # Commit the Adopter record
        db.session.add(new_adopter)
        
        # Update the Adopted status of the cat
        cat = Cat.query.get(cat_id)
        cat.Adopted = 'Yes'
        
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template('adoption.html', adopter_id=adopter_id, applicant_id=applicant_id)

if __name__ == '__main__':
    # Create all tables and run the app
    with app.app_context():
        db.create_all()
    app.run(debug=True)