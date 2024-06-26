CREATE OR ALTER PROC QB.p_getNumberOfClients
AS
    BEGIN
        SELECT COUNT(*) AS TotalClientes FROM QB.cliente
    END;
GO

CREATE OR ALTER PROC QB.p_NumberOfBottlesPerClient
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



CREATE OR ALTER PROCEDURE GetClientesPaginadas
    @PageNumber INT,
    @RowsPerPage INT
	AS
	BEGIN
		SET NOCOUNT ON;
		SELECT * FROM QB.cliente
		ORDER BY QB.cliente.nome DESC
		OFFSET (@PageNumber - 0) * @RowsPerPage ROWS
		FETCH NEXT @RowsPerPage ROWS ONLY;
	END;

	GO

	CREATE OR ALTER PROCEDURE QB.GetTotalGarrafasCliente
		@NIF_cliente NVARCHAR(49)
	AS
        BEGIN
            SET NOCOUNT ON;

            SELECT DISTINCT
                sum(
                    case 
                        when right(s.id, 1) = '1' then i.quantidadeitems 
                        when right(s.id, 1) = '2' then i.quantidadeitems 
                        when right(s.id, 1) = '3' then i.quantidadeitems * coalesce(caixa.numgarrafas, 1) 
                        else 0
                    end
                ) as total_garrafas
                from qb.cliente as c
                left join qb.encomenda as e on c.nif = e.nif_cliente
                left join qb.item as i on e.numero = i.numero_encomenda
                left join qb.stock as s on i.id_stock = s.id
                left join qb.caixa as caixa on caixa.id_stock = s.id
            WHERE e.NIF_cliente = @NIF_cliente;
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

CREATE OR ALTER PROC QB.p_DetalhesEcomendasPorCliente
    @NIF_cliente VARCHAR(50)
    AS
        BEGIN
            SELECT DISTINCT
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
            JOIN QB.encomenda e on c.NIF = e.NIF_cliente
            left JOIN QB.item i on e.numero = i.numero_encomenda
            left JOIN QB.stock s on i.id_stock = s.id
            left JOIN QB.tipoVinho v on s.id_tipoVinho = v.id
            WHERE c.NIF = @NIF_cliente
            ORDER BY ClienteNome
        END
   
 GO



CREATE OR ALTER PROC QB.p_AdicionarCliente
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

GO


CREATE OR ALTER PROCEDURE QB.fornecimentos
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

GO

CREATE OR ALTER PROC QB.insert_fornecimento
    @nomeFornecedor varchar(255),
    @tipoRolha varchar(255),
    @quantidadeRolhas int,
    @data DATE
    AS
    BEGIN
        DECLARE @nif int;
        DECLARE @material varchar(255);
        DECLARE @formato varchar(255);
        DECLARE @tipoRolhaId INT;
        DECLARE @componenteId INT = 2;

        -- obter o formato e o material das rolhas atraves do nome
        SET @material = SUBSTRING(@tipoRolha, 1, CHARINDEX(' - ', @tipoRolha) - 1);
        SET @formato = SUBSTRING(@tipoRolha, CHARINDEX(' - ', @tipoRolha) + 3, LEN(@tipoRolha) - CHARINDEX(' - ', @tipoRolha) - 2);

        -- verificar se o fornecedor existe
        SELECT @nif = NIF
        FROM QB.fornecedor
        WHERE nome = @nomeFornecedor

        IF @nif IS NULL
        BEGIN
            PRINT 'Erro: Fornecedor não existe.';
            RETURN;
        END

        -- obter id tipo de rolha a partir do material e do formato
        SELECT @tipoRolhaId = id
        FROM QB.tipoRolha
        WHERE material = @material AND formato = @formato

        if @tipoRolhaId IS NULL
        BEGIN
            PRINT 'Erro: Tipo de rolha não existe.';
            RETURN;
        END

        BEGIN TRANSACTION

        BEGIN TRY
            BEGIN
                -- Atualizar a quantidade
                UPDATE QB.tipoRolha_Fornecedor
                SET quantidade = quantidade + @quantidadeRolhas
                WHERE NIF = @NIF AND id_tipoRolha = @tipoRolhaId;
            END

            UPDATE QB.componente
            SET quantidade = quantidade + @quantidadeRolhas
            WHERE id = @componenteId;

            COMMIT TRANSACTION;
            PRINT 'Fornecimento inserido com sucesso!';

        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION ;
        END CATCH
    END

GO

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
        FULL JOIN
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

