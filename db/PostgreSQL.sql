----------------------------- Clube Esportivo -----------------------------

----------------------------- Setup  Database -----------------------------

-- O que seria passado para criar a role de DBA e o DB:
-- CREATE ROLE clube_dba WITH PASSWORD '1234567' CREATEDB LOGIN;
-- CREATE DATABASE db_clube_esportivo;

--------------------------------- Tabelas ---------------------------------


CREATE TABLE IF NOT EXISTS esportes (
    id_esporte integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nome varchar
);

CREATE TABLE IF NOT EXISTS instalacoes (
    id_instalacao integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nome varchar,
    em_funcionamento boolean DEFAULT FALSE,
    capacidade integer DEFAULT 0 NOT NULL
);

CREATE TABLE IF NOT EXISTS equipes (
    id_equipe integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nome varchar,
    esporte_praticado integer NOT NULL
);

CREATE TABLE IF NOT EXISTS associados (
    cpf varchar(11) PRIMARY KEY,
    nome varchar,
    foto bytea,
    data_adesao date,
    data_nascimento date,
    endereco varchar,
    email varchar,
    associado_titular varchar,
    contrato integer NOT NULL
);

CREATE TABLE IF NOT EXISTS associados_telefones (
    associado varchar,
    telefone varchar(13),
    PRIMARY KEY (associado, telefone)
);

CREATE TABLE IF NOT EXISTS atestados (
    id_atestado integer GENERATED ALWAYS AS IDENTITY,
    associado varchar,
    data_emissao date,
    data_validade date,
    emitido_pelo_funcionario varchar,
    PRIMARY KEY (id_atestado, associado)
);

CREATE TABLE IF NOT EXISTS contratos (
    id_contrato integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    data_inicio date,
    data_termino date,
    plano varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS pagamentos (
    data_vencimento date,
    contrato integer,
    valor numeric(15,2) NOT NULL,
    data_pagamento date,
    PRIMARY KEY (data_vencimento, contrato)
);

CREATE TABLE IF NOT EXISTS planos (
    nome varchar PRIMARY KEY,
    valor numeric(15,2)
);

CREATE TABLE IF NOT EXISTS eventos (
    id_evento integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nome varchar NOT NULL,
    data date NOT NULL,
    descricao varchar
);

CREATE TABLE IF NOT EXISTS funcionarios (
    cpf varchar(11) PRIMARY KEY,
    nome varchar,
    data_nascimento date,
    data_admissao date,
    email varchar,
    salario numeric(15,2),
    endereco varchar,
    cargo integer NOT NULL,
    departamento integer NOT NULL
);

CREATE TABLE IF NOT EXISTS funcionarios_telefones (
    funcionario varchar,
    telefone varchar(13),
    PRIMARY KEY (funcionario, telefone)
);

CREATE TABLE IF NOT EXISTS departamentos (
    id_departamento integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nome varchar NOT NULL,
    localizacao integer
);

CREATE TABLE IF NOT EXISTS cargos (
    id_cargo integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nome varchar NOT NULL,
    descricao varchar,
    salario_base numeric(15, 2)
);

----------------------------------- N-N -----------------------------------

CREATE TABLE IF NOT EXISTS associados_equipes (
    associado varchar REFERENCES associados (cpf),
    equipe integer REFERENCES equipes (id_equipe),
    PRIMARY KEY (associado, equipe)
);

CREATE TABLE IF NOT EXISTS associados_eventos (
    associado varchar REFERENCES associados (cpf),
    evento integer REFERENCES eventos (id_evento),
    PRIMARY KEY (associado, evento)
);

CREATE TABLE IF NOT EXISTS equipes_eventos (
    equipe integer REFERENCES equipes (id_equipe),
    evento integer REFERENCES eventos (id_evento),
    PRIMARY KEY (equipe, evento)
);

CREATE TABLE IF NOT EXISTS funcionarios_esportes (
    funcionario varchar REFERENCES funcionarios (cpf),
    esporte integer REFERENCES esportes (id_esporte),
    PRIMARY KEY (funcionario, esporte)
);

CREATE TABLE IF NOT EXISTS funcionarios_equipes (
    funcionario varchar REFERENCES funcionarios (cpf),
    equipe integer REFERENCES equipes (id_equipe),
    PRIMARY KEY (funcionario, equipe)
);

CREATE TABLE IF NOT EXISTS instalacoes_departamentos (
    instalacao integer REFERENCES instalacoes (id_instalacao),
    departamento integer REFERENCES departamentos (id_departamento),
    PRIMARY KEY (instalacao, departamento)
);

CREATE TABLE IF NOT EXISTS instalacoes_eventos (
    instalacao integer REFERENCES instalacoes (id_instalacao),
    evento integer REFERENCES eventos (id_evento),
    PRIMARY KEY (instalacao, evento)
);

CREATE TABLE IF NOT EXISTS instalacoes_esportes (
    instalacao integer REFERENCES instalacoes (id_instalacao),
    esporte integer REFERENCES esportes (id_esporte),
    PRIMARY KEY (instalacao, esporte)
);


-------------------------------- 1-N & FK --------------------------------

ALTER TABLE equipes
ADD FOREIGN KEY (esporte_praticado) REFERENCES esportes (id_esporte) MATCH FULL;

ALTER TABLE associados
ADD FOREIGN KEY (contrato) REFERENCES contratos (id_contrato) MATCH FULL;

ALTER TABLE associados
ADD FOREIGN KEY (associado_titular) REFERENCES associados (cpf) MATCH FULL;

ALTER TABLE associados_telefones
ADD FOREIGN KEY (associado) REFERENCES associados (cpf) MATCH FULL;

ALTER TABLE atestados
ADD FOREIGN KEY (associado) REFERENCES associados (cpf) MATCH FULL;

ALTER TABLE atestados
ADD FOREIGN KEY (emitido_pelo_funcionario) REFERENCES funcionarios (cpf) MATCH FULL;

ALTER TABLE contratos
ADD FOREIGN KEY (plano) REFERENCES planos (nome) MATCH FULL;

ALTER TABLE pagamentos
ADD FOREIGN KEY (contrato) REFERENCES contratos (id_contrato) MATCH FULL;

ALTER TABLE funcionarios
ADD FOREIGN KEY (cargo) REFERENCES cargos (id_cargo) MATCH FULL;

ALTER TABLE funcionarios
ADD FOREIGN KEY (departamento) REFERENCES departamentos (id_departamento) MATCH FULL;

ALTER TABLE funcionarios_telefones
ADD FOREIGN KEY (funcionario) REFERENCES funcionarios (cpf) MATCH FULL;

ALTER TABLE departamentos
ADD FOREIGN KEY (localizacao) REFERENCES instalacoes (id_instalacao) MATCH FULL;
