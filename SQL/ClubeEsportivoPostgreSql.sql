DROP SCHEMA IF EXISTS public CASCADE;

-- Criar o novo esquema
CREATE SCHEMA IF NOT EXISTS mydb;

-- Definir o esquema padrão para a sessão atual
SET search_path TO mydb;

-- Tabela Associado
CREATE TABLE IF NOT EXISTS mydb.Associado (
  MatriculaAssoc INT NOT NULL,
  Nome VARCHAR(45) NOT NULL,
  Endereco VARCHAR(45) NOT NULL,
  Data_nascimento TIMESTAMP(0) NULL,
  Telefone VARCHAR(15) NOT NULL,
  Email VARCHAR(45) NOT NULL,
  CPF VARCHAR(15) NOT NULL,
  "Tipo (titular/dependente)" VARCHAR(45) NOT NULL,
  Data_adesao TIMESTAMP(0) NOT NULL,
  Foto BYTEA NULL,
  "Tipo (associado/dependente)" VARCHAR(45) NOT NULL,
  PRIMARY KEY (MatriculaAssoc),
  CONSTRAINT CPF_UNIQUE UNIQUE (CPF)
);

-- Tabela Departamento
CREATE TABLE IF NOT EXISTS mydb.Departamento (
  IdDpto INT NOT NULL,
  NomeDpto VARCHAR(45) NULL,
  PRIMARY KEY (IdDpto)
);

-- Tabela Cargo
CREATE TABLE IF NOT EXISTS mydb.Cargo (
  idCargo INT NOT NULL,
  Nome_Cargo VARCHAR(45) NOT NULL,
  Descricao VARCHAR(45) NULL,
  Salário VARCHAR(45) NOT NULL,
  PRIMARY KEY (idCargo)
);

