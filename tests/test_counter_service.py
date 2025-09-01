import pytest
from app.counter_service import CounterService
from app.database import reset_db, get_session
from app.models import Counter
from sqlmodel import select


@pytest.fixture()
def new_db():
    reset_db()
    yield
    reset_db()


def test_get_or_create_counter_new(new_db):
    """Test creating a new counter when none exists."""
    counter = CounterService.get_or_create_counter("test_counter")

    assert counter.name == "test_counter"
    assert counter.value == 0
    assert counter.id is not None
    assert counter.created_at is not None
    assert counter.updated_at is not None


def test_get_or_create_counter_existing(new_db):
    """Test retrieving an existing counter."""
    # Create first counter
    counter1 = CounterService.get_or_create_counter("existing")
    original_id = counter1.id

    # Get same counter again
    counter2 = CounterService.get_or_create_counter("existing")

    assert counter2.id == original_id
    assert counter2.name == "existing"
    assert counter2.value == 0


def test_get_counter_value_new(new_db):
    """Test getting value of non-existent counter creates it with 0."""
    value = CounterService.get_counter_value("new_counter")
    assert value == 0

    # Verify it was actually created
    with get_session() as session:
        statement = select(Counter).where(Counter.name == "new_counter")
        counter = session.exec(statement).first()
        assert counter is not None
        assert counter.value == 0


def test_get_counter_value_existing(new_db):
    """Test getting value of existing counter."""
    # Create counter with specific value
    counter = CounterService.get_or_create_counter("test")
    with get_session() as session:
        statement = select(Counter).where(Counter.name == "test")
        counter = session.exec(statement).first()
        if counter is not None:
            counter.value = 42
            session.commit()

    value = CounterService.get_counter_value("test")
    assert value == 42


def test_increment_counter_new(new_db):
    """Test incrementing a non-existent counter creates it with value 1."""
    value = CounterService.increment_counter("new_inc")
    assert value == 1

    # Verify in database
    with get_session() as session:
        statement = select(Counter).where(Counter.name == "new_inc")
        counter = session.exec(statement).first()
        assert counter is not None
        assert counter.value == 1


def test_increment_counter_existing(new_db):
    """Test incrementing an existing counter."""
    # Create counter
    CounterService.get_or_create_counter("inc_test")

    # Increment multiple times
    value1 = CounterService.increment_counter("inc_test")
    assert value1 == 1

    value2 = CounterService.increment_counter("inc_test")
    assert value2 == 2

    value3 = CounterService.increment_counter("inc_test")
    assert value3 == 3


def test_decrement_counter_new(new_db):
    """Test decrementing a non-existent counter creates it with value -1."""
    value = CounterService.decrement_counter("new_dec")
    assert value == -1

    # Verify in database
    with get_session() as session:
        statement = select(Counter).where(Counter.name == "new_dec")
        counter = session.exec(statement).first()
        assert counter is not None
        assert counter.value == -1


def test_decrement_counter_existing(new_db):
    """Test decrementing an existing counter."""
    # Create counter and set initial value
    counter = CounterService.get_or_create_counter("dec_test")
    with get_session() as session:
        statement = select(Counter).where(Counter.name == "dec_test")
        counter = session.exec(statement).first()
        if counter is not None:
            counter.value = 5
            session.commit()

    # Decrement multiple times
    value1 = CounterService.decrement_counter("dec_test")
    assert value1 == 4

    value2 = CounterService.decrement_counter("dec_test")
    assert value2 == 3

    value3 = CounterService.decrement_counter("dec_test")
    assert value3 == 2


def test_decrement_below_zero(new_db):
    """Test that counter can go below zero."""
    CounterService.get_or_create_counter("negative_test")

    value1 = CounterService.decrement_counter("negative_test")
    assert value1 == -1

    value2 = CounterService.decrement_counter("negative_test")
    assert value2 == -2


def test_reset_counter_new(new_db):
    """Test resetting a non-existent counter creates it with value 0."""
    value = CounterService.reset_counter("new_reset")
    assert value == 0

    # Verify in database
    with get_session() as session:
        statement = select(Counter).where(Counter.name == "new_reset")
        counter = session.exec(statement).first()
        assert counter is not None
        assert counter.value == 0


def test_reset_counter_existing(new_db):
    """Test resetting an existing counter to 0."""
    # Create counter and increment it
    CounterService.increment_counter("reset_test")
    CounterService.increment_counter("reset_test")
    CounterService.increment_counter("reset_test")

    # Verify it has value 3
    assert CounterService.get_counter_value("reset_test") == 3

    # Reset counter
    value = CounterService.reset_counter("reset_test")
    assert value == 0

    # Verify it's actually 0
    assert CounterService.get_counter_value("reset_test") == 0


def test_multiple_counters(new_db):
    """Test that different counter names maintain separate values."""
    # Create and modify different counters
    CounterService.increment_counter("counter1")
    CounterService.increment_counter("counter1")

    CounterService.increment_counter("counter2")
    CounterService.increment_counter("counter2")
    CounterService.increment_counter("counter2")

    # Verify they have different values
    assert CounterService.get_counter_value("counter1") == 2
    assert CounterService.get_counter_value("counter2") == 3

    # Modify one, verify the other is unchanged
    CounterService.reset_counter("counter1")
    assert CounterService.get_counter_value("counter1") == 0
    assert CounterService.get_counter_value("counter2") == 3


def test_counter_updated_at_changes(new_db):
    """Test that updated_at timestamp changes when counter is modified."""
    counter1 = CounterService.get_or_create_counter("timestamp_test")
    original_updated_at = counter1.updated_at

    # Small delay to ensure timestamp difference
    import time

    time.sleep(0.01)

    # Increment counter
    CounterService.increment_counter("timestamp_test")

    # Get counter again and verify updated_at changed
    counter2 = CounterService.get_or_create_counter("timestamp_test")
    assert counter2.updated_at > original_updated_at


def test_default_counter_name(new_db):
    """Test that default counter name works correctly."""
    # Test with default name
    value1 = CounterService.increment_counter()
    assert value1 == 1

    value2 = CounterService.get_counter_value()
    assert value2 == 1

    value3 = CounterService.decrement_counter()
    assert value3 == 0
