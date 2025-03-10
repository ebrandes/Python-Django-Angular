from django.apps import AppConfig


class AddressesConfig(AppConfig):
    name = "addresses"

    def ready(self) -> None:
        import addresses.signals

        return super().ready()
