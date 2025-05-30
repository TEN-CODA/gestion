"""add note parameters to ecoles table

Revision ID: add_note_parameters
Revises: 
Create Date: 2024-03-19

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'add_note_parameters'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Ajouter les colonnes pour les paramètres de notes
    op.add_column('ecoles', sa.Column('coefficients_notes', mysql.JSON, nullable=True))
    op.add_column('ecoles', sa.Column('seuils_appreciation', mysql.JSON, nullable=True))
    
    # Définir les valeurs par défaut
    default_seuils = {
        'Excellent': 16,
        'Très bien': 14,
        'Bien': 12,
        'Assez bien': 10,
        'Passable': 8
    }
    
    # Mettre à jour les enregistrements existants
    op.execute(f"""
        UPDATE ecoles 
        SET coefficients_notes = JSON_OBJECT(),
            seuils_appreciation = JSON_OBJECT(
                'Excellent', 16,
                'Très bien', 14,
                'Bien', 12,
                'Assez bien', 10,
                'Passable', 8
            )
    """)

def downgrade():
    # Supprimer les colonnes
    op.drop_column('ecoles', 'coefficients_notes')
    op.drop_column('ecoles', 'seuils_appreciation') 