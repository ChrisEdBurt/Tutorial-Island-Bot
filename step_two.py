"""
Step two file.

Generating a username from dinopass

an_name is alpha numeric name
name is only alpha


"""

# Step Two Choose Account Name -------------------------------------------------------------------------------------------------

import requests


def generate_username():
    uri = 'https://www.dinopass.com/password/simple'
    r = requests.get(uri)
    an_name = r.text
    name = ''.join(filter(str.isalpha, an_name))

    return an_name, name


# For testing
#t1, t2 = generate_username()
#print(t1)
#print(t2)