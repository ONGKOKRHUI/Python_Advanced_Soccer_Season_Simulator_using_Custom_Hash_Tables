import datetime
import pytest

from enums import PlayerPosition
from data_structures import LinearProbeTable
from player import Player  # replace your_module with the actual module name


def test_constructor_and_attributes():
    # Create a 25-year-old striker
    p = Player(name="Alice", position=PlayerPosition.STRIKER, age=25)
    
    assert p.name == "Alice"
    # born_year should be current year minus age
    expected_born = datetime.datetime.now().year - 25
    assert p.born_year == expected_born
    assert p.position == PlayerPosition.STRIKER
    assert p.goals == 0
    # stats table should be an empty LinearProbeTable
    assert isinstance(p.stats, LinearProbeTable)
    assert list(p.stats.keys()) == []


def test_set_and_get_statistic():
    p = Player("Bob", PlayerPosition.DEFENDER, age=30)
    # set a new statistic
    p["tackles"] = 7
    assert p.stats["tackles"] == 7
    # __getitem__ should mirror stats lookup
    assert p["tackles"] == 7

    # overwrite the stat
    p["tackles"] = 10
    assert p["tackles"] == 10

    # set another stat
    p["clearances"] = 4
    assert p["clearances"] == 4


def test_reset_stats_preserves_keys_and_zeroes_values():
    p = Player("Carol", PlayerPosition.MIDFIELDER, age=22)
    # populate stats
    p["passes"] = 55
    p["shots"] = 12
    assert p["passes"] == 55 and p["shots"] == 12

    # reset
    p.reset_stats()
    # keys still present but values zero
    assert sorted(p.stats.keys()) == sorted(["passes", "shots"])
    assert p["passes"] == 0
    assert p["shots"] == 0


def test_get_age_updates_with_time(monkeypatch):
    # Freeze "now" to a known date
    fake_year = 2030
    class FakeDateTime(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(fake_year, 1, 1)
    monkeypatch.setattr(datetime, 'datetime', FakeDateTime)

    # Create with age 20 at fake_year
    p = Player("Dave", PlayerPosition.GOALKEEPER, age=20)
    # born_year should be 2030 - 20 = 2010
    assert p.born_year == fake_year - 20
    # get_age should return 20
    assert p.get_age() == 20

    # Advance a year
    class FakeDateTime2(FakeDateTime):
        @classmethod
        def now(cls, tz=None):
            return cls(fake_year + 1, 1, 1)
    monkeypatch.setattr(datetime, 'datetime', FakeDateTime2)
    assert p.get_age() == 21


def test_str_and_repr():
    p = Player("Eve", PlayerPosition.STRIKER, age=18)
    assert str(p) == "Eve"
    assert repr(p) == "Eve"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
