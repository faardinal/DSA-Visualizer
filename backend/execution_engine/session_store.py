"""In-memory persistence for deterministic execution and trace replay."""

from dataclasses import dataclass, field
from threading import RLock
from typing import Optional
import time
import uuid

from .plugin_base import TestCase


@dataclass
class ExecutionSession:
    session_id: str
    problem_id: str
    seed: int
    test_cases: list[TestCase]
    created_at: float = field(default_factory=time.time)


class SessionStore:
    """Small bounded store; test inputs remain stable across replay requests."""

    def __init__(self, max_sessions: int = 200, ttl_seconds: int = 3600):
        self._max_sessions = max_sessions
        self._ttl_seconds = ttl_seconds
        self._sessions: dict[str, ExecutionSession] = {}
        self._lock = RLock()

    def create(self, problem_id: str, seed: int, test_cases: list[TestCase]) -> ExecutionSession:
        with self._lock:
            self._prune()
            while len(self._sessions) >= self._max_sessions:
                oldest = min(self._sessions.values(), key=lambda item: item.created_at)
                self._sessions.pop(oldest.session_id, None)
            session = ExecutionSession(str(uuid.uuid4()), problem_id, seed, test_cases)
            self._sessions[session.session_id] = session
            return session

    def get(self, session_id: Optional[str], problem_id: str) -> Optional[ExecutionSession]:
        if not session_id:
            return None
        with self._lock:
            self._prune()
            session = self._sessions.get(session_id)
            if session and session.problem_id == problem_id:
                return session
            return None

    def _prune(self) -> None:
        cutoff = time.time() - self._ttl_seconds
        for session_id, session in list(self._sessions.items()):
            if session.created_at < cutoff:
                self._sessions.pop(session_id, None)


session_store = SessionStore()
