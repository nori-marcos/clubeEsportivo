----------------------------- Clube Esportivo -----------------------------

----------------------------- Setup  Database -----------------------------

-- O que seria passado para criar a role de DBA e o DB:
-- CREATE ROLE clube_dba WITH PASSWORD '1234567' CREATEDB LOGIN;
-- CREATE DATABASE db_clube_esportivo;

--------------------------------- Tabelas ---------------------------------


CREATE TABLE IF NOT EXISTS esportes
(
    id_esporte integer PRIMARY KEY,
    nome       varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS instalacoes
(
    id_instalacao    integer PRIMARY KEY,
    nome             varchar NOT NULL,
    em_funcionamento boolean DEFAULT FALSE NOT NULL,
    capacidade       integer DEFAULT 0 NOT NULL
);

CREATE TABLE IF NOT EXISTS equipes
(
    id_equipe         integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
    nome              varchar NOT NULL,
    esporte_praticado integer NOT NULL
);

CREATE TABLE IF NOT EXISTS associados
(
    cpf               varchar(11) PRIMARY KEY,
    nome              varchar NOT NULL,
    foto              bytea,
    data_adesao       date NOT NULL,
    data_nascimento   date NOT NULL,
    endereco          varchar NOT NULL,
    email             varchar NOT NULL,
    associado_titular varchar,
    contrato          integer NOT NULL
);

CREATE TABLE IF NOT EXISTS associados_telefones
(
    associado varchar,
    telefone  varchar(13),
    PRIMARY KEY (associado, telefone)
);

CREATE TABLE IF NOT EXISTS atestados
(
    id_atestado              integer GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
    associado                varchar NOT NULL,
    data_emissao             date NOT NULL,
    data_validade            date NOT NULL,
    emitido_pelo_funcionario varchar NOT NULL,
    PRIMARY KEY (id_atestado, associado)
);

CREATE TABLE IF NOT EXISTS contratos
(
    id_contrato  integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
    data_inicio  date NOT NULL,
    data_termino date NOT NULL,
    plano        varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS pagamentos
(
    data_vencimento date NOT NULL,
    contrato        integer NOT NULL,
    valor           numeric(15, 2) NOT NULL,
    data_pagamento  date NOT NULL,
    PRIMARY KEY (data_vencimento, contrato)
);

CREATE TABLE IF NOT EXISTS planos
(
    nome  varchar PRIMARY KEY,
    valor numeric(15, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS eventos
(
    id_evento integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
    nome      varchar NOT NULL,
    data      date    NOT NULL,
    descricao varchar
);

CREATE TABLE IF NOT EXISTS funcionarios
(
    cpf             varchar(11) PRIMARY KEY,
    nome            varchar NOT NULL,
    data_nascimento date NOT NULL,
    data_admissao   date NOT NULL,
    email           varchar NOT NULL,
    salario         numeric(15, 2) NOT NULL,
    endereco        varchar NOT NULL,
    cargo           integer NOT NULL,
    departamento    integer NOT NULL
);

CREATE TABLE IF NOT EXISTS funcionarios_telefones
(
    funcionario varchar,
    telefone    varchar(13),
    PRIMARY KEY (funcionario, telefone)
);

CREATE TABLE IF NOT EXISTS departamentos
(
    id_departamento integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
    nome            varchar NOT NULL,
    localizacao     integer
);

CREATE TABLE IF NOT EXISTS cargos
(
    id_cargo     integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
    nome         varchar NOT NULL,
    descricao    varchar NOT NULL,
    salario_base numeric(15, 2) NOT NULL
);

----------------------------------- N-N -----------------------------------

CREATE TABLE IF NOT EXISTS associados_equipes
(
    associado varchar REFERENCES associados (cpf),
    equipe    integer REFERENCES equipes (id_equipe),
    PRIMARY KEY (associado, equipe)
);

CREATE TABLE IF NOT EXISTS associados_eventos
(
    associado varchar REFERENCES associados (cpf),
    evento    integer REFERENCES eventos (id_evento),
    PRIMARY KEY (associado, evento)
);

CREATE TABLE IF NOT EXISTS equipes_eventos
(
    equipe integer REFERENCES equipes (id_equipe),
    evento integer REFERENCES eventos (id_evento),
    PRIMARY KEY (equipe, evento)
);

CREATE TABLE IF NOT EXISTS funcionarios_esportes
(
    funcionario varchar REFERENCES funcionarios (cpf),
    esporte     integer REFERENCES esportes (id_esporte),
    PRIMARY KEY (funcionario, esporte)
);

CREATE TABLE IF NOT EXISTS funcionarios_equipes
(
    funcionario varchar REFERENCES funcionarios (cpf),
    equipe      integer REFERENCES equipes (id_equipe),
    PRIMARY KEY (funcionario, equipe)
);

CREATE TABLE IF NOT EXISTS instalacoes_departamentos
(
    instalacao   integer REFERENCES instalacoes (id_instalacao),
    departamento integer REFERENCES departamentos (id_departamento),
    PRIMARY KEY (instalacao, departamento)
);

CREATE TABLE IF NOT EXISTS instalacoes_eventos
(
    instalacao integer REFERENCES instalacoes (id_instalacao),
    evento     integer REFERENCES eventos (id_evento),
    PRIMARY KEY (instalacao, evento)
);

CREATE TABLE IF NOT EXISTS instalacoes_esportes
(
    instalacao integer REFERENCES instalacoes (id_instalacao),
    esporte    integer REFERENCES esportes (id_esporte),
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
