import React, { useState, useEffect } from "react";
import "./App.css";

interface IData {
  members: string[];
}

const App: React.FC = () => {
  const [data, setData] = useState<IData[]>([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/members')
      .then((res) => res.json())
      .then((data) => {
        setData([data]);
        console.log(data);
      })
      .catch((e) => {
        console.log(e);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Data from Flask API</h1>
        {data.length === 0 ? (
          <p> loading ... </p>
        ) : (
          data[0].members.map((member, i) => (
            <p key={i}>{member}</p>
          ))
        )}
      </header>
    </div>
  );
};

export default App;
