use p8g4
GO

CREATE TRIGGER trg_AtualizarEncomendas

ON QB.encomenda
AFTER INSERT, UPDATE, DELETE
AS 
	BEGIN
		DECLARE @TotalEncomendas INT;
		SET @TotalEncomendas = (SELECT QB.fn_AtualizaContagemEncomendas());
	END;
GO

CREATE TRIGGER trg_UpdateTotalClientes
ON QB.cliente
AFTER INSERT
AS
    BEGIN
        DECLARE @totalClientes INT;

        SELECT @totalClientes = COUNT(*) FROM QB.cliente;
    end

SELECT COUNT(*) AS TotalClientes FROM QB.cliente;
GO