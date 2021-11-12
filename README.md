# Wiki

This is a wiki style encyclopedia site created using the django framwwork in python. 

Each entry has it's own address in the form of wiki/entry-title

It allows users to add their own entry pages inputting the text in markdown language for easy formatting.

When any wiki entry is displayed it is then converted into html using python-markdown2 package to perform this conversion, installable via pip3 install markdown2. Credit to https://github.com/trentm/python-markdown2

The user can search for entries which match or contain a string or their choosing.
They can also click on the random button to be directed to a random entry page.

Once on an entry page they can also edit the entry, saving their changes.