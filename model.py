# This function gets the table head and returns a list of all the fields in the table head row.
def get_table_head_fields_as_list(table_obj):
    result = []
    table_head = table_obj.find('thead')
    table_head_fields = table_head.find_all('th')
    for field_obj in table_head_fields:
        result.append(field_obj.getText().strip())
    return result

# This function gets the table body and return a list of rows with data fields.
def get_table_body_as_lists(table_obj):
    result = []
    table_body = table_obj.find('tbody')
    table_rows = table_body.find_all('tr')
    for row in table_rows:
        curr_row = []
        row_fields = row.find_all('td')
        for field_obj in row_fields:
            curr_row.append(field_obj.getText().strip())
        result.append(curr_row)
    return result