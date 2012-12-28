from distutils.core import setup, Extension

module1 = Extension('chiffresc',
                    sources = ['chiffres.c'])

setup (name = 'chiffresc',
       version = '1.0',
       description = 'Implementation of the chiffres algorithm in C for better performance',
       ext_modules = [module1])
