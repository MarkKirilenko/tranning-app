"""
Простые базовые тесты для проверки работоспособности pytest.
"""

def test_addition():
    """Проверка сложения."""
    assert 1 + 1 == 2

def test_string_operations():
    """Проверка операций со строками."""
    assert "hello".upper() == "HELLO"
    assert len("test") == 4

def test_list_operations():
    """Проверка операций со списками."""
    numbers = [1, 2, 3, 4, 5]
    assert len(numbers) == 5
    assert sum(numbers) == 15
    assert 3 in numbers

def test_dict_operations():
    """Проверка операций со словарями."""
    data = {"name": "John", "age": 30}
    assert data["name"] == "John"
    assert "age" in data
    assert len(data) == 2

class TestSimpleMath:
    """Простые математические тесты."""
    
    def test_multiplication(self):
        """Тест умножения."""
        assert 2 * 3 == 6
        assert 5 * 0 == 0
        assert -1 * 4 == -4
    
    def test_division(self):
        """Тест деления."""
        assert 10 / 2 == 5
        assert 9 / 3 == 3
    
    def test_boolean_logic(self):
        """Тест булевой логики."""
        assert True is True
        assert False is False
        assert not False is True
        assert True or False is True
        assert True and True is True