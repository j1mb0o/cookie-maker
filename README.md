#  Genetric Cookie-Maker

## Setup
Using conda create a virtual environment.

```bash
conda create -n [NAME] python=3.11
```

To install the required packages:
```bash
conda activate [NAME]
pip install -r requirements.txt 
```

## Project structure
In the directory  `presentation` are the images created using 
stable diffusion for the image representation of the cookies, as well as
the cookbook in a pdf format.

To generate new cookie recipe run the `recipe_generator.py`, which will
then create the recipes, generate a name, calculate the creativity score,
and save the new recipes in a json file named `cretive_recipes.json`

The main files that are being used to generate new recipes are:
`const.py`, `cretivity_evaluation.py`,`genetic_algo.py`,`recipes_expanded.json`. 
The rest of the files are purely supportive and their scope is to create the
inpiring set which is `recipes_expanded.json`

## Important Files Description
* `recipe_generator.py` : the main file for the generation of new recipes, name and creativity score.
* `genetic_algo.py` : has all the genetic algorithm code to create the new recipes.
* `creativity_evaluation.py` : given a recipe returns a score on how novel/creative is a generated recipe
* `const.py` : contains constant values for the ingredients
* `recipes_expanded.json` : inspiring set
