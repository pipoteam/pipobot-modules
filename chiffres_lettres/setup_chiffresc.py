from distutils.core import setup, Extension

module1 = Extension('chiffresc',
                    # See http://bugs.python.org/issue21121
                    extra_compile_args=["-Wno-error=declaration-after-statement"],
                    sources = ['chiffres.c'])

setup (name = 'chiffresc',
       version = '1.0',
       description = 'Implementation of the chiffres algorithm in C for better performance',
       ext_modules = [module1])
