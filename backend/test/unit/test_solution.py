import pytest
import unittest.mock as mock

from src.controllers.recipecontroller import RecipeController
from src.static.diets import Diet,from_string

@pytest.fixture
def sut(recipe_readiness: dict):
    magic_dao = mock.MagicMock()
    magic_dao.get_readiness_of_recipes.return_value = recipe_readiness
    magic_dao.load_recipes.return_value = {0: "Banana Bread", 1: "Pancakes"}

    sut = RecipeController(items_dao = magic_dao)
    return sut

@pytest.mark.unit
@pytest.mark.parametrize('recipe_readiness, expected',[({"Banana Bread": 0.9, "Pancakes": 0.1}, "Banana Bread")])
def test_take_best_recipe(sut, expected):
    diet = from_string("normal")
    result = sut.get_recipe(diet=diet,take_best=True)
    assert result == expected

@pytest.mark.unit
@pytest.mark.parametrize('recipe_readiness, expected',[({"Banana Bread": 0.9, "Pancakes": 0.1}, ["Banana Bread","Pancakes"])])
def test_take_random(sut, expected):
    diet = from_string("normal")
    result = sut.get_recipe(diet=diet,take_best=False)
    assert result in expected

@pytest.mark.unit
@pytest.mark.parametrize('recipe_readiness, expected',[({}, None)])
def test_no_recipes(sut, expected):
    diet = from_string("normal")
    result = sut.get_recipe(diet=diet,take_best=True)
    assert result == expected

@pytest.mark.unit
@pytest.mark.parametrize('recipe_readiness, expected',[({"Banana Bread": 0}, None)])
def test_readiness_low(sut, expected):
    diet = from_string("normal")
    result = sut.get_recipe(diet=diet,take_best=True)
    assert result == expected