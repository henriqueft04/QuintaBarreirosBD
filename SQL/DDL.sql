CREATE SCHEMA [QB]
GO

CREATE TABLE [QB].[casta] (
  [nome] varchar(255),
  [id] int PRIMARY KEY
)
GO

CREATE TABLE [QB].[casta_tipoVinho] (
  [id_tipoVinho] int,
  [id_casta] int,
  PRIMARY KEY ([id_tipoVinho], [id_casta])
)
GO

CREATE TABLE [QB].[tipoVinho] (
  [notacao] varchar(255),
  [denominacao] varchar(255) UNIQUE,
  [id] int PRIMARY KEY,
  [acidez] decimal,
  [ano_colheita] int,
  [teor_alcoolico] decimal,
  [sub-regiao] varchar(255)
)
GO

CREATE TABLE [QB].[cuba] (
  [codigo] int PRIMARY KEY,
  [id_TipoVinho] int,
  [dataArmazenado] date,
  [descricao] varchar(255),
  [volume] int,
  [volumeOcupado] int,
  [refrigerada] bit,
  [termica] bit
)
GO

CREATE TABLE [QB].[cuba_engarrafamento] (
  [codigo_Cuba] int,
  [dataEngarrafamento] date
)
GO

CREATE TABLE [QB].[engarrafamento] (
  [dataEng] date PRIMARY KEY,
  [litragemEng] int,
  [quantidade] int
)
GO

CREATE TABLE [QB].[cliente] (
  [NIF] int PRIMARY KEY,
  [morada] varchar(255),
  [nome] varchar(255),
  [telemovel] int,
  [tipo] varchar(255),
)
GO

CREATE TABLE [QB].[fornecedor] (
  [NIF] int PRIMARY KEY,
  [morada] varchar(255),
  [nome] varchar(255),
  [telemovel] int,
)
GO

CREATE TABLE [QB].[encomenda] (
  [NIF_cliente] int,
  [fatura] bit,
  [valor] decimal,
  [notas] varchar(255),
  [data] date,
  [numero] int PRIMARY KEY
)
GO

CREATE TABLE [QB].[stock] (
  [id_tipoVinho] int,
  [id] int PRIMARY KEY,
  [quantidade] int,
  [peso_liquido] decimal,
  [peso_bruto] decimal,
  [preco] decimal
)
GO

CREATE TABLE [QB].[item] (
  [quantidadeItems] int,
  [id_stock] int ,
  [numero_encomenda] int
)
GO

CREATE TABLE [QB].[garrafao] (
  [id_stock] int PRIMARY KEY,
  [dataEng] date
)
GO

CREATE TABLE [QB].[garrafa] (
  [id_tipoVinho] int,
  [id_stock] int UNIQUE,
  [dataEng] date
)
GO

CREATE TABLE [QB].[componente] (
  [id] int PRIMARY KEY,
  [quantidade] int
)
GO

CREATE TABLE [QB].[rotulo] (
  [id_componente] int PRIMARY KEY,
  [NIF_cliente] int,
  [notacao_tipoVinho] nvarchar(255)
)
GO

CREATE TABLE [QB].[rolha] (
  [id_componente] int PRIMARY KEY,
  [id_tipoRolha] int
)
GO

CREATE TABLE [QB].[tipoRolha] (
  [id] int PRIMARY KEY,
  [material] varchar(255),
  [formato] varchar(255)
)
GO

CREATE TABLE [QB].[tipoRolha_fornecedor] (
  [id_tipoRolha] int,
  [NIF] int,
  [data] date,
  [quantidade] int,
  PRIMARY KEY ([id_tipoRolha], [NIF])
)
GO

CREATE TABLE [QB].[selo] (
  [id_componente] int PRIMARY KEY,
  [ano] int,
  [categoria] varchar(255)
)
GO

CREATE TABLE [QB].[certificados] (
  [id_componente] int PRIMARY KEY,
  [ano] int,
  [associacao] varchar(255),
  [titulo] varchar(255)
)
GO

CREATE TABLE [QB].[caixa] (
  [numGarrafas] varchar(255),
  [id_tipoVinho_garrafa] int,
  [id_stock] int,
  [dataEng] date,
  [id_stock_garrafa] int
)
GO

ALTER TABLE [QB].[casta_tipoVinho] ADD FOREIGN KEY ([id_casta]) REFERENCES [QB].[casta] ([id])
GO

ALTER TABLE [QB].[casta_tipoVinho] ADD FOREIGN KEY ([id_tipoVinho]) REFERENCES [QB].[tipoVinho] ([id])
GO

ALTER TABLE [QB].[cuba_engarrafamento] ADD FOREIGN KEY ([codigo_Cuba]) REFERENCES [QB].[cuba] ([codigo])
GO

ALTER TABLE [QB].[cuba_engarrafamento] ADD FOREIGN KEY ([dataEngarrafamento]) REFERENCES [QB].[engarrafamento] ([dataEng])
GO

ALTER TABLE [QB].[garrafa] ADD FOREIGN KEY ([dataEng]) REFERENCES [QB].[engarrafamento] ([dataEng])
GO

ALTER TABLE [QB].[rotulo] ADD FOREIGN KEY ([NIF_cliente]) REFERENCES [QB].[cliente] ([NIF])
GO

ALTER TABLE [QB].[encomenda] ADD FOREIGN KEY ([NIF_cliente]) REFERENCES [QB].[cliente] ([NIF])
GO

ALTER TABLE [QB].[item] ADD FOREIGN KEY ([numero_encomenda]) REFERENCES [QB].[encomenda] ([numero])
GO

ALTER TABLE [QB].[item] ADD FOREIGN KEY ([id_stock]) REFERENCES [QB].[stock] ([id])
GO

ALTER TABLE [QB].[caixa] ADD FOREIGN KEY ([id_stock]) REFERENCES [QB].[stock] ([id])
GO

ALTER TABLE [QB].[garrafao] ADD FOREIGN KEY ([id_stock]) REFERENCES [QB].[stock] ([id])
GO

ALTER TABLE [QB].[garrafa] ADD FOREIGN KEY ([id_stock]) REFERENCES [QB].[stock] ([id])
GO

ALTER TABLE [QB].[componente] ADD FOREIGN KEY ([id]) REFERENCES [QB].[garrafa] ([id_stock])
GO

ALTER TABLE [QB].[rotulo] ADD FOREIGN KEY ([id_componente]) REFERENCES [QB].[componente] ([id])
GO

ALTER TABLE [QB].[rolha] ADD FOREIGN KEY ([id_componente]) REFERENCES [QB].[componente] ([id])
GO

ALTER TABLE [QB].[selo] ADD FOREIGN KEY ([id_componente]) REFERENCES [QB].[componente] ([id])
GO

ALTER TABLE [QB].[certificados] ADD FOREIGN KEY ([id_componente]) REFERENCES [QB].[componente] ([id])
GO

ALTER TABLE [QB].[rolha] ADD FOREIGN KEY ([id_tipoRolha]) REFERENCES [QB].[tipoRolha] ([id])
GO

ALTER TABLE [QB].[tipoRolha_fornecedor] ADD FOREIGN KEY ([id_tipoRolha]) REFERENCES [QB].[tipoRolha] ([id])
GO

ALTER TABLE [QB].[tipoRolha_fornecedor] ADD FOREIGN KEY ([NIF]) REFERENCES [QB].[fornecedor] ([NIF])
GO

