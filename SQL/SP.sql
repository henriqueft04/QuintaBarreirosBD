GO
DROP PROCEDURE IF EXISTS QB.fornecimentos;
GO

CREATE PROCEDURE QB.fornecimentos
AS
	BEGIN
		SELECT f.nome, f.morada, f.telemovel, tr.material, tr.formato, r.quantidade, f.NIF, c.quantidade AS quantidadeTotal
		FROM QB.fornecedor AS f
		JOIN QB.tipoRolha_Fornecedor AS r
			ON f.NIF = r.NIF
		JOIN QB.tipoRolha AS tr
			ON tr.id = r.id_tipoRolha
		JOIN QB.rolha 
			ON rolha.id_tipoRolha = tr.id
		JOIN QB.componente AS c
			ON c.id = rolha.id_componente;

		SELECT COUNT(*) AS total_fornecedores
		FROM QB.fornecedor;

		SELECT tr.material, tr.formato, tr.id
		FROM QB.tipoRolha AS tr;

	END;
GO

DROP PROCEDURE IF EXISTS QB.engarrafamentos;
GO

CREATE PROCEDURE QB.engarrafamentos
AS 
BEGIN
	SELECT codigo_Cuba AS codigo_cuba, dataEng, litragemEng as litragem, quantidade, notacao, denominacao
		FROM QB.cuba_engarrafamento
		JOIN QB.engarrafamento 
			ON dataEng = dataEngarrafamento
		JOIN QB.cuba
			ON codigo_Cuba = cuba.codigo
		JOIN QB.tipoVinho
			ON tipoVinho.id = cuba.id_TipoVinho

	SELECT COUNT(*) AS total_engarrafamentos
		FROM QB.engarrafamento;

	
END;