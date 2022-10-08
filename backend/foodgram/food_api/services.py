
def generate_shopping_list(queryset):
    '''
    This function generates a list of ingredients
    contained in the selected recipes.
    '''
    shopping_data = dict()
    for item in queryset:
        ingredient_id = item.ingredient.id
        ingredient = item.ingredient
        measurement_unit = item.ingredient.measurement_unit
        amount = item.amount
        if ingredient_id in shopping_data.keys():
            shopping_data[ingredient_id]['amount'] += amount
        else:
            shopping_data[ingredient_id] = {'ingredient': ingredient,
                                            'measurement_unit':
                                            measurement_unit,
                                            'amount': amount
                                            }
    ingredients_list = (f'{value["ingredient"]}: {value["amount"]}'
                        f' {value["measurement_unit"]}'
                        for value in shopping_data.values())
    shopping_list = '\n'.join(ingredients_list)
    return shopping_list
