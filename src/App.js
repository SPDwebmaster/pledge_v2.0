import React, { useState } from 'react';
import './App.css';
import DashBoard from './components/dashboard';

function App() {

  const [pledgeClassName, setPledgeClassName] = useState("Pledge Class");

  return (
    <div className="App">
      <header className="App-header">
        <div className="frame">
          <h2>{pledgeClassName}</h2>
          <DashBoard setPledgeClassName={setPledgeClassName}/>
        </div>
      </header>
    </div>
  );
}

export default App;
