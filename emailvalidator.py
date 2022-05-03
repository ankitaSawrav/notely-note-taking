import re


def isValidEmail(email):
    check_emailfor_atrate_symbol = email.split("@")
    atrate_count = int(email.count('@'))
    # check for @ present only once
    # It has exactly one @ symbol
    if atrate_count != 1:
        
        # print('It has exactly one @ symbol')
        return False
        # check for . present at least
    # It has at least one .    
    dot_count = email.count(".")
    if dot_count == 0:
        # print ("It has at least one .")
        return False
# There is at least one . following the @ symbol   
    if '.' not in check_emailfor_atrate_symbol[1]:
        # print("There is at least one . following the @ symbol ")
        return False  
# There is at least one character before the @  
    length_of_list_one_after_atsplit = len(check_emailfor_atrate_symbol[0])  
    if length_of_list_one_after_atsplit == 0:
        # print("There is at least one character before the @ ")
        return False
# There is at least one character between the @ and .
    result_email_split_at_and_dot = re.split(r"@|\.", email)
    # print(result)
    # print(result[1])
    if len(result_email_split_at_and_dot[1])==0:
        # print("Check : There is at least one character between the @ and .")
        return False
    # There is at least one character after the final .
    if len(result_email_split_at_and_dot[2])==0:
        # print("Check :There is at least one character after the final .")
        return False
    return True
            
        
            
        