import React from 'react';
import './App.css';
import { TableElements } from './TableElements';
import stus from 'data/pyrxsum/pyrxsum-stus.json';
import smus from 'data/pyrxsum/pyrxsum-smus.json';
import scus from 'data/pyrxsum/pyrxsum-scus.json';
import acc from 'data/pyrxsum/pyrxsum-acc.json';
// import stus from 'data/tac08/tac2008-stus.json';
// import smus from 'data/tac08/tac2008-smus.json';
// import scus from 'data/tac08/tac2008-scus.json';

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
              {ex.summary}
                <TableElements scus={scus[ind].scus} smus={smus[ind].smus} stus={stus[ind].stus} accSMUs={acc[ind]['acc-smus']} accSTUs={acc[ind]['acc-stus']} />
            </div>
          ))
        }
        </div>
      </body>
    </div>
  );
}

export default App;
