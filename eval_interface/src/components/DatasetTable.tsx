import DataUnitTable from "./DataUnitTable";
import React from "react";

import scusRealsumm from '../data/realsumm/realsumm-scus.json';
import stusRealsumm from '../data/realsumm/realsumm-stus.json';
import smusSG2Realsumm from '../data/realsumm/realsumm-smus-sg2.json';
//import smusSG3Realsumm from '../data/realsumm/realsumm-smus-sg3.json';
import acc2Realsumm from '../data/realsumm/realsumm-acc-sg2.json';
//import acc3Realsumm from '../data/realsumm/realsumm-acc-sg3.json';


import scusPyrxsum from '../data/pyrxsum/pyrxsum-scus.json';
import stusPyrxsum from '../data/pyrxsum/pyrxsum-stus.json';
import smusSG2Pyrxsum from '../data/pyrxsum/pyrxsum-smus-sg2.json';
//import smusSG3Pyrxsum from '../data/pyrxsum/pyrxsum-smus-sg3.json';
import acc2Pyrxsum from '../data/pyrxsum/pyrxsum-acc-sg2.json';
//import acc3Pyrxsum from '../data/pyrxsum/pyrxsum-acc-sg3.json';

/*
import scusTac08 from '../data/tac08/tac2008-scus.json';
import stusTac08 from '../data/tac08/tac2008-stus.json';
import smusTac08 from '../data/tac08/tac2008-smus.json';
import accTac08 from '../data/tac08/tac08-acc.json';

import scusTac09 from '../data/tac09/tac2009-scus.json';
import stusTac09 from '../data/tac09/tac2009-stus.json';
import smusTac09 from '../data/tac09/tac2009-smus.json';
import accTac09 from '../data/tac09/tac09-acc.json';*/

import {Dataset} from "./Enums";

interface Props {
    dataset: string
    isDetailOpen: boolean
    metric: string
}

const DatasetTable = (props: Props) => {
    const {dataset, isDetailOpen, metric} = props;

    let stus: any[] = [];
    let smus: any[] = [];
    let scus: any[] = [];
    let acc: any[] = [];

    switch (dataset) {
        // PyrXsum
        case Dataset.PyrXsum: {
            scus = scusPyrxsum;
            stus = stusPyrxsum;
            smus = smusSG2Pyrxsum;
            acc = acc2Pyrxsum
            break;
        }
        /*
        case Dataset.Tac08: {
            scus = scusTac08;
            stus = stusTac08;
            smus = smusTac08;
            acc = accTac08;
            break;
        }
       case Dataset.Tac09: {
           scus = scusTac09;
           stus = stusTac09;
           smus = smusTac09;
           acc = accTac09;
           break;
       }*/
        // Realsumm
        default: {
            scus = scusRealsumm;
            stus = stusRealsumm;
            smus = smusSG2Realsumm;
            acc = acc2Realsumm
            break;
        }
    }

    return (
        <div className='table-wrapper'>
            {scus.map((ex, ind) => (
                <DataUnitTable key={ex.instance_id} ex={ex} ind={ind} isDetailOpen={isDetailOpen} scus={scus}
                               stus={stus} smus={smus} acc={acc} metric={metric}/>
            ))}
        </div>
    );
};

export default DatasetTable;
