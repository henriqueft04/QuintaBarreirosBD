DROP PROC IF EXISTS QB.p_getNumberOfClients
GO
DROP PROC IF EXISTS QB.p_NumberOfBottlesPerClient
GO
DROP PROC IF EXISTS QB.p_DetalhesEcomendasPorCliente
GO
DROP PROC IF EXISTS QB.p_AdicionarCliente
GO
DROP PROCEDURE IF EXISTS QB.fornecimentos
GO
DROP PROCEDURE IF EXISTS QB.engarrafamentos
GO

CREATE PROC QB.p_getNumberOfClients
AS
    BEGIN
        SELECT COUNT(*) AS TotalClientes FROM QB.cliente
    END;
GO

CREATE PROC QB.p_NumberOfBottlesPerClient
AS
    BEGIN
        SELECT QB.cliente.NIF AS ClienteNIF,
               QB.cliente.nome AS ClienteNome,
               SUM(QB.item.quantidadeItems) AS TotalGarrafas
        FROM
            QB.cliente
        INNER JOIN QB.encomenda on cliente.NIF = encomenda.NIF_cliente
        INNER JOIN QB.item on encomenda.numero = item.numero_encomenda
        GROUP BY QB.cliente.NIF, QB.cliente.nome
    END
GO

CREATE PROC QB.p_DetalhesEcomendasPorCliente
    @NIF_cliente VARCHAR(50)
AS
    BEGIN
        SELECT
            c.nome AS ClienteNome,
            e.numero AS NumeroEncomenda,
            e.data AS DataEncomenda,
            e.estadoPagamento AS EstadoPagamento,
            e.fatura AS Fatura,
            e.valor AS ValorEncomenda,
            e.notas AS Notas,
            v.denominacao AS Denominacao,
            i.quantidadeItems AS QuantidadeItems
        FROM QB.cliente as c
        INNER JOIN QB.encomenda e on c.NIF = e.NIF_cliente
        INNER JOIN QB.item i on e.numero = i.numero_encomenda
        JOIN QB.stock s on i.id_stock = s.id
        JOIN QB.tipoVinho v on s.id_tipoVinho = v.id
        WHERE c.NIF = @NIF_cliente
        ORDER BY ClienteNome
    END
GO



CREATE PROC QB.p_AdicionarCliente
    @nif INT,
    @morada VARCHAR(255),
    @nome VARCHAR(255),
    @telemovel INT,
    @tipo VARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        BEGIN TRANSACTION

        INSERT INTO QB.cliente (NIF, morada, nome, telemovel, tipo)
        VALUES (@nif, @morada, @nome, @telemovel, @tipo)

        COMMIT TRANSACTION
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION

        DECLARE @ErrorMessage NVARCHAR(4000), @ErrorSeverity INT, @ErrorState INT
        SELECT @ErrorMessage = ERROR_MESSAGE(), @ErrorSeverity = ERROR_SEVERITY(), @ErrorState = ERROR_STATE()
        RAISERROR (@ErrorMessage, @ErrorSeverity, @ErrorState)
    END CATCH
END
go

CREATE PROCEDURE QB.fornecimentos
    (@nomeFornecedor VARCHAR(255) = NULL)
AS
	BEGIN

        DECLARE @query NVARCHAR(MAX);
        SET @query = 'SELECT f.nome, f.morada, f.telemovel, tr.material, tr.formato, r.quantidade, f.NIF, c.quantidade AS quantidadeTotal
                    FROM QB.fornecedor AS f
                    JOIN QB.tipoRolha_Fornecedor AS r ON f.NIF = r.NIF
                    JOIN QB.tipoRolha AS tr ON tr.id = r.id_tipoRolha
                    JOIN QB.rolha ON rolha.id_tipoRolha = tr.id
                    JOIN QB.componente AS c ON c.id = rolha.id_componente';

		IF @nomeFornecedor IS NOT NULL
        SET @query = @query + ' WHERE f.nome LIKE ''%' + @nomeFornecedor + '%''';

    EXEC sp_executesql @query;


	SELECT COUNT(*) AS total_fornecedores
		FROM QB.fornecedor;

	SELECT tr.material, tr.formato, tr.id
		FROM QB.tipoRolha AS tr;

	END;
go

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
go



