GO

ALTER PROCEDURE QB.fornecimentos
    @nomeFornecedor VARCHAR(255) = NULL
AS
BEGIN
    IF @nomeFornecedor IS NOT NULL
    BEGIN
        SELECT f.nome, f.morada, f.telemovel, tr.material, tr.formato, r.quantidade, f.NIF, c.quantidade AS quantidadeTotal
        FROM QB.fornecedor AS f
        JOIN QB.tipoRolha_Fornecedor AS r ON f.NIF = r.NIF
        JOIN QB.tipoRolha AS tr ON tr.id = r.id_tipoRolha
        JOIN QB.rolha ON rolha.id_tipoRolha = tr.id
        JOIN QB.componente AS c ON c.id = rolha.id_componente
        WHERE f.nome LIKE '%' + @nomeFornecedor + '%';
    END
    ELSE
    BEGIN
        SELECT f.nome, f.morada, f.telemovel, tr.material, tr.formato, r.quantidade, f.NIF, c.quantidade AS quantidadeTotal
        FROM QB.fornecedor AS f
        JOIN QB.tipoRolha_Fornecedor AS r ON f.NIF = r.NIF
        JOIN QB.tipoRolha AS tr ON tr.id = r.id_tipoRolha
        JOIN QB.rolha ON rolha.id_tipoRolha = tr.id
        JOIN QB.componente AS c ON c.id = rolha.id_componente

        SELECT COUNT(*) AS total_fornecedores FROM QB.fornecedor;
        SELECT f.nome, tr.material, tr.formato
        FROM QB.fornecedor AS f
        JOIN QB.tipoRolha_fornecedor AS r ON f.NIF = r.NIF
        JOIN QB.tipoRolha AS tr ON tr.id = r.id_tipoRolha
    END

END;

	
CREATE OR ALTER PROCEDURE QB.engarrafamentos
    @orderBy varchar(20) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    IF @orderBy IS NULL OR @orderBy = ''
    BEGIN
        SET @orderBy = 'Mais Recente';
    END

    SELECT
        codigo_Cuba AS codigo_cuba,
        dataEng,
        litragemEng as litragem,
        quantidade,
        notacao,
        denominacao
    FROM
        QB.cuba_engarrafamento
    JOIN
        QB.engarrafamento
        ON dataEng = dataEngarrafamento
    JOIN
        QB.cuba
        ON codigo_Cuba = cuba.codigo
    LEFT JOIN
        QB.tipoVinho
        ON tipoVinho.id = cuba.id_TipoVinho
    ORDER BY
        CASE
            WHEN @orderBy = 'Maior Litragem' THEN litragemEng END DESC,
        CASE
            WHEN @orderBy = 'Menor Litragem' THEN litragemEng END,
        CASE
            WHEN @orderBy = 'Mais Recente' THEN dataEng END DESC,
        CASE
            WHEN @orderBy = 'Mais Antigo' THEN dataEng END;

    SELECT
        COUNT(*) AS total_engarrafamentos
    FROM
        QB.engarrafamento;
END;
GO


GO

CREATE OR ALTER PROCEDURE QB.GetEncomendasPaginadas
    @PageNumber INT,
    @RowsPerPage INT,
    @Ano INT = NULL,
    @Mes INT = NULL,
    @Semana INT = NULL,
    @Dia DATE = NULL
AS
BEGIN
    SET NOCOUNT ON;

    WITH Encomendas AS (
        SELECT 
            NIF_cliente, 
            estadoPagamento, 
            fatura, 
            valor, 
            notas, 
            QB.encomenda.data, 
            numero, 
            NIF, 
            morada, 
            nome, 
            tipo,
            (SELECT SUM(CASE 
                        WHEN RIGHT(QB.stock.id, 1) = '1' THEN stock.quantidade
                        WHEN RIGHT(QB.stock.id, 1) = '2' THEN stock.quantidade
                        WHEN RIGHT(QB.stock.id, 1) = '3' THEN numGarrafas * stock.quantidade
                        ELSE 0 
                    END)
             FROM QB.item 
             JOIN QB.stock ON QB.stock.id = QB.item.id_stock 
             LEFT JOIN QB.caixa ON QB.caixa.id_stock = QB.stock.id
             WHERE QB.item.numero_encomenda = QB.encomenda.numero) AS TotalGarrafas
        FROM QB.encomenda 
        JOIN QB.cliente ON QB.cliente.NIF = QB.encomenda.NIF_cliente
        WHERE
            (@Ano IS NULL OR YEAR(QB.encomenda.data) = @Ano) AND
            (@Mes IS NULL OR MONTH(QB.encomenda.data) = @Mes) AND
            (@Semana IS NULL OR DATEPART(WEEK, QB.encomenda.data) = @Semana) AND
            (@Dia IS NULL OR CAST(QB.encomenda.data AS DATE) = @Dia)
    )
    SELECT *
    FROM Encomendas
    ORDER BY data DESC
    OFFSET (@PageNumber - 1) * @RowsPerPage ROWS
    FETCH NEXT @RowsPerPage ROWS ONLY;
