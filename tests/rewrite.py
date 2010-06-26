from typedispatch import *

# This will find all of the phone numbers in the input
# automagically using regex.
@dispatch(regexmulti(r'(\d{3})\D{0,2}(\d{3})\D?(\d{4})'))
def phone_numbers(phone_numbers):
    # We found some phone numbers!
    for match in phone_numbers:
        print '-'.join(match.groups())


@dispatch()
def phone_numbers(text):
    print "Could not find a phone number :-("






# This just looks to see if the regex is inside the list.
@dispatch([regexsingle(r'(ab+)'), str])
def rewrite_in_list(arg):
    match, title = arg
    print title
    print match.groups()[0]
