from app.taraweeh_ayat import get_start_end_ayah_by_day, AyahInfo


def test_get_start_end_ayah_by_day_returns_properly():
    assert get_start_end_ayah_by_day(2) == (AyahInfo(2, 204), AyahInfo(3, 91))


def test_get_start_end_ayah_by_day_does_not_break():
    for day in range(-30, 31):
        get_start_end_ayah_by_day(day)
