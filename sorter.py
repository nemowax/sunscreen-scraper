import operator

# TODO: Figure out how to share dictionary from scraper.py to sorter.py
def ascendingPrice(products_list):
    sorted_list = sorted(products_list, key = operator.itemgetter('price'))
    return sorted_list

def descendingPrice(products_list):
    sorted_list = sorted(products_list, key = operator.itemgetter('price'), reverse=True)
    return sorted_list

# TODO: Select all products with no homosalate, no pg, no ppdl

# TODO: Select all products with no pg, no ppdl

# TODO: Sort products by increasing homosalate percentage.