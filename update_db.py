import sqlite3

def add_criteria_columns():
    with sqlite3.connect('database.db') as conn:
        # Verifica se as colunas já existem e as adiciona se não existirem
        cursor = conn.execute("PRAGMA table_info(fornecedores)")
        columns = [column[1] for column in cursor.fetchall()]
        criteria = ['condicoes_pagamento', 'frete_cif', 'possui_iso', 'precos_justos', 'boa_indicacao']
        for criterion in criteria:
            if criterion not in columns:
                conn.execute(f'ALTER TABLE fornecedores ADD COLUMN {criterion} INTEGER')
                print(f"Coluna '{criterion}' adicionada com sucesso.")
            else:
                print(f"Coluna '{criterion}' já existe.")

if __name__ == '__main__':
    add_criteria_columns()
