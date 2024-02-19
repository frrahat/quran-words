from app.taraweeh_ayat import get_start_end_ayah_by_night, AyahInfo


def test_get_start_end_ayah_by_night_returns_properly():
    assert get_start_end_ayah_by_night(2) == (AyahInfo(2, 204), AyahInfo(3, 91))


def test_get_start_end_ayah_by_night_does_not_break():
    for day in range(-30, 31):
        get_start_end_ayah_by_night(day)
