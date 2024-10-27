#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username test_user --dbname postgres <<-EOSQL

    create table h1(
        harnessname text,
        cablename text,
        cabletype text,
        wirename text,
        fromconnectorname text,
        fromconnectorlibdataname text,
        frompinname text,
        fromcontactmodelname text,
        toconnectorname text,
        toconnectorlibdataname text,
        topinname text,
        tocontactmodelname text,
        signal text
    );

    insert into h1 (
        harnessname,
        cablename,
        cabletype,
        wirename,
        fromconnectorname,
        fromconnectorlibdataname,
        frompinname,
        fromcontactmodelname,
        toconnectorname,
        toconnectorlibdataname,
        topinname,
        tocontactmodelname,
        signal
    )
    values 
        ('H1', 'H1-W39', 'M27500A22SR2U00', '1', 'PCUSC1-P1', 'SDD104M1000G-1144.8', '2', '', 'H2-H1-P1', 'D38999/26GJ61SN', '4', '', 'SOME_SIGNAL_NAME_1'),
        ('H1', 'H1-W39', 'M27500A22SR2U00', '2', 'PCUSC1-P1', 'SDD104M1000G-1144.8', '4', '', 'H2-H1-P1', 'D38999/26GJ61SN', '3', '', 'SOME_SIGNAL_NAME_2'),
        ('H1', 'H1-W39', 'M27500A22SR2U00', '2', 'PCUSC1-P1', 'SDD104M1000G-1144.8', '4', '', 'H2-H1-P1', 'D38999/26GJ61SN', '20', '', 'SOME_SIGNAL_NAME_3'),
        ('H1', 'H1-W39', 'M27500A22SR2U00', '2', 'PCUSC1-P1', 'SDD104M1000G-1144.8', '4', '', 'H2-H1-P1', 'D38999/26GJ61SN', '3', '', 'SOME_SIGNAL_NAME_4'),
        ('H1', 'H1-W53', 'M22759/44-20-9',	'1', 'Something', 'SDD104M1000G-1144.8', '103', '', 'H5-H1-P1',	'Something_else', 'F', '', 'TEST_PLUG_SIGNAL'),
        ('H1', 'H1-W54', 'M27500-20SR2S23', '1', 'BlaBla', 'SDD104M1000G-1144.8', '104', '', 'H6-H1-P1', 'Foo', 'S', '', 'SPLICE_SIGNAL');

    create table h2(
        harnessname text,
        cablename text,
        cabletype text,
        wirename text,
        fromconnectorname text,
        fromconnectorlibdataname text,
        frompinname text,
        fromcontactmodelname text,
        toconnectorname text,
        toconnectorlibdataname text,
        topinname text,
        tocontactmodelname text,
        signal text
    );

    insert into h2 (
        harnessname,
        cablename,
        cabletype,
        wirename,
        fromconnectorname,
        fromconnectorlibdataname,
        frompinname,
        fromcontactmodelname,
        toconnectorname,
        toconnectorlibdataname,
        topinname,
        tocontactmodelname,
        signal
    )
    values 
        ('H2', 'H2-W39', 'M27500A22SR2U00', '1', 'H2-H1-J1', 'SDD104M1000G-1144.8', '4', '', 'RWA1-P2', 'D38999/26GJ61SN', '15', '', 'SOME_SIGNAL_NAME_1'),
        ('H2', 'H2-W39', 'M27500A22SR2U01', '2', 'H2-H1-J1', 'SDD104M1000G-1144.8', '3', '', 'RWA1-P2', 'D38999/26GJ61SN', '14', '', 'SOME_SIGNAL_NAME_2'),
        ('H2', 'H2-W39', 'M27500A22SR2U00', '2', 'H2-H1-J1', 'SDD104M1000G-1144.8', '21', '', 'RWA1-P2', 'D38999/26GJ61SN', '17', '', 'SOME_SIGNAL_NAME_3');

    create table h3(
        harnessname text,
        cablename text,
        cabletype text,
        wirename text,
        fromconnectorname text,
        fromconnectorlibdataname text,
        frompinname text,
        fromcontactmodelname text,
        toconnectorname text,
        toconnectorlibdataname text,
        topinname text,
        tocontactmodelname text,
        signal text
    );

    insert into h3 (
        harnessname,
        cablename,
        cabletype,
        wirename,
        fromconnectorname,
        fromconnectorlibdataname,
        frompinname,
        fromcontactmodelname,
        toconnectorname,
        toconnectorlibdataname,
        topinname,
        tocontactmodelname,
        signal
    )
    values 
        ('H3', 'H3-W01', 'ABC1234', '1', 'XFC-ARM-J1', 'BLABLA', '3', '', 'XFC-P1', 'WhoDoneIt', '2', '', 'SOME_SIGNAL_NAME_3'),
        ('H3', 'H3-W07', 'ABC1234', '1', 'FTSU-P09', 'WUTWUT', '4', '', 'XFC-ARM-J1', 'TheyDoneDidIt', '14', '', 'SOME_SIGNAL_NAME_3');

    create table h4(
        harnessname text,
        cablename text,
        cabletype text,
        wirename text,
        fromconnectorname text,
        fromconnectorlibdataname text,
        frompinname text,
        fromcontactmodelname text,
        toconnectorname text,
        toconnectorlibdataname text,
        topinname text,
        tocontactmodelname text,
        signal text
    );

    insert into h4 (
        harnessname,
        cablename,
        cabletype,
        wirename,
        fromconnectorname,
        fromconnectorlibdataname,
        frompinname,
        fromcontactmodelname,
        toconnectorname,
        toconnectorlibdataname,
        topinname,
        tocontactmodelname,
        signal
    )
    values
        ('H4', 'H3-W01', 'ABC1234', '1', 'FTSU-P09', 'BLABLA', '7', '', 'XFC-ARM-J1', 'Wahoo', '1', '', 'SOME_SIGNAL_NAME_N'), 
        ('H4', 'H3-W01', 'ABC1234', '1', 'XFC-ARM-J1', 'BLABLA', '3', '', 'XFC-P1', 'WhoDoneIt', '2', '', 'SOME_SIGNAL_NAME_4'),
        ('H4', 'H3-W01', 'ABC1234', '1', 'XFC-ARM-J1', 'BLABLA', '5', '', 'XFC-P1', 'WhoDoneIt', '10', '', 'SOME_SIGNAL_NAME_4'),
        ('H4', 'H3-W07', 'ABC1234', '1', 'FTSU-P09', 'WUTWUT', '4', '', 'XFC-ARM-J1', 'TheyDoneDidIt', '14', '', 'SOME_SIGNAL_NAME_4');


    create table h5(
        harnessname text,
        cablename text,
        cabletype text,
        wirename text,
        fromconnectorname text,
        fromconnectorlibdataname text,
        frompinname text,
        fromcontactmodelname text,
        toconnectorname text,
        toconnectorlibdataname text,
        topinname text,
        tocontactmodelname text,
        signal text
    );

    insert into h5 (
        harnessname,
        cablename,
        cabletype,
        wirename,
        fromconnectorname,
        fromconnectorlibdataname,
        frompinname,
        fromcontactmodelname,
        toconnectorname,
        toconnectorlibdataname,
        topinname,
        tocontactmodelname,
        signal
    )
    values
        ('H5', 'H5-W17', 'M22759/44-20-9', '1', 'H5-H1-J1', 'D38999/20GE35PN', 'F', '', 'SP6', 'SDD62S1000G-1144.8', 'A', '', 'TEST_PLUG_SIGNAL'), 
        ('H5', 'H47-W16', 'M22759/44-20-9', '1', 'SP6', 'D38999/20GE35PN', 'B', '', 'P49-P1', 'SDD62S1000G-1144.8', '26', '', 'TEST_PLUG_SIGNAL'),
        ('H5', 'H5-W19', 'M22759/44-20-9', '1', 'SP6', 'D38999/20GE35PN', 'B', '', 'PRP-TEST-J1', 'SDD62S1000G-1144.8', '5', '', 'TEST_PLUG_SIGNAL');

    create table h6(
        harnessname text,
        cablename text,
        cabletype text,
        wirename text,
        fromconnectorname text,
        fromconnectorlibdataname text,
        frompinname text,
        fromcontactmodelname text,
        toconnectorname text,
        toconnectorlibdataname text,
        topinname text,
        tocontactmodelname text,
        signal text
    );

    insert into h6 (
        harnessname,
        cablename,
        cabletype,
        wirename,
        fromconnectorname,
        fromconnectorlibdataname,
        frompinname,
        fromcontactmodelname,
        toconnectorname,
        toconnectorlibdataname,
        topinname,
        tocontactmodelname,
        signal
    )
    values
        ('H6', 'H6-W28', 'M27500-20SR2S23', '1', 'H6-H1-J1', 'D38999/20GE35PN', 'S', '', 'SP13', 'D38999/26GE35SN', 'A', '', 'SPLICE_SIGNAL'),
        ('H6', 'H6-W28', 'M22759/33-26-9', '1', 'SP13', '', 'B', '', 'P702-P1', 'SDD62S1000G-1144.8', '11', '', 'SPLICE_SIGNAL'),
        ('H6', 'H6-W25', 'M22759/33-26-9', '1', 'SP13', '', 'B', '', 'P702-P1', 'SDD62S1000G-1144.8', '23', '', 'SPLICE_SIGNAL'),
        ('H6', 'H6-W26', 'M22759/33-26-9', '1', 'SP13', '', 'B', '', 'P702-P1', 'SDD62S1000G-1144.8', '7', '', 'SPLICE_SIGNAL'),
        ('H6', 'H6-W27', 'M22759/33-26-9', '1', 'SP13', '', 'B', '', 'P702-P1', 'SDD62S1000G-1144.8', '19', '', 'SPLICE_SIGNAL');

EOSQL
