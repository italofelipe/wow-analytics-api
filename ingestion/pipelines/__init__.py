"""Pipelines: entrypoints CLI. Wiring de deps + tratamento top-level.

Cada módulo aqui é invocado via `python -m ingestion.pipelines.<name>`.
Segue um padrão:

    def main() -> int:
        settings = get_settings()
        configure_logging(settings.log_level, settings.log_format)
        # construir clients + repos
        # orquestrar
        # retornar exit code

    if __name__ == "__main__":
        raise SystemExit(main())
"""
