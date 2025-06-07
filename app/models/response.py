from app.models import db

class Response(db.Model):
    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete="CASCADE"), nullable=False)
    is_agree = db.Column(db.Boolean, nullable=False)  # True if agree, False if disagree
    response = db.Column(db.String(255), nullable=False)
    question = db.relationship('Question', back_populates='responses', lazy=True)

    def __repr__(self):
        return f'Response text: {self.text}'