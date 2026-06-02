import re

with open("argus/llm/factory.py", "r") as f:
    content = f.read()

new_methods = """
    def __init__(self):
        self._providers_instance = {}
        self._provider_types = self._providers.copy()

    def register_provider_type(self, provider_type, provider_class):
        self._provider_types[provider_type] = provider_class

    def create_provider(self, config, force_recreate=False):
        provider_type = config.provider
        if provider_type not in self._provider_types:
            raise ValueError(f"Unsupported provider type: {provider_type}")
        
        provider_class = self._provider_types[provider_type]
        try:
            provider = provider_class(config)
            if not provider.validate_config():
                raise ValueError(f"Invalid configuration for provider: {provider_type}")
            self._providers_instance[provider_type] = provider
            return provider
        except ValueError:
            raise
        except Exception as e:
            raise RuntimeError(f"Provider creation failed: {e}")

    def get_provider_instance(self, provider_name):
        return self._providers_instance.get(provider_name)

    def get_all_providers(self):
        return self._providers_instance.copy()

    def remove_provider(self, provider_name):
        if provider_name in self._providers_instance:
            del self._providers_instance[provider_name]
            return True
        return False

    def clear_providers(self):
        self._providers_instance.clear()

    def get_supported_providers(self):
        return list(self._provider_types.keys())
"""

# We need to hack property _providers to return _providers_instance on instance level
property_hack = """
    @property
    def _providers(self):
        if not hasattr(self, '_providers_instance'):
            return self.__class__._providers_class
        return self._providers_instance
"""

content = content.replace("    _providers = {", "    _providers_class = {")
content = content.replace("        return cls._instances[instance_key]", new_methods + "\n        return cls._instances[instance_key]")

with open("argus/llm/factory.py", "w") as f:
    f.write(content)
