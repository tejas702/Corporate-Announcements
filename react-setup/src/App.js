// Importing modules
import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  // usestate for setting a javascript
  // object for storing and using data
  const [lis, setlis] = useState([]);

  // // Using useEffect for single rendering
  useEffect(() => {
    // Using fetch to fetch the api from
    // flask server it will be redirected to proxy
    fetch("http://localhost:5000/").then((res) => {
      console.log(res);
      res.json().then((data) => {
        // Setting a data from api
        setlis(data);
      });
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>React and flask</h1>
        {lis.map((item) => {
          return (
		item.keywords.length > 0 && 	
			<div>
				<p>{item.title}</p>
				<p>{item.link}</p>
				<p>{item.keywords}</p>
			</div>
          );
        })}
      </header>
    </div>
  );
}

export default App;
