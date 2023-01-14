import React from 'react';
import './App.css';
import { TableElements } from './TableElements';
// import stus from 'data/pyrxsum/pyrxsum-stus.json';
// import smus from 'data/pyrxsum/pyrxsum-smus.json';
// import scus from 'data/pyrxsum/pyrxsum-scus.json';
// import acc from 'data/pyrxsum/pyrxsum-acc.json';
import stus from './data/realsumm/realsumm-stus.json';
import smus from './data/realsumm/realsumm-smus-test-with-st.json';
import scus from './data/realsumm/realsumm-scus.json';
import acc from './data/realsumm/realsumm-acc-test.json';

function App() {

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
        <div className="App">
            <header className="App-header">
                <div>
                    <h1>Evaluation interface</h1>
                </div>
            </header>
            <body>
            <div>
                {scus.map((ex, ind) => (
                    <div className='instance' key={ex.instance_id}>
                        <h4>{ex.instance_id}</h4>
                        <table>
                            <tr className='table-title'>
                                <th>{ex.summary.replaceAll("<t>", "").replaceAll("</t>", "")}</th>
                            </tr>
                            {trees_table(ind)}
                        </table>
                        <TableElements scus={scus[ind].scus} smus={smus[ind].smus} trees={smus[ind].tree}
                                       stus={stus[ind].stus}
                                       accSMUs={acc[ind]['easiness-smus-acc-bert']}
                                       accSTUs={acc[ind]['easiness-stus-acc-bert']}
                                       stu_pos={acc[ind]['stus-pos-bert']} smu_pos={acc[ind]['smus-pos-bert']}/>
                    </div>
                ))}
            </div>
            </body>
        </div>
    );
}

export default App;
