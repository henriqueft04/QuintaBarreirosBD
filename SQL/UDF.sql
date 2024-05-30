USE p8g4;
GO

ALTER FUNCTION QB.fn_AtualizaContagemEncomendas(@ano INT, @mes INT, @semana INT, @dia DATE)
RETURNS INT
AS
BEGIN
    DECLARE @TotalEncomendas INT;
    
    SELECT @TotalEncomendas = COUNT(*)
    FROM QB.encomenda
    WHERE (@ano IS NULL OR YEAR(data) = @ano)
        AND (@mes IS NULL OR MONTH(data) = @mes)
        AND (@semana IS NULL OR DATEPART(week, data) = @semana)
        AND (@dia IS NULL OR CAST(data AS DATE) = @dia);
    
    RETURN @TotalEncomendas;
END;
GO


ALTER FUNCTION QB.fn_AtualizaContagemClientes(@SearchParam varchar(2048))
RETURNS INT
AS
BEGIN
    DECLARE @TotalClientes INT;
    
    SELECT @TotalClientes = COUNT(*)
    FROM QB.cliente
    WHERE QB.cliente.nome LIKE '%' + @SearchParam + '%'
    
    RETURN @TotalClientes;
END;
GO
