from typedispatch import *

# This will find all of the phone numbers in the input
# automagically using regex.
@dispatch(regexmulti(r'(\d{3})\D{0,2}(\d{3})\D?(\d{4})'))
def phone_numbers(phone_numbers):
    for match in phone_numbers:
        print '-'.join(match.groups())


@dispatch()
def phone_numbers(text):
    print "Could not find a phone number :-("


@dispatch([regexsingle(r'(ab+)'), str])
def rewrite_in_list(arg):
    match, title = arg
    print title
    print match.groups()[0]
