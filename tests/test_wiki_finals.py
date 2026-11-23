from pathlib import Path

from pipeline.estafet.wiki_finals import infer_scoring_system, parse_finals, parse_score

FIXTURE = Path(__file__).parent / "fixtures" / "player_finals_sample.html"


def test_parse_score_flags():
    s = parse_score("15–11 5–15 7–1 retired")
    assert s["games"] == [(15, 11), (5, 15), (7, 1)]
    assert s["retired"] and not s["walkover"]
    assert parse_score("Walkover")["walkover"]


def test_scoring_system():
    assert infer_scoring_system([(15, 3), (15, 7)]) == "side_out_15"
    assert infer_scoring_system([(7, 5), (0, 7), (7, 1), (1, 7), (7, 4)]) == "side_out_7x5"
    assert infer_scoring_system([(26, 28), (21, 17), (21, 14)]) == "rally_21"
    assert infer_scoring_system([(11, 5), (11, 8)]) == "side_out_11"
    # retired: the unfinished last game is ignored
    assert infer_scoring_system([(15, 11), (5, 15), (7, 1)], retired=True) == "side_out_15"
    assert infer_scoring_system([]) == "unknown"


def test_parse_finals_fixture():
    df = parse_finals(FIXTURE.read_text(), source_url="https://example.org")
    assert len(df) == 6  # performance timeline is skipped
    wc = df[df["subsection"] == "World Championships"]
    assert list(wc["year"]) == [2001, 2005]
    assert wc.iloc[0]["retired"]
    gp = df[df["section"] == "BWF Grand Prix"]
    assert list(gp["year"]) == [2001, 2001, 2010]  # rowspan carried down
    assert gp.iloc[0]["scoring_system"] == "side_out_7x5"
    assert gp.iloc[0]["subsection"] == ""
    assert df[df["subsection"] == "World Cup"].iloc[0]["walkover"]
