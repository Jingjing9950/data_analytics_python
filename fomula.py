parameter = {"a1":10,"b":45,"c":23,"d":20,"e1":19}

def input_fomula(fomula_string):
    # fomula_list = list(fomula_string)
    # for i in range(len(fomula_list)):
    #     key_value = fomula_list[i]
    #     if key_value in parameter.keys():
    #         fomula_list[i] = parameter[key_value]
    # fomula_list = map(str,fomula_list)
    # list_to_string = "".join(fomula_list)
    #
    # keys_list = parameter.keys()
    # for j in range(len(keys_list)):
    #     if list_to_string.find()
    fomula_string_copy = fomula_string
    start_quote = 0
    while start_quote != -1 :
        start_quote = fomula_string_copy.find("|")
        end_quote = fomula_string_copy.find("|", start_quote+1)
        variable_value = fomula_string_copy[start_quote+1:end_quote]
        if variable_value in parameter.keys():
            fomula_string = fomula_string.replace(variable_value,str(parameter[variable_value]))
        if end_quote == -1:
            break
        fomula_string_copy = fomula_string_copy[end_quote:]
    fomula_string = fomula_string.replace("|","")
    result = eval(fomula_string)
    return fomula_string, result

print(input_fomula("(|a1|+|c|)/2"))

