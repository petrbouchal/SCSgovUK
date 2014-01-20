import gzip

__author__ = 'petrbouchal'



s = input("Please enter the text you want to compress")
fn = input("Please enter the desired filename")
with gzip.open(fn+".gz","wb") as f_out:
    f_out.write(bytes(s, 'UTF-8'))