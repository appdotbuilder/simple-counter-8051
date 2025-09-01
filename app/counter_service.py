from datetime import datetime
from sqlmodel import select
from app.database import get_session
from app.models import Counter


class CounterService:
    """Service layer for counter operations."""

    @staticmethod
    def get_or_create_counter(name: str = "default") -> Counter:
        """Get existing counter by name or create a new one."""
        with get_session() as session:
            statement = select(Counter).where(Counter.name == name)
            counter = session.exec(statement).first()

            if counter is None:
                counter = Counter(name=name, value=0)
                session.add(counter)
                session.commit()
                session.refresh(counter)

            return counter

    @staticmethod
    def get_counter_value(name: str = "default") -> int:
        """Get current counter value."""
        counter = CounterService.get_or_create_counter(name)
        return counter.value

    @staticmethod
    def increment_counter(name: str = "default") -> int:
        """Increment counter by 1 and return new value."""
        with get_session() as session:
            statement = select(Counter).where(Counter.name == name)
            counter = session.exec(statement).first()

            if counter is None:
                counter = Counter(name=name, value=1)
                session.add(counter)
            else:
                counter.value += 1
                counter.updated_at = datetime.utcnow()

            session.commit()
            session.refresh(counter)
            return counter.value

    @staticmethod
    def decrement_counter(name: str = "default") -> int:
        """Decrement counter by 1 and return new value."""
        with get_session() as session:
            statement = select(Counter).where(Counter.name == name)
            counter = session.exec(statement).first()

            if counter is None:
                counter = Counter(name=name, value=-1)
                session.add(counter)
            else:
                counter.value -= 1
                counter.updated_at = datetime.utcnow()

            session.commit()
            session.refresh(counter)
            return counter.value

    @staticmethod
    def reset_counter(name: str = "default") -> int:
        """Reset counter to 0 and return new value."""
        with get_session() as session:
            statement = select(Counter).where(Counter.name == name)
            counter = session.exec(statement).first()

            if counter is None:
                counter = Counter(name=name, value=0)
                session.add(counter)
            else:
                counter.value = 0
                counter.updated_at = datetime.utcnow()

            session.commit()
            session.refresh(counter)
            return counter.value
