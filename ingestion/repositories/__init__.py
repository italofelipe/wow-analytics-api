"""Repositories: única camada que fala com Postgres/R2.

Regra: nenhum import de httpx aqui. Collectors e pipelines injetam
repositories via argumento; não há singleton global de pool.
"""