-- Tabela Funcionario
CREATE TABLE IF NOT EXISTS mydb.Funcionario (
  Funcionario_MatriculaFunc INT NOT NULL,
  Cargo_idCargo INT NOT NULL,
  Departamento_IdDpto INT NOT NULL,
  CPF_func VARCHAR(11) NOT NULL,
  PRIMARY KEY (Funcionario_MatriculaFunc),
  CONSTRAINT CPF_Func_UNIQUE UNIQUE (CPF_func),
  CONSTRAINT fk_Funcionario_Cargo1
    FOREIGN KEY (Cargo_idCargo)
    REFERENCES mydb.Cargo (idCargo)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_Funcionario_Departamento1
    FOREIGN KEY (Departamento_IdDpto)
    REFERENCES mydb.Departamento (IdDpto)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Tabela Atestado
CREATE TABLE IF NOT EXISTS mydb.Atestado (
  idAtestado INT NOT NULL,
  Funcionario_MatriculaFunc INT NOT NULL,
  Associado_MatriculaAssoc INT NOT NULL,
  Data_emissao TIMESTAMP(0) NOT NULL,
  Data_validade TIMESTAMP(0) NOT NULL,
  PRIMARY KEY (idAtestado),
  CONSTRAINT fk_Atestado_Funcionario1
    FOREIGN KEY (Funcionario_MatriculaFunc)
    REFERENCES mydb.Funcionario (Funcionario_MatriculaFunc)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_Atestado_Associado1
    FOREIGN KEY (Associado_MatriculaAssoc)
    REFERENCES mydb.Associado (MatriculaAssoc)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Tabela Instalacao
CREATE TABLE IF NOT EXISTS mydb.Instalacao (
  idInstalacao INT NOT NULL,
  Nome VARCHAR(45) NOT NULL,
  Tipo VARCHAR(45) NULL,
  Capacidade VARCHAR(45) NULL,
  PRIMARY KEY (idInstalacao)
);

-- Tabela Esporte
CREATE TABLE IF NOT EXISTS mydb.Esporte (
  idEsporte INT NOT NULL,
  Nome_Esporte VARCHAR(45) NOT NULL,
  Tipo_ind_col VARCHAR(45) NOT NULL,
  Instalacao_idInstalacao INT NOT NULL,
  PRIMARY KEY (idEsporte, Instalacao_idInstalacao),
  CONSTRAINT fk_Esporte_Instalacao1
    FOREIGN KEY (Instalacao_idInstalacao)
    REFERENCES mydb.Instalacao (idInstalacao)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Tabela Equipe
CREATE TABLE IF NOT EXISTS mydb.Equipe (
  idEquipe INT NOT NULL,
  Nome VARCHAR(45) NULL,
  Tecnico_Responsavel VARCHAR(45) NULL,
  Esporte_idEsporte INT NOT NULL,
  Instalacao_idInstalacao INT NOT NULL,
  PRIMARY KEY (idEquipe, Esporte_idEsporte, Instalacao_idInstalacao),
  CONSTRAINT fk_Equipe_Esporte1
    FOREIGN KEY (Esporte_idEsporte, Instalacao_idInstalacao)
    REFERENCES mydb.Esporte (idEsporte, Instalacao_idInstalacao)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Tabela Equipe_tem_associado
CREATE TABLE IF NOT EXISTS mydb.Equipe_tem_associado (
  Equipe_idEquipe INT NOT NULL,
  Esporte_idEsporte INT NOT NULL,
  Instalacao_idInstalacao INT NOT NULL,
  Associado_MatriculaAssoc INT NOT NULL,
  PRIMARY KEY (Equipe_idEquipe, Esporte_idEsporte, Instalacao_idInstalacao, Associado_MatriculaAssoc),
  CONSTRAINT fk_Equipe_has_Associado_Equipe1
    FOREIGN KEY (Equipe_idEquipe, Esporte_idEsporte, Instalacao_idInstalacao)
    REFERENCES mydb.Equipe (idEquipe, Esporte_idEsporte, Instalacao_idInstalacao)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_Equipe_has_Associado_Associado1
    FOREIGN KEY (Associado_MatriculaAssoc)
    REFERENCES mydb.Associado (MatriculaAssoc)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Tabela Evento
CREATE TABLE IF NOT EXISTS mydb.Evento (
  idEvento INT NOT NULL,
  Nome VARCHAR(45) NOT NULL,
  Data_realizacao TIMESTAMP(0) NULL,
  Descricao VARCHAR(45) NULL,
  Eventocol VARCHAR(45) NULL,
  Associado_MatriculaAssoc INT NOT NULL,
  Equipe_idEquipe INT NOT NULL,
  Esporte_idEsporte INT NOT NULL,
  Instalacao_idInstalacao INT NOT NULL,
  PRIMARY KEY (idEvento),
  CONSTRAINT fk_Evento_Associado1
    FOREIGN KEY (Associado_MatriculaAssoc)
    REFERENCES mydb.Associado (MatriculaAssoc)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_Evento_Equipe1
    FOREIGN KEY (Equipe_idEquipe, Esporte_idEsporte, Instalacao_idInstalacao)
    REFERENCES mydb.Equipe (idEquipe, Esporte_idEsporte, Instalacao_idInstalacao)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Tabela Plano
CREATE TABLE IF NOT EXISTS mydb.Plano (
  idPlano INT NOT NULL,
  Nome VARCHAR(45) NOT NULL,
  Descricao VARCHAR(45) NOT NULL,
  Valor INT NOT NULL,
  Periodo VARCHAR(45) NOT NULL,
  PRIMARY KEY (idPlano)
);

-- Tabela Contrato
CREATE TABLE IF NOT EXISTS mydb.Contrato (
  idContrato INT NOT NULL,
  Associado_MatriculaAssoc INT NOT NULL,
  Plano_idPlano INT NOT NULL,
  PRIMARY KEY (idContrato),
  CONSTRAINT fk_Contrato_Associado1
    FOREIGN KEY (Associado_MatriculaAssoc)
    REFERENCES mydb.Associado (MatriculaAssoc)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_Contrato_Plano1
    FOREIGN KEY (Plano_idPlano)
    REFERENCES mydb.Plano (idPlano)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Tabela Pagamento
CREATE TABLE IF NOT EXISTS mydb.Pagamento (
  idPagamento INT NOT NULL,
  Data TIMESTAMP(0) NULL,
  Valor DECIMAL(10,2) NULL,
  Metodo VARCHAR(45) NULL,
  Status_pago_nao_pago VARCHAR(45) NULL,
  Contrato_idContrato INT NOT NULL,
  PRIMARY KEY (idPagamento, Contrato_idContrato),
  CONSTRAINT fk_Pagamento_Contrato1
    FOREIGN KEY (Contrato_idContrato)
    REFERENCES mydb.Contrato (idContrato)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Tabela Instalacao_realiza_Evento
CREATE TABLE IF NOT EXISTS mydb.Instalacao_realiza_Evento (
  Instalacao_idInstalacao INT NOT NULL,
  Evento_idEvento INT NOT NULL,
  PRIMARY KEY (Instalacao_idInstalacao, Evento_idEvento),
  CONSTRAINT fk_Instalacao_has_Evento_Instalacao1
    FOREIGN KEY (Instalacao_idInstalacao)
    REFERENCES mydb.Instalacao (idInstalacao)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_Instalacao_has_Evento_Evento1
    FOREIGN KEY (Evento_idEvento)
    REFERENCES mydb.Evento (idEvento)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Tabela Departamento_esta_Instalacao
CREATE TABLE IF NOT EXISTS mydb.Departamento_esta_Instalacao (
  Instalacao_idInstalacao INT NOT NULL,
  Departamento_IdDpto INT NOT NULL,
  PRIMARY KEY (Instalacao_idInstalacao, Departamento_IdDpto),
  CONSTRAINT fk_Instalacao_has_Departamento_Instalacao1
    FOREIGN KEY (Instalacao_idInstalacao)
    REFERENCES mydb.Instalacao (idInstalacao)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_Instalacao_has_Departamento_Departamento1
    FOREIGN KEY (Departamento_IdDpto)
    REFERENCES mydb.Departamento (IdDpto)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Tabela Funcionario_treina_Equipe
CREATE TABLE IF NOT EXISTS mydb.Funcionario_treina_Equipe (
  Funcionario_MatriculaFunc INT NOT NULL,
  Cargo_idCargo INT NOT NULL,
  Departamento_IdDpto INT NOT NULL,
  Equipe_idEquipe INT NOT NULL,
  Esporte_idEsporte INT NOT NULL,
  Instalacao_idInstalacao INT NOT NULL,
  PRIMARY KEY (Funcionario_MatriculaFunc, Cargo_idCargo, Departamento_IdDpto, Equipe_idEquipe, Esporte_idEsporte, Instalacao_idInstalacao),
  CONSTRAINT fk_Funcionario_has_Equipe_Funcionario1
    FOREIGN KEY (Funcionario_MatriculaFunc)
    REFERENCES mydb.Funcionario (Funcionario_MatriculaFunc)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_Funcionario_has_Equipe_Equipe1
    FOREIGN KEY (Equipe_idEquipe, Esporte_idEsporte, Instalacao_idInstalacao)
    REFERENCES mydb.Equipe (idEquipe, Esporte_idEsporte, Instalacao_idInstalacao)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Tabela Funcionario_instrui_Esporte
CREATE TABLE IF NOT EXISTS mydb.Funcionario_instrui_Esporte (
  Funcionario_MatriculaFunc INT NOT NULL,
  Cargo_idCargo INT NOT NULL,
  Departamento_IdDpto INT NOT NULL,
  Esporte_idEsporte INT NOT NULL,
  Instalacao_idInstalacao INT NOT NULL,
  PRIMARY KEY (Funcionario_MatriculaFunc, Cargo_idCargo, Departamento_IdDpto, Esporte_idEsporte, Instalacao_idInstalacao),
  CONSTRAINT fk_Funcionario_has_Esporte_Funcionario1
    FOREIGN KEY (Funcionario_MatriculaFunc)
    REFERENCES mydb.Funcionario (Funcionario_MatriculaFunc)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_Funcionario_has_Esporte_Esporte1
    FOREIGN KEY (Esporte_idEsporte, Instalacao_idInstalacao)
    REFERENCES mydb.Esporte (idEsporte, Instalacao_idInstalacao)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);
