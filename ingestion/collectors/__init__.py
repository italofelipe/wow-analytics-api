"""Collectors: orquestram client + mapeiam resposta bruta para domínio.

Regra: nenhum import de repositories/ ou de módulos de DB/R2 aqui.
Collector puro recebe client(s) + CharacterRef e retorna domínio — facilita
testes com respx e evita side-effects escondidos.
"""
