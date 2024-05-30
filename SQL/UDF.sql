USE p8g4;
GO

ALTER FUNCTION QB.fn_AtualizaContagemEncomendas(@ano INT, @mes INT, @semana INT, @dia INT)
RETURNS INT
AS
BEGIN
    DECLARE @TotalEncomendas INT;
    
    SELECT @TotalEncomendas = COUNT(*)
    FROM QB.encomenda
    WHERE (@ano IS NULL OR YEAR(data) = @ano)
        AND (@mes IS NULL OR MONTH(data) = @mes)
        AND (@semana IS NULL OR DATEPART(week, data) = @semana)
        AND (@dia IS NULL OR DAY(data) = @dia);
    
    RETURN @TotalEncomendas;
END;
GO