import pytest
from nicegui.testing import User
from app.database import reset_db


@pytest.fixture()
def new_db():
    reset_db()
    yield
    reset_db()


async def test_counter_page_loads(user: User, new_db) -> None:
    """Test that counter page loads with initial display."""
    await user.open("/counter")

    # Check that page content is present
    await user.should_see("Counter Application")
    await user.should_see("0")  # Initial counter value


async def test_increment_functionality(user: User, new_db) -> None:
    """Test increment button functionality."""
    await user.open("/counter")

    # Initial value should be 0
    await user.should_see("0")

    # Click increment button multiple times
    user.find("+").click()
    await user.should_see("1")

    user.find("+").click()
    await user.should_see("2")

    user.find("+").click()
    await user.should_see("3")


async def test_decrement_functionality(user: User, new_db) -> None:
    """Test decrement button functionality."""
    await user.open("/counter")

    # Initial value should be 0
    await user.should_see("0")

    # Click decrement button - should go to -1
    user.find("−").click()
    await user.should_see("-1")

    # Click decrement again - should go to -2
    user.find("−").click()
    await user.should_see("-2")


async def test_mixed_increment_decrement(user: User, new_db) -> None:
    """Test mixed increment and decrement operations."""
    await user.open("/counter")

    # Start with increment to 2
    user.find("+").click()
    user.find("+").click()
    await user.should_see("2")

    # Decrement once to 1
    user.find("−").click()
    await user.should_see("1")

    # Increment again to 2
    user.find("+").click()
    await user.should_see("2")

    # Decrement three times to -1
    user.find("−").click()
    user.find("−").click()
    user.find("−").click()
    await user.should_see("-1")


async def test_reset_functionality(user: User, new_db) -> None:
    """Test reset button functionality."""
    await user.open("/counter")

    # Increment to some value
    user.find("+").click()
    user.find("+").click()
    user.find("+").click()
    await user.should_see("3")

    # Reset to 0
    user.find("Reset").click()
    await user.should_see("0")

    # Try reset from negative value
    user.find("−").click()
    user.find("−").click()
    await user.should_see("-2")

    user.find("Reset").click()
    await user.should_see("0")


async def test_home_page_navigation(user: User, new_db) -> None:
    """Test navigation from home page to counter."""
    await user.open("/")

    # Check home page content
    await user.should_see("Welcome to the Counter App")
    await user.should_see("Open Counter")

    # Click navigation button
    user.find("Open Counter").click()

    # Should be on counter page now
    await user.should_see("Counter Application")
    await user.should_see("0")  # Initial counter value


async def test_counter_persistence(user: User, new_db) -> None:
    """Test that counter value persists across page visits."""
    await user.open("/counter")

    # Increment counter to 5
    for _ in range(5):
        user.find("+").click()
    await user.should_see("5")

    # Navigate away and back
    await user.open("/")
    await user.open("/counter")

    # Counter should still show 5
    await user.should_see("5")

    # Modify it further
    user.find("−").click()
    user.find("−").click()
    await user.should_see("3")


async def test_counter_ui_elements_present(user: User, new_db) -> None:
    """Test that UI elements are properly present."""
    await user.open("/counter")

    # Verify all key UI elements exist
    await user.should_see("Counter Application")
    await user.should_see("Click + to increment, − to decrement, or Reset to start over")

    # Verify buttons are present
    await user.should_see("+")
    await user.should_see("−")
    await user.should_see("Reset")
