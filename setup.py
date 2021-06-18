import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='intpy',  
     version='0.1',
     scripts=['intpy/intpy.py'] ,
     author="UFF",
     author_email="uff@id.uff.br",
     description="",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/claytonchagas/intpy_dev",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
     ]
 )
