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
    function return_sum_tree({sum_tree}: { sum_tree: String[] }){
    const output = []
    for (let i = 0; i < Math.max(sum_tree.length); i++) {
    output.push(
        <tr>
            <td className="trees">{sum_tree[i]}</td>
        </tr>
    )
}
    return output
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
                    <tr>
                        <th>{ex.summary.replaceAll("<t>", "").replaceAll("</t>", "")}</th>
                    </tr>
                    {return_sum_tree({sum_tree: smus[ind].summary_trees})}
                </table>
                <TableElements scus={scus[ind].scus} smus={smus[ind].smus} trees={smus[ind].tree} stus={stus[ind].stus}
                               accSMUs={acc[ind]['easiness-smus-acc-bert']} accSTUs={acc[ind]['easiness-stus-acc-bert']}
                               stu_pos={acc[ind]['stus-pos-bert']} smu_pos={acc[ind]['smus-pos-bert']} />
            </div>
          ))
        }
        </div>
      </body>
    </div>
  );
}

export default App;
