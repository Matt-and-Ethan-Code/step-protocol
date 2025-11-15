from django import template 

register = template.Library()

@register.filter 
def get_item(form, key):
    print("form: ", form, "key: ", key)
    return form[key]