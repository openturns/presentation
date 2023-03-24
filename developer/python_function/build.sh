# TODO : export .ipynb into pdf and html (RevealSlide)
jupyter nbconvert --to slides scripts/Python_functions_overview.ipynb --output-dir=exports
jupyter nbconvert --to script scripts/Python_functions_overview.ipynb --output-dir=exports
jupyter nbconvert --to pdf scripts/Python_functions_overview.ipynb --output-dir=exports
jupyter nbconvert --to script scripts/Coupling_tools.ipynb --output-dir=exports
jupyter nbconvert --to script scripts/Parametric_function.ipynb --output-dir=exports
jupyter nbconvert --to script scripts/Python_function_exercises.ipynb --output-dir=exports
jupyter nbconvert --to script scripts/Symbolic_function.ipynb --output-dir=exports
