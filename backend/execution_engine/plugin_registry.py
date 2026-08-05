"""
Plugin registry for LeetCode problem definitions.

Discovers and manages ProblemPlugin instances from the problems/ directory.
Each problem is a separate .py file — no monolithic registry.
"""

import importlib
import importlib.util
import os
import pkgutil
from typing import Optional

from .plugin_base import ProblemPlugin, ProblemInfo


class PluginRegistry:
    """
    Discovers, registers, and provides access to ProblemPlugin instances.

    Plugins are loaded from a directory of .py files. Each file should
    contain exactly one class that extends ProblemPlugin.

    Usage:
        registry = PluginRegistry()
        registry.discover_plugins("/path/to/problems/")
        plugin = registry.get("two-sum")
        matches = registry.find_by_method("search")
    """

    def __init__(self):
        self._plugins: dict[str, ProblemPlugin] = {}  # problem_id -> plugin
        self._by_method: dict[str, list[str]] = {}   # method_name -> [problem_ids]

    def discover_plugins(self, directory: str) -> int:
        """
        Scan a directory for .py plugin files and register all ProblemPlugin
        subclasses found.

        Args:
            directory: Path to the directory containing plugin .py files.

        Returns:
            Number of plugins successfully registered.
        """
        if not os.path.isdir(directory):
            return 0

        count = 0
        init_path = os.path.join(directory, "__init__.py")

        for filename in os.listdir(directory):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue

            filepath = os.path.join(directory, filename)
            module_name = filename[:-3]  # Strip .py

            try:
                plugins = self._load_plugins_from_file(filepath, module_name)
                for plugin in plugins:
                    self.register(plugin)
                    count += 1
            except Exception as e:
                # Log but don't crash — one bad plugin shouldn't block others
                print(f"[PluginRegistry] Failed to load {filename}: {e}")

        return count

    def discover_from_package(self, package_name: str) -> int:
        """
        Discover plugins from a Python package (e.g., "backend.execution_engine.problems").

        Args:
            package_name: Dotted package name.

        Returns:
            Number of plugins registered.
        """
        try:
            package = importlib.import_module(package_name)
        except ImportError:
            return 0

        package_dir = os.path.dirname(getattr(package, "__file__", ""))
        if not package_dir or not os.path.isdir(package_dir):
            return 0

        return self.discover_plugins(package_dir)

    def _load_plugins_from_file(self, filepath: str, module_name: str) -> list:
        """Load ProblemPlugin subclasses from a single .py file."""
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        if spec is None or spec.loader is None:
            return []

        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception:
            return []

        plugins = []
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            # Check if it's a class, not the ABC itself, and has required attributes
            if (isinstance(attr, type)
                    and issubclass(attr, ProblemPlugin)
                    and attr is not ProblemPlugin
                    and hasattr(attr, "problem_id")
                    and attr.problem_id):
                try:
                    instance = attr()
                    plugins.append(instance)
                except Exception:
                    continue

        return plugins

    def register(self, plugin: ProblemPlugin):
        """Register a single plugin instance."""
        pid = plugin.problem_id
        self._plugins[pid] = plugin

        method = plugin.method_name
        if method not in self._by_method:
            self._by_method[method] = []
        if pid not in self._by_method[method]:
            self._by_method[method].append(pid)

    def get(self, problem_id: str) -> Optional[ProblemPlugin]:
        """Get a plugin by its problem_id."""
        return self._plugins.get(problem_id)

    def find_by_method(self, method_name: str) -> list:
        """
        Find ALL plugins matching a method name.
        Returns a list (may be empty or contain multiple entries).
        Callers must handle ambiguity when len > 1.
        """
        pids = self._by_method.get(method_name, [])
        return [self._plugins[pid] for pid in pids if pid in self._plugins]

    def list_problems(self) -> list:
        """Return a list of ProblemInfo summaries for all registered problems."""
        return [plugin.to_info() for plugin in self._plugins.values()]

    def list_problem_dicts(self) -> list:
        """Return problem info as plain dicts (for JSON serialization)."""
        return [info.to_dict() for info in self.list_problems()]

    def get_all_problem_ids(self) -> list:
        """Return all registered problem IDs."""
        return list(self._plugins.keys())

    def has_problem(self, problem_id: str) -> bool:
        """Check if a problem is registered."""
        return problem_id in self._plugins

    def __len__(self) -> int:
        return len(self._plugins)

    def __contains__(self, problem_id: str) -> bool:
        return problem_id in self._plugins


# ---------------------------------------------------------------------------
# Global singleton — created once at import time, populated on first use.
# ---------------------------------------------------------------------------
_global_registry: Optional[PluginRegistry] = None


def get_registry() -> PluginRegistry:
    """Get the global plugin registry, initializing if needed."""
    global _global_registry
    if _global_registry is None:
        _global_registry = PluginRegistry()
        # Auto-discover plugins from the problems package
        problems_dir = os.path.join(os.path.dirname(__file__), "problems")
        _global_registry.discover_plugins(problems_dir)
    return _global_registry
