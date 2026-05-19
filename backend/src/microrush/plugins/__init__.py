"""Plugin System — Dynamic skill loading at runtime."""

from abc import ABC, abstractmethod
from typing import Any
import importlib


class Plugin(ABC):
    """
    Base class for all Micro Rush plugins/skills.

    Implement this to create a new skill:
    ```python
    class MySkill(Plugin):
        name = "my_skill"
        description = "What this skill does"

        def execute(self, context: dict) -> dict:
            # Your logic here
            return {"result": "something"}
    ```
    """

    name: str = "base_plugin"
    description: str = "A Micro Rush plugin"
    version: str = "0.1.0"

    @abstractmethod
    def execute(self, context: dict) -> dict:
        """Execute the plugin with given context.

        Args:
            context: Dict containing relevant data for this skill.
                Typically includes 'user_message', 'memory', 'session_id', etc.

        Returns:
            Dict with 'result' key (or 'error' if failed).
        """
        ...

    def validate(self, context: dict) -> bool:
        """Check if this plugin can handle the given context."""
        return True


class PluginRegistry:
    """
    Dynamic registry for runtime plugin discovery and loading.

    Usage:
        registry = PluginRegistry()
        registry.discover("src/microrush/skills")
        skill = registry.get("calendar")
        result = skill.execute(context)
    """

    def __init__(self):
        self._plugins: dict[str, type[Plugin]] = {}
        self._instances: dict[str, Plugin] = {}

    def register(self, plugin_class: type[Plugin]) -> None:
        """Register a plugin class."""
        instance = plugin_class()
        self._plugins[instance.name] = plugin_class
        self._instances[instance.name] = instance
        print(f"📦 Plugin registered: {instance.name}")

    def get(self, name: str) -> Plugin | None:
        """Get a plugin instance by name."""
        return self._instances.get(name)

    def list(self) -> list[dict]:
        """List all registered plugins."""
        return [
            {"name": p.name, "description": p.description, "version": p.version}
            for p in self._instances.values()
        ]

    def discover(self, plugin_dir: str) -> int:
        """
        Auto-discover plugins in a directory.

        Looks for classes that inherit from Plugin.
        """
        count = 0
        try:
            for file in os.listdir(plugin_dir):
                if file.endswith("_plugin.py"):
                    module_name = file[:-3]
                    # Dynamic import
                    spec = importlib.util.spec_from_file_location(
                        module_name, f"{plugin_dir}/{file}"
                    )
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        # Find Plugin subclasses
                        for attr_name in dir(module):
                            attr = getattr(module, attr_name)
                            if (
                                isinstance(attr, type)
                                and issubclass(attr, Plugin)
                                and attr is not Plugin
                            ):
                                self.register(attr)
                                count += 1
        except FileNotFoundError:
            pass
        return count


import os  # noqa: E402