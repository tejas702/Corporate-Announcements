// Importing modules
import React, { useState, useEffect } from "react";
import "./App.css";
import Table from "react-bootstrap/Table";

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
        <h1>Corporate Announcements</h1>
        <Table striped bordered hover responsive variant="dark">
          <thead>
            <tr>
              <th>Keywords</th>
              <th>Title</th>
            </tr>
          </thead>
          <tbody>
            {lis.map((item) => {
              return (
                item.keywords.length > 0 && (
                  <tr>
                    <td>{item.keywords}</td>
                    <td>
                      <a
                        href={item.link}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        {item.title}
                      </a>
                    </td>
                  </tr>
                )
              );
            })}
          </tbody>
        </Table>
      </header>
    </div>
  );
}

export default App;
