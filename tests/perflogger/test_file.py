import jsonlines
from pathlib import Path

from perflogger import PerfLogger

def test_file_writing(tmp_path):

    file_path = tmp_path / "test_file_writing.jsonl"
    file_path.unlink(missing_ok=True)
    reference_path = Path(__file__).parent / "reference_data" / "test_file_writing.jsonl"
    assert reference_path.exists()

    pl = PerfLogger(name="perflogger1", tick_func=lambda: 1, avgs_step=1, output_file_path=file_path)

    pl.start()
    
    pl.add("1")
    pl.add("2")
    pl.add("3")

    assert file_path.exists()

    with jsonlines.open(file_path) as generated:
        with jsonlines.open(reference_path) as reference:
            assert list(generated) == list(reference)

def test_file_cowriting(tmp_path):

    file_path = tmp_path / "test_file_cowriting.jsonl"
    file_path.unlink(missing_ok=True)
    reference_path = Path(__file__).parent / "reference_data" / "test_file_cowriting.jsonl"
    assert reference_path.exists()

    pl1 = PerfLogger(name="perflogger1", tick_func=lambda: 1, avgs_step=1, output_file_path=file_path)
    pl2 = PerfLogger(name="perflogger2", tick_func=lambda: 1, avgs_step=1, output_file_path=file_path)

    pl1.start()
    pl2.start()
    
    pl1.add("1")
    pl2.add("1")
    pl1.add("2")
    pl2.add("2")
    pl1.add("3")
    pl2.add("3")

    pl1.add("1")
    pl2.add("2")
    pl2.add("1")
    pl1.add("2")
    pl1.add("3")
    pl2.add("3")

    assert file_path.exists()

    with jsonlines.open(file_path) as generated:
        with jsonlines.open(reference_path) as reference:
            assert list(generated) == list(reference)