END;



GO 


CREATE OR ALTER PROCEDURE GetClientesPaginadas
    @PageNumber INT,
    @RowsPerPage INT
	AS
	BEGIN
		SET NOCOUNT ON;
		SELECT * FROM QB.cliente
		ORDER BY QB.cliente.nome DESC
		OFFSET (@PageNumber - 1) * @RowsPerPage ROWS
		FETCH NEXT @RowsPerPage ROWS ONLY;
	END;

	GO

	CREATE OR ALTER PROCEDURE QB.GetTotalGarrafasCliente
		@NIF_cliente NVARCHAR(50)
	AS
	BEGIN
		SET NOCOUNT ON;

		SELECT 
			SUM(CASE 
					WHEN RIGHT(QB.stock.id, 1) = '1' THEN quantidadeItems 
					WHEN RIGHT(QB.stock.id, 1) = '2' THEN quantidadeItems 
					WHEN RIGHT(QB.stock.id, 1) = '3' THEN quantidadeItems * numGarrafas 
					ELSE 0 
				END) AS TotalGarrafas
		FROM QB.encomenda 
		JOIN QB.item ON QB.item.numero_encomenda = QB.encomenda.numero
		JOIN QB.stock ON QB.stock.id = QB.item.id_stock 
		LEFT JOIN QB.caixa ON QB.caixa.id_stock = QB.stock.id
		WHERE QB.encomenda.NIF_cliente = @NIF_cliente;
END;


GO


CREATE OR ALTER PROCEDURE QB.stockInfo
AS
BEGIN
    SET NOCOUNT ON;

    -- Subconsulta para contar o total de tipos de vinho
    DECLARE @total_tiposVinho INT;
    SELECT @total_tiposVinho = COUNT(*) FROM QB.tipoVinho;

    SELECT 
        tv.id AS id_tipoVinho, 
        tv.notacao,
        tv.denominacao, 
        MAX(s.dataEng) AS dataEng,
        SUM(CASE WHEN RIGHT(s.id, 1) = '1' THEN s.quantidade ELSE 0 END) AS total_garrafoes,
        SUM(CASE WHEN RIGHT(s.id, 1) = '2' THEN s.quantidade ELSE 0 END) AS total_garrafas,
        SUM(CASE WHEN RIGHT(s.id, 1) = '3' THEN s.quantidade ELSE 0 END) AS total_caixas,
        SUM(CASE 
                WHEN RIGHT(s.id, 1) = '1' THEN s.quantidade 
                WHEN RIGHT(s.id, 1) = '2' THEN s.quantidade 
                WHEN RIGHT(s.id, 1) = '3' THEN s.quantidade * ISNULL(c.numGarrafas, 0)
                ELSE 0 
            END) AS total_garrafas_total,
        @total_tiposVinho AS total_tiposVinho 
    FROM QB.stock s
    LEFT JOIN QB.tipoVinho tv ON tv.id = s.id_tipoVinho
    LEFT JOIN QB.caixa c ON c.id_stock = s.id
    GROUP BY 
        tv.id, 
        tv.notacao, 
        tv.denominacao,
        s.dataEng
    ORDER BY 
        tv.id,
        s.dataEng;
END;
GO




CREATE OR ALTER  PROCEDURE QB.cubaInfo
    @orderBy varchar(20) = NULL
AS
BEGIN
	SET NOCOUNT ON;

	IF @orderBy IS NULL OR @orderBy = ''
    BEGIN
        SET @orderBy = 'ID';
    END

	DECLARE @cubas_totais INT;
	SELECT @cubas_totais = COUNT(*) FROM QB.cuba;

	SELECT @cubas_totais AS cubas_totais,codigo,volumeOcupado, volume, notacao + ' - ' + denominacao AS nomeVinho, dataArmazenado, descricao, refrigerada, termica
	FROM QB.cuba
		LEFT JOIN QB.tipoVinho tv on tv.id = cuba.id_tipoVinho
    ORDER BY
        CASE
            WHEN @orderBy = 'Maior Litragem' THEN volumeOcupado END DESC,
         CASE
            WHEN @orderBy = 'Menor Litragem' THEN volumeOcupado END,
        CASE
            WHEN @orderBy = 'Mais Recente' THEN dataArmazenado END DESC,
        CASE
            WHEN @orderBy = 'Mais Antigo' THEN dataArmazenado END,
	    CASE
            WHEN @orderBy = 'ID' THEN codigo END;


END;
go


