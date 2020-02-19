from django import forms


class ContactForm(forms.Form):
    # bootstrap is handling email style verification
    sender = forms.CharField(required=False,
                             label='Contact (Optional)',
                             widget=forms.TextInput(
                                attrs={
                                    'type': "email",
                                    'class': "form-control",
                                    'name': "sender",
                                    'placeholder': "name@example.com"
                                        }
                                                    )
                            )
    message = forms.CharField(
                            label='Message',
                            widget=forms.Textarea(
                                            attrs=
                                                {
                                                    'label': 'Message',
                                                    'class': "form-control",
                                                    'name': "message",
                                                    'rows': "4",
                                                    'required': 'required'
                                                }
                                            )
                            )
