from jacob_core.memory import MemoryEngine
from jacob_core.models import MemoryCategory, MemoryRecord


def test_memory_engine_add_search_delete(tmp_path):
    store = MemoryEngine(path=str(tmp_path / "memory.json"))

    memory = store.add_memory(
        MemoryRecord(
            key="active_project",
            value="Jacob 0.1 is the current priority.",
            category=MemoryCategory.PROJECTS,
            importance=5,
        )
    )

    assert memory.id
    assert len(store.list_memories()) == 1
    assert store.search("Jacob")[0].key == "active_project"
    assert store.delete_memory(memory.id) is True
    assert store.list_memories() == []


def test_memory_engine_rejects_unauthorized_memory(tmp_path):
    store = MemoryEngine(path=str(tmp_path / "memory.json"))

    unauthorized = MemoryRecord(
        key="private",
        value="Do not store this.",
        authorized=False,
    )

    try:
        store.add_memory(unauthorized)
        assert False, "Expected ValueError"
    except ValueError:
        assert True
