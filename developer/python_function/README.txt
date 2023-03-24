In order to generate the slides from the .ipynb, please use the next bash commands:

# jupyter nbconvert --to slides scripts/Python_functions_overview.ipynb --output-dir=exports  # To create the slides.
# jupyter nbconvert --to script scripts/Python_functions_overview.ipynb --output-dir=exports  # To get the scripts
# jupyter nbconvert --to pdf scripts/Python_functions_overview.ipynb --output-dir=exports  # For the PDF
# jupyter nbconvert --to script scripts/Coupling_tools.ipynb --output-dir=exports
# jupyter nbconvert --to script scripts/Parametric_function.ipynb --output-dir=exports
# jupyter nbconvert --to script scripts/Python_function_exercises.ipynb --output-dir=exports
# jupyter nbconvert --to script scripts/Symbolic_function.ipynb --output-dir=exports

In order to build the PDF of the LaTeX slides, please run the next bash commands:

pdflatex python_function
pdflatex python_function
