// Importing modules
import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
	// usestate for setting a javascript
	// object for storing and using data
	const [data, setdata] = useState({
		title: "",
		link: "",
		keywords: [],
	});

	// // Using useEffect for single rendering
	useEffect(() => {
		// Using fetch to fetch the api from
		// flask server it will be redirected to proxy
		fetch("http://localhost:5000/").then((res) => {
            console.log(res);
			res.json().then((data) => {
				// Setting a data from api
				setdata({
					title: data.title,
					link: data.link,
					keywords: data.keywords,
				});
			})
        });
	}, []);


    // const fetchAndLog = async () => {
    //     const response = await fetch('http://localhost:5000/');
    //     const json = await response.json();
    //     // just log ‘json’
    //     console.log(json);
    // }
    
    // fetchAndLog();

	return (
		<div className="App">
			<header className="App-header">
				<h1>React and flask</h1>
				<p>{data.title}</p>
				<p>{data.link}</p>
				<p>{data.keywords}</p>
			</header>
		</div>
	);
}

export default App;
