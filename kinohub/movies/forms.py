from django import forms


class SearchForm(forms.Form):
    title = forms.CharField(
        label="Назва",
        max_length=120,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    year = forms.IntegerField(
        label="Рік",
        max_value=2026,
        min_value=1920,
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    min_imdb_rating = forms.DecimalField(
        label="Мінімальний IMDB",
        min_value=1,
        max_value=10,
        decimal_places=1,
        max_digits=3,
        initial=5,
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "step": "0.1",
            }
        ),
    )
    genres = forms.ChoiceField(
        label="Жанр",
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def __init__(self, *args, genres=None, **kwargs):
        super().__init__(*args, **kwargs)

        choices = [("", "All")]
        if genres:
            choices += [(g.name, g.name) for g in genres]

        self.fields["genres"].choices = choices
