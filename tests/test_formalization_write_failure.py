import importlib.util
from pathlib import Path
from unittest.mock import patch
import pytest

spec = importlib.util.spec_from_file_location('formalization', Path(__file__).parents[1] / 'scripts' / 'update_formalization_status.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_serialization_failure_preserves_database(tmp_path):
    database = tmp_path / 'problems.yaml'
    original = '- number: "1"\n  formalized:\n    state: "no"\n'
    database.write_text(original)
    def failing_dump(data, stream):
        stream.write('partial output\n')
        raise OSError('disk full')
    with patch.object(module, 'DATA_PATH', database), patch.object(module.YAML, 'dump', side_effect=failing_dump):
        with pytest.raises(OSError, match='disk full'):
            module.update_yaml_file({'1'})
    assert database.read_text() == original
    assert list(tmp_path.iterdir()) == [database]

def test_successful_update_preserves_mode(tmp_path):
    database = tmp_path / 'problems.yaml'
    database.write_text('- number: "1"\n  formalized:\n    state: "no"\n')
    database.chmod(0o644)
    with patch.object(module, 'DATA_PATH', database):
        module.update_yaml_file({'1'})
    assert 'state: "yes"' in database.read_text()
    assert database.stat().st_mode & 0o777 == 0o644
