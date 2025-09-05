from django import forms


class NoDefaultValuesMixin:
    """
    Mixin to prevent default values in forms.
    Override form initialization to ensure no default values are set.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._clear_default_values()
    
    def _clear_default_values(self):
        """Clear any default values from form fields"""
        for field_name, field in self.fields.items():
            if hasattr(field, 'initial') and field.initial:
                field.initial = None
            
            # Clear widget values
            if hasattr(field, 'widget') and hasattr(field.widget, 'attrs'):
                if 'value' in field.widget.attrs:
                    del field.widget.attrs['value']
            
            # Ensure no placeholder values are treated as defaults
            if hasattr(field, 'widget') and hasattr(field.widget, 'attrs'):
                if 'placeholder' in field.widget.attrs:
                    # Remove placeholder to prevent confusion with default values
                    del field.widget.attrs['placeholder']


class CleanFormsetMixin:
    """
    Mixin for formsets to ensure no default values are set.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._clear_formset_defaults()
    
    def _clear_formset_defaults(self):
        """Clear default values from all forms in the formset"""
        for form in self.forms:
            if hasattr(form, 'initial'):
                form.initial = {}
            
            # Clear field values
            for field_name, field in form.fields.items():
                if hasattr(field, 'initial') and field.initial:
                    field.initial = None
                
                # Clear widget values
                if hasattr(field, 'widget') and hasattr(field.widget, 'attrs'):
                    if 'value' in field.widget.attrs:
                        del field.widget.attrs['value']
                    if 'placeholder' in field.widget.attrs:
                        del field.widget.attrs['placeholder']


class ProductionSafeForm(NoDefaultValuesMixin, forms.ModelForm):
    """
    Base form class that prevents default values in production.
    Use this for all forms that should start clean.
    """
    pass


class ProductionSafeFormset(CleanFormsetMixin, forms.BaseFormSet):
    """
    Base formset class that prevents default values in production.
    Use this for all formsets that should start clean.
    """
    pass