CREATE OR ALTER PROC QB.insert_fornecedor
    @nomeFornecedor varchar(255),
    @telemovelForn INT,
    @NIF_forn INT,
    @morada_forn varchar(255)

    AS
    BEGIN
        SET NOCOUNT ON;

        BEGIN TRY
            BEGIN TRANSACTION
            INSERT INTO QB.fornecedor (NIF, morada, nome, telemovel)
            VALUES (@NIF_forn, @morada_forn, @nomeFornecedor, @telemovelForn)

            COMMIT TRANSACTION
        END TRY

        BEGIN CATCH
            ROLLBACK TRANSACTION

            DECLARE @ErrorMessage NVARCHAR(4000), @ErrorSeverity INT, @ErrorState INT
            SELECT @ErrorMessage = ERROR_MESSAGE(), @ErrorSeverity = ERROR_SEVERITY(), @ErrorState = ERROR_STATE()
            RAISERROR (@ErrorMessage, @ErrorSeverity, @ErrorState)
        END CATCH
    END

    GO

CREATE OR ALTER PROC QB.deleteCuba
    @codigo INT
    AS
    BEGIN
        SET NOCOUNT ON;

        IF EXISTS (SELECT 1 FROM [QB].[cuba] WHERE [codigo] = @codigo)
        BEGIN
            BEGIN TRY

                BEGIN TRANSACTION
                    DELETE FROM [QB].[cuba_engarrafamento] WHERE [codigo_Cuba] = @codigo;
                    DELETE FROM [QB].[cuba] WHERE [codigo] = @codigo;
                    COMMIT TRANSACTION;

                    PRINT 'cuba eliminada.';
            END TRY
            begin catch
                ROLLBACK TRANSACTION;
                PRINT 'erro ao eliminar a cuba.';
            end catch
        END
        ELSE
        BEGIN
            PRINT 'cuba não encontrada.';
        END
    end

    GO

CREATE OR ALTER  PROCEDURE QB.insertEncomenda
    @nomeCliente VARCHAR(255),
    @estadoPagamento BIT,
    @notas VARCHAR(300),
    @valor DECIMAL,
    @fatura BIT,
    @data DATE,
    @items NVARCHAR(MAX)
    AS
    BEGIN
        SET NOCOUNT ON;

        BEGIN TRY
            BEGIN TRANSACTION;

            DECLARE @nifCliente VARCHAR(20);
            SELECT @nifCliente = NIF FROM [QB].[cliente] WHERE nome = @nomeCliente;

            IF @nifCliente IS NULL
            BEGIN
                RAISERROR('Cliente não encontrado.', 16, 1);
                ROLLBACK TRANSACTION;
                RETURN;
            END

            INSERT INTO [QB].[encomenda] ([NIF_cliente], [estadoPagamento], [fatura], [valor], [notas], [data])
            VALUES (@nifCliente, @estadoPagamento, @fatura, @valor, @notas, @data);

            DECLARE @numero_encomenda INT = SCOPE_IDENTITY();

            DECLARE @json NVARCHAR(MAX) = @items;
            DECLARE @quantidadeItems INT, @id_stock INT, @dataEng DATE;

            DECLARE @i INT = 0;
            DECLARE @itemCount INT = JSON_VALUE(@json, '$.length');

            WHILE @i < @itemCount
            BEGIN
                SET @quantidadeItems = JSON_VALUE(@json, CONCAT('$[', @i, '].quantidadeItems'));
                SET @id_stock = JSON_VALUE(@json, CONCAT('$[', @i, '].id_stock'));
                SET @dataEng = JSON_VALUE(@json, CONCAT('$[', @i, '].dataEng'));

                INSERT INTO [QB].[item] ([quantidadeItems], [id_stock], [dataEng], [numero_encomenda])
                VALUES (@quantidadeItems, @id_stock, @dataEng, @numero_encomenda);

                UPDATE [QB].[stock]
                SET quantidade = quantidade - @quantidadeItems
                WHERE id = @id_stock AND dataEng = @dataEng;

                IF @@ROWCOUNT = 0
                BEGIN
                    RAISERROR('Stock insuficiente ou item não encontrado.', 16, 1);
                    ROLLBACK TRANSACTION;
                    RETURN;
                END

                SET @i = @i + 1;
            END

            COMMIT TRANSACTION;
            PRINT 'Encomenda inserida e Stock atualizado';
        END TRY
        BEGIN CATCH
            IF @@TRANCOUNT > 0
            BEGIN
                ROLLBACK TRANSACTION;
            END
            DECLARE @ErrorMessage NVARCHAR(4000);
            DECLARE @ErrorSeverity INT;
            DECLARE @ErrorState INT;

            SELECT @ErrorMessage = ERROR_MESSAGE(), @ErrorSeverity = ERROR_SEVERITY(), @ErrorState = ERROR_STATE();

            RAISERROR (@ErrorMessage, @ErrorSeverity, @ErrorState);
        END CATCH
    END;
    GO 

