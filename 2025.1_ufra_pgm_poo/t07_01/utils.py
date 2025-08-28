# Utilidades simples e funções auxiliares.
# Este módulo pode crescer com funções de validação e geração de ids, etc.

def generate_id(prefix):
    import random
    return f"{prefix}_{random.randint(1000, 9999)}"