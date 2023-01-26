import {TableElements} from "./TableElements";
import React, {useState} from "react";
import {Collapse} from 'react-collapse';
import IconButton from '@mui/material/IconButton';
import {Stack} from "@mui/material";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';

import stus from './data/realsumm/realsumm-stus.json';
import smus from './data/realsumm/realsumm-smus-sg2.json';
import scus from './data/realsumm/realsumm-scus.json';
import acc from './data/realsumm/realsumm-acc-sg2.json';

function CustomTable(props: { ex: any, ind: any }) {
    const [isOpen, setIsOpen] = useState(true);

    const trees_table = (ind: number) => {
        const sentences: string[] = [];
        const trees: string[] = []
        smus[ind].summary_trees.forEach((sum_tree) => {
            const str = sum_tree.toString();
            sentences.push(str.slice(0, str.indexOf('\n')));
            trees.push(str.slice(str.indexOf('\n') + 1));
        })
        return (
            <table>
                <tr>
                    {sentences.map((sent) => {
                        return <td>{sent}</td>
                    })}
                </tr>
                <tr className='tree-table'>{
                    trees.map((tree) => {
                        return <td>{tree}</td>
                    })}
                </tr>
            </table>
        )
    }

    return (
        <div className='instance' key={props.ind}>
            <Stack direction="row">
                <h4>{props.ex.instance_id}</h4>
                <IconButton aria-label="collapse" onClick={() => setIsOpen(!isOpen)}
                            color="primary">
                    {isOpen ? <KeyboardArrowDownIcon/> : <KeyboardArrowRightIcon/>}
                </IconButton>
            </Stack>
            <Collapse isOpened={isOpen}>
                <table key={props.ex.instance_id}>
                    <tr className='table-title'>
                        <th>{props.ex.summary.replaceAll("<t>", "").replaceAll("</t>", "")}</th>
                    </tr>
                    {trees_table(props.ind)}
                </table>
                <TableElements scus={scus[props.ind].scus}
                               smus={smus[props.ind].smus}
                               trees={smus[props.ind].tree}
                               stus={stus[props.ind].stus}
                               accSMUs={acc[props.ind]["easiness-smus-acc-bert"]}
                               accSTUs={acc[props.ind]["easiness-stus-acc-bert"]}
                               stu_pos={acc[props.ind]["stus-pos-bert"]}
                               smu_pos={acc[props.ind]["smus-pos-bert"]}/>
            </Collapse>
        </div>
    );
}

export default CustomTable;