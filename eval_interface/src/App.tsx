import React from 'react';
import './App.css';
import { TableElements } from './TableElements';
// import stus from 'data/pyrxsum/pyrxsum-stus.json';
// import smus from 'data/pyrxsum/pyrxsum-smus.json';
// import scus from 'data/pyrxsum/pyrxsum-scus.json';
// import acc from 'data/pyrxsum/pyrxsum-acc.json';
import stus from './data/realsumm/realsumm-stus.json';
import smus from './data/realsumm/realsumm-smus.json';
import scus from './data/realsumm/realsumm-scus.json';
import acc from './data/realsumm/realsumm-acc.json';

function App() {
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
              {ex.summary.replaceAll("<t>", "").replaceAll("</t>", "")}
                <TableElements scus={scus[ind].scus} smus={smus[ind].smus} trees={smus[ind].tree} stus={stus[ind].stus} accSMUs={acc[ind]['easiness-smus-acc-bert']} accSTUs={acc[ind]['easiness-stus-acc-bert']} />
            </div>
          ))
        }
        </div>
      </body>
    </div>
  );
}

export default App;
