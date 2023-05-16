from django.forms import widgets

class CustomSelect(widgets.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        if value == '---':
            option['attrs'] = {'disabled': True, 'selected': True}
        return option