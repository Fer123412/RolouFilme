from django import forms
from .models import Review, Comentario

class ReviewForm(forms.ModelForm):
    nota_review = forms.IntegerField(
        min_value=1,
        max_value=5,
        label='Nota (1 a 5)'
    )

    class Meta:
        model = Review
        fields = ['nota_review',
                  'texto_review', 
                  'contem_spoiler'
                  ]

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto_comentario']
