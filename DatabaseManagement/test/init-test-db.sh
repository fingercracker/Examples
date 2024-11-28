#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username test_user --dbname postgres <<-EOSQL


    create table h1(
        harness text,
        reference text,
        mark text,
        net text,
        wire text,
        source text,
        pin text,
        target text,
        pin_1 text,
        manufacturer text
    );

    insert into h1 (harness, reference, mark, net, wire, source, pin, target, pin_1, manufacturer)
    values 
        ('H1', 'W01', 'ABC1234', 'SOME_SIGNAL_NAME_1', 'White22AWG', 'PCUSC1-P1', '1', 'H2-H1-P1', '2', 'Multiple'),
        ('H1', 'W01', 'ABC1234', 'SOME_SIGNAL_NAME_2', 'Blue24AWG', 'PCUSC2-P1', '3', 'H2-H1-P1', '4', 'Multiple');

    create table h2(
        harness text,
        reference text,
        mark text,
        net text,
        wire text,
        source text,
        pin text,
        target text,
        pin_1 text,
        manufacturer text
    );

    insert into h2 (harness, reference, mark, net, wire, source, pin, target, pin_1, manufacturer)
    values 
        ('H2', 'W01', 'ABC1234', 'SOME_SIGNAL_NAME_1', 'White22AWG', 'H2-H1-J1', '2', 'RWA1-P2', '10', 'Multiple'),
        ('H2', 'W01', 'ABC1234', 'SOME_SIGNAL_NAME_2', 'Blue24AWG', 'H2-H1-J1', '4', 'RWA1-P2', '20', 'Multiple');

    create table h3(
        harness text,
        reference text,
        mark text,
        net text,
        wire text,
        source text,
        pin text,
        target text,
        pin_1 text,
        manufacturer text
    );

    insert into h3 (harness, reference, mark, net, wire, source, pin, target, pin_1, manufacturer)
    values 
        ('H3', 'W01', 'ABC1234', 'SOME_SIGNAL_NAME_3', 'White22AWG', 'XFC-ARM-J1', '2', 'XFC-P1', '10', 'Multiple'),
        ('H3', 'W01', 'ABC1234', 'SOME_SIGNAL_NAME_3', 'White22AWG', 'FTSU-P09', '4', 'XFC-ARM-J1', '20', 'Multiple');

EOSQL
