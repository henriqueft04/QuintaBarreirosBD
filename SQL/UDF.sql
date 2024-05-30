use p8g4
GO

ALTER FUNCTION QB.fn_AtualizaContagemEncomendas()
RETURNS INT
AS
	BEGIN
		DECLARE @TotalEncomendas INT;
		SELECT @TotalEncomendas = COUNT(*) FROM QB.encomenda;
		RETURN @TotalEncomendas;
	END;
GO