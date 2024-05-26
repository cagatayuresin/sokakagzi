from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def total_votes(explanation):
    return explanation.total_up_votes - explanation.total_down_votes
