--- CLUBE ESPORTIVO


CREATE TABLE IF NOT EXISTS esporte (
    nome varchar PRIMARY KEY
);


CREATE TABLE IF NOT EXISTS instalacao (
    nome varchar PRIMARY KEY,
    em_funcionamento boolean DEFAULT FALSE,
    capacidade integer DEFAULT 0 NOT NULL
);


CREATE TABLE IF NOT EXISTS equipe (
    nome varchar PRIMARY KEY,
    esporte_praticado varchar PRIMARY KEY
);


CREATE TABLE IF NOT EXISTS associado (
    cpf varchar PRIMARY KEY,
    nome varchar,
    foto bytea,
    data_adesao date,
    data_nascimento date,
    endereco varchar,
    email varchar,
    associado_titular varchar REFERENCES associado(nome)
);


CREATE TABLE IF NOT EXISTS associado_telefone (
    cpf varchar PRIMARY KEY,
    telefone varchar(13) PRIMARY KEY
);


CREATE TABLE IF NOT EXISTS atestado (
    id_atestado integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    data_emissao date NOT NULL,
    data_validade date NOT NULL,
    emitido_pelo_funcionario varchar
);


CREATE TABLE IF NOT EXISTS contrato (
    associado_contratante varchar PRIMARY KEY,
    data_inicio date PRIMARY KEY,
    data_termino date,
    plano varchar NOT NULL
);


CREATE TABLE IF NOT EXISTS pagamento (
    data_vencimento date PRIMARY KEY,
    associado_contratante varchar PRIMARY KEY,
    data_inicio_contrato date PRIMARY KEY,
    valor numeric(15,2) NOT NULL,
    data_pagamento date
);


CREATE TABLE IF NOT EXISTS plano (
    nome varchar PRIMARY KEY,
    valor numeric(15,2)
);


CREATE TABLE IF NOT EXISTS evento (
    nome varchar NOT NULL,
    data date NOT NULL,
    descricao varchar,
    local varchar,
    organizador varchar
);


CREATE TABLE IF NOT EXISTS funcionarios (
    cpf varchar(11) PRIMARY KEY,
    nome varchar,
    data_nascimento date,
    data_admissao date,
    email varchar,
    salario numeric(15,2),
    endereco varchar,
    cargo integer,
    departamento integer
);


CREATE TABLE IF NOT EXISTS funcionarios_telefone (
    cpf varchar PRIMARY KEY,
    telefone varchar(13) PRIMARY KEY
);


CREATE TABLE IF NOT EXISTS treinadores (
    treinador varchar PRIMARY KEY,
    equipe_treinada varchar PRIMARY KEY,
    esporte varchar PRIMARY KEY
);


CREATE TABLE IF NOT EXISTS treinadores_capacitados (
    treinador varchar PRIMARY KEY,
    esporte varchar PRIMARY KEY
);


CREATE TABLE IF NOT EXISTS departamento (
    id_departamento integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nome varchar NOT NULL,
    localizacao varchar
);


CREATE TABLE IF NOT EXISTS cargo (
    id_cargo integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nome varchar NOT NULL,
    descricao varchar,
    salario_base numeric(15, 2)
);


CREATE TABLE IF NOT EXISTS esporte_acontece_em_instalacao(
    nome_esporte varchar PRIMARY KEY REFERENCES esporte(nome),
    nome_instalacao varchar PRIMARY KEY REFERENCES instalacao(nome)
);