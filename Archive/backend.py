# sort_contents(listof(Dict)) -> Listof(Dict)
# Takes a list of json objects that have been converted to dict form and sorts them
# By number
def sort_contents(json_list):
    sorted_list = sorted(json_list, key=lambda val: int(val['content']))
    return sorted_list
