use p8g4
GO

DROP PROC QB.fornecimentos
GO

CREATE PROCEDURE QB.fornecimentos

AS
	BEGIN
		SELECT f.nome, f.morada, f.telemovel, tr.material, tr.formato, tr.id, r.quantidade, f.NIF, c.quantidade AS quantidadeTotal

		FROM QB.fornecedor as f
		JOIN QB.tipoRolha_Fornecedor AS r
			ON f.NIF = r.NIF
		JOIN QB.tipoRolha as tr
			ON tr.id = r.id_tipoRolha
		JOIN QB.rolha 
			ON rolha.id_tipoRolha = tr.id
		JOIN QB.componente as c
			ON c.id = rolha.id_componente
	END;